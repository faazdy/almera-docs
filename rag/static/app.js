const chatEl = document.getElementById('chat');
const emptyEl = document.getElementById('empty');
const form = document.getElementById('composer');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send');
const moduleSel = document.getElementById('module');
const contributeBtn = document.getElementById('contribute');
const uploadDialog = document.getElementById('upload-dialog');
const uploadForm = document.getElementById('upload-form');
const uploadModule = document.getElementById('upload-module');
const uploadFile = document.getElementById('upload-file');
const uploadSubmit = document.getElementById('upload-submit');
const uploadResult = document.getElementById('upload-result');

const history = [];
let busy = false;
let maxUploadMb = 20;

const render = (md) => DOMPurify.sanitize(marked.parse(md));

const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

async function loadModules() {
    try {
        const res = await fetch('/api/modules');
        const data = await res.json();
        document.getElementById('model').textContent = data.model;
        for (const m of data.modules) {
            const opt = document.createElement('option');
            opt.value = m.id;
            opt.textContent = m.name;
            opt.title = m.description;
            moduleSel.appendChild(opt);
            if (m.uploads !== false) uploadModule.appendChild(opt.cloneNode(true));
        }
        maxUploadMb = data.max_upload_mb;
        contributeBtn.hidden = !data.upload;
    } catch {
        document.getElementById('model').textContent = 'servidor no disponible';
    }
}

function addTurn(question) {
    emptyEl?.remove();
    const turn = document.createElement('article');
    turn.className = 'turn';
    turn.innerHTML = `
        <div class="turn-label">Pregunta</div>
        <p class="turn-q"></p>
        <div class="turn-label"><span class="dot"></span>SABIA<span class="modules"></span></div>
        <div class="answer"><span class="typing"><i></i><i></i><i></i></span></div>`;
    turn.querySelector('.turn-q').textContent = question;
    chatEl.appendChild(turn);
    return {
        turn,
        modules: turn.querySelector('.modules'),
        answer: turn.querySelector('.answer'),
    };
}

function scrollDown() {
    window.scrollTo({ top: document.body.scrollHeight });
}

function renderMeta(ui, meta) {
    if (meta.modules.length) ui.modules.textContent = `· ${meta.modules.join(' · ')}`;
    if (!meta.sources.length) return;
    const details = document.createElement('details');
    details.className = 'sources';
    details.innerHTML = `<summary>Secciones consultadas</summary><ul>${meta.sources
        .map((s) => `<li>${esc(s.module)} › ${esc(s.section)}</li>`)
        .join('')}</ul>`;
    ui.sources = details;
}

// Lee el stream SSE de /api/chat (POST, así que no sirve EventSource)
async function* readEvents(res) {
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        let idx;
        while ((idx = buffer.indexOf('\n\n')) !== -1) {
            const raw = buffer.slice(0, idx);
            buffer = buffer.slice(idx + 2);
            const event = raw.match(/^event: (.*)$/m)?.[1];
            const data = raw.match(/^data: (.*)$/m)?.[1];
            if (event) yield { event, data: JSON.parse(data) };
        }
    }
}

async function ask(question) {
    busy = true;
    sendBtn.disabled = true;
    history.push({ role: 'user', content: question });
    const ui = addTurn(question);
    scrollDown();

    let answer = '';
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: history, module: moduleSel.value || null }),
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(typeof err.detail === 'string' ? err.detail : `Error ${res.status}`);
        }
        for await (const { event, data } of readEvents(res)) {
            if (event === 'meta') renderMeta(ui, data);
            else if (event === 'delta') {
                answer += data;
                ui.answer.innerHTML = render(answer);
                scrollDown();
            } else if (event === 'error') throw new Error(data);
        }
        history.push({ role: 'assistant', content: answer });
        if (ui.sources) ui.answer.after(ui.sources);
    } catch (err) {
        history.pop(); // la pregunta fallida no queda en el historial
        ui.answer.classList.add('error');
        ui.answer.textContent = err.message;
    } finally {
        busy = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q || busy) return;
    input.value = '';
    input.style.height = '';
    ask(q);
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        form.requestSubmit();
    }
});

input.addEventListener('input', () => {
    input.style.height = '';
    input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
});

document.querySelectorAll('.quicklink').forEach((btn) =>
    btn.addEventListener('click', () => !busy && ask(btn.dataset.q))
);

