const chatEl = document.getElementById('chat');
const emptyEl = document.getElementById('empty');
const form = document.getElementById('composer');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send');
const moduleSel = document.getElementById('module');

const history = [];
let busy = false;

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
        }
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

loadModules();
input.focus();