// ---------- Aportar un documento ----------
const STATUS = {
    verde: { icon: '🟢', title: 'Publicado. SABIA ya lo usa para responder.' },
    amarillo: { icon: '🟡', title: 'Publicado con advertencias. SABIA ya lo usa, pero conviene mejorarlo:' },
    rojo: { icon: '🔴', title: 'No se publicó. Corrígelo y vuelve a subirlo:' },
};
const ALLOWED = ['.docx', '.pdf', '.pptx', '.xlsx', '.txt', '.md'];
const OLD_FORMATS = { '.doc': '.docx', '.ppt': '.pptx', '.xls': '.xlsx' };

function showResult(kind, title, notes = []) {
    uploadResult.hidden = false;
    uploadResult.className = `upload-result ${kind}`;
    uploadResult.innerHTML = `<p class="result-title">${esc(title)}</p>${
        notes.length ? `<ul>${notes.map((n) => `<li>${esc(n)}</li>`).join('')}</ul>` : ''
    }`;
}

// Revisa lo obvio antes de subir, para no hacer esperar a nadie por un error evidente
function checkFile(file) {
    if (!uploadModule.value) return 'Elige el módulo al que pertenece el documento.';
    if (!file) return 'Elige el archivo que quieres publicar.';
    const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
    if (OLD_FORMATS[ext])
        return `Es un formato antiguo (${ext}). Ábrelo y usa Guardar como → ${OLD_FORMATS[ext]}.`;
    if (!ALLOWED.includes(ext))
        return 'Formato no soportado. Usa Word (.docx), PDF, PowerPoint (.pptx), Excel (.xlsx) o texto (.txt).';
    if (file.name.startsWith('~$')) return 'Ese es un archivo temporal de Office. Elige el documento original.';
    if (!file.size) return 'El archivo está vacío.';
    if (file.size > maxUploadMb * 1024 * 1024) return `El archivo pesa más de ${maxUploadMb} MB.`;
    return null;
}

async function sendFile(file, replace) {
    const params = new URLSearchParams({ module: uploadModule.value, filename: file.name, replace });
    const res = await fetch(`/api/upload?${params}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/octet-stream' },
        body: file,
    });
    const data = await res.json().catch(() => ({}));
    return { res, data };
}

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = uploadFile.files[0];
    const problem = checkFile(file);
    if (problem) return showResult('rojo', problem);

    uploadSubmit.disabled = true;
    uploadSubmit.textContent = 'Revisando…';
    showResult('working', 'Guardando y revisando el documento. Puede tardar unos segundos…');
    try {
        let { res, data } = await sendFile(file, false);
        if (res.status === 409) {
            const moduleName = uploadModule.selectedOptions[0].textContent;
            if (!confirm(`Ya existe "${file.name}" en ${moduleName}.\n\n¿Reemplazarlo por esta versión?`)) {
                showResult('working', 'No se subió nada. Cambia el nombre del archivo si es un documento distinto.');
                return;
            }
            ({ res, data } = await sendFile(file, true));
        }
        if (!res.ok) throw new Error(typeof data.detail === 'string' ? data.detail : `Error ${res.status}`);
        const s = STATUS[data.status];
        showResult(data.status, `${s.icon} ${s.title}`, data.notes);
        if (data.status !== 'rojo') uploadFile.value = '';
    } catch (err) {
        showResult('rojo', err.message === 'Failed to fetch' ? 'No hay conexión con el servidor.' : err.message);
    } finally {
        uploadSubmit.disabled = false;
        uploadSubmit.textContent = 'Publicar';
    }
});

contributeBtn.addEventListener('click', () => {
    // Solo si ese módulo acepta documentos (el de "cómo alimentar a SABIA" no)
    if (moduleSel.value && uploadModule.querySelector(`option[value="${moduleSel.value}"]`))
        uploadModule.value = moduleSel.value;
    uploadResult.hidden = true;
    uploadDialog.showModal();
});
uploadDialog.querySelector('[data-close]').addEventListener('click', () => uploadDialog.close());
uploadDialog.addEventListener('click', (e) => e.target === uploadDialog && uploadDialog.close());
[uploadModule, uploadFile].forEach((el) => el.addEventListener('change', () => (uploadResult.hidden = true)));

loadModules();
input.focus();
