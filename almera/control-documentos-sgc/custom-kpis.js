(function(){
  "use strict";

  // Motor de indicadores personalizados: permite que alguien sin conocimientos de
  // código agregue tarjetas de KPI adicionales (mismo formato que las nativas del
  // informe) desde un panel, sin tocar main.js. Ver docs/02-informes.md.
  //
  // Solo cubre condiciones de un solo campo (vacío/no vacío/igual/distinto/contiene/
  // mayor/menor). Reglas que cruzan varios campos (duplicados, fechas futuras, etc.)
  // siguen requiriendo un cambio de código — ver sección "Mantenimiento" de la doc.

  const SEVERITY_LABEL = { problem: 'Requiere acción', warn: 'Atención', info: 'Informativo' };

  const OPERATORS_BY_TYPE = {
    text:   [['empty','está vacío'],['not_empty','no está vacío'],['equals','es igual a'],['not_equals','es distinto de'],['contains','contiene']],
    number: [['empty','está vacío'],['not_empty','no está vacío'],['equals','es igual a'],['gt','es mayor que'],['lt','es menor que']],
    years:  [['empty','sin fecha'],['not_empty','con fecha'],['gt','es mayor que (años)'],['lt','es menor que (años)']]
  };
  const NEEDS_VALUE = { empty:false, not_empty:false, equals:true, not_equals:true, contains:true, gt:true, lt:true };

  let cfg = null; // {storageKey, fields:[{key,label,type}], getYears(row), onChange()}
  let fieldsByKey = {};
  let panelRules = [];
  let editingId = null;

  function escapeHtml(s){
    return String(s === null || s === undefined ? '' : s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function isEmpty(v){ return v === null || v === undefined || v === ''; }

  function loadRules(){
    try{
      const raw = localStorage.getItem(cfg.storageKey);
      const arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr : [];
    }catch(e){ return []; }
  }

  function saveRules(rules){
    try{ localStorage.setItem(cfg.storageKey, JSON.stringify(rules)); }
    catch(e){ alert('No se pudo guardar la configuración en este navegador.'); }
  }

  function genId(){ return 'k' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }

  function getFieldValue(row, fdef){
    return fdef.type === 'years' ? cfg.getYears(row) : row[fdef.key];
  }

  function evalRule(row, rule){
    const fdef = fieldsByKey[rule.field];
    if(!fdef) return false;
    const raw = getFieldValue(row, fdef);
    switch(rule.operator){
      case 'empty': return isEmpty(raw);
      case 'not_empty': return !isEmpty(raw);
      case 'equals': return !isEmpty(raw) && String(raw).trim().toLowerCase() === String(rule.value || '').trim().toLowerCase();
      case 'not_equals': return isEmpty(raw) || String(raw).trim().toLowerCase() !== String(rule.value || '').trim().toLowerCase();
      case 'contains': return !isEmpty(raw) && String(raw).toLowerCase().indexOf(String(rule.value || '').toLowerCase()) !== -1;
      case 'gt': return !isEmpty(raw) && Number(raw) > Number(rule.value);
      case 'lt': return !isEmpty(raw) && Number(raw) < Number(rule.value);
      default: return false;
    }
  }

  function describeRule(rule){
    const fdef = fieldsByKey[rule.field];
    const label = fdef ? fdef.label : rule.field;
    const ops = OPERATORS_BY_TYPE[fdef ? fdef.type : 'text'];
    const opLabel = (ops.filter(function(o){ return o[0] === rule.operator; })[0] || [])[1] || rule.operator;
    return NEEDS_VALUE[rule.operator] ? (label + ' ' + opLabel + ' "' + rule.value + '"') : (label + ' ' + opLabel);
  }

  // ---------- integración con renderKPIs() del informe ----------
  function apply(ctx){
    if(!cfg) return;
    loadRules().forEach(function(rule){
      const key = 'custom_' + rule.id;
      ctx.sets[key] = ctx.rows.filter(function(r){ return evalRule(r, rule); });
      ctx.cardDefs.push({
        key: key,
        sev: rule.severity,
        title: rule.title,
        subtitle: rule.subtitle || describeRule(rule),
        modalTitle: rule.title,
        custom: true
      });
    });
  }

  // ---------- panel ----------
  function fieldOptionsHtml(selected){
    return cfg.fields.map(function(f){
      return '<option value="' + escapeHtml(f.key) + '"' + (f.key === selected ? ' selected' : '') + '>' + escapeHtml(f.label) + '</option>';
    }).join('');
  }

  function operatorOptionsHtml(fieldKey, selected){
    const fdef = fieldsByKey[fieldKey] || cfg.fields[0];
    const ops = OPERATORS_BY_TYPE[fdef.type] || OPERATORS_BY_TYPE.text;
    return ops.map(function(o){
      return '<option value="' + o[0] + '"' + (o[0] === selected ? ' selected' : '') + '>' + o[1] + '</option>';
    }).join('');
  }

  function openPanel(){
    panelRules = loadRules();
    editingId = null;
    renderPanel();
  }

  function renderPanel(){
    const prev = document.getElementById('customKpiOverlay');
    if(prev) prev.remove();

    const editing = editingId ? panelRules.filter(function(r){ return r.id === editingId; })[0] : null;
    const defaultField = cfg.fields[0].key;

    const listHtml = panelRules.length ? panelRules.map(function(r){
      return '<div class="note-box" style="margin-bottom:10px;display:flex;align-items:flex-start;justify-content:space-between;gap:14px;">' +
        '<div>' +
          '<div style="font:400 14.5px \'DM Sans\',sans-serif;">' + escapeHtml(r.title) + ' <span class="tag-dup">Personalizado</span></div>' +
          '<div class="note-text" style="margin-top:4px;">' + escapeHtml(r.subtitle || describeRule(r)) + '</div>' +
        '</div>' +
        '<div style="display:flex;gap:8px;flex-shrink:0;">' +
          '<button class="btn-ghost" type="button" data-edit="' + r.id + '">Editar</button>' +
          '<button class="btn-ghost" type="button" data-del="' + r.id + '">Eliminar</button>' +
        '</div>' +
      '</div>';
    }).join('') : '<p class="note-text" style="margin-bottom:14px;">Todavía no agregaste ningún indicador personalizado.</p>';

    const formHtml =
      '<div id="customKpiForm" style="border-top:1px solid var(--line);padding-top:18px;margin-top:6px;">' +
        '<div style="font:400 14.5px \'DM Sans\',sans-serif;margin-bottom:12px;">' + (editing ? 'Editar indicador' : 'Nuevo indicador') + '</div>' +
        '<div class="filter-group" style="margin-bottom:12px;"><label>Título</label><input type="text" id="ckTitle" value="' + escapeHtml(editing ? editing.title : '') + '" placeholder="Ej: Documentos en estado Borrador"></div>' +
        '<div class="filter-group" style="margin-bottom:12px;"><label>Subtítulo (opcional)</label><input type="text" id="ckSubtitle" value="' + escapeHtml(editing ? (editing.subtitle || '') : '') + '" placeholder="Si lo dejas vacío se genera uno automático"></div>' +
        '<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:12px;">' +
          '<div class="filter-group"><label>Campo</label><select id="ckField">' + fieldOptionsHtml(editing ? editing.field : defaultField) + '</select></div>' +
          '<div class="filter-group"><label>Condición</label><select id="ckOperator">' + operatorOptionsHtml(editing ? editing.field : defaultField, editing ? editing.operator : 'empty') + '</select></div>' +
          '<div class="filter-group" id="ckValueWrap"><label>Valor</label><input type="text" id="ckValue" value="' + escapeHtml(editing ? (editing.value || '') : '') + '"></div>' +
          '<div class="filter-group"><label>Severidad</label><select id="ckSeverity">' +
            ['problem', 'warn', 'info'].map(function(s){ return '<option value="' + s + '"' + ((editing ? editing.severity : 'warn') === s ? ' selected' : '') + '>' + SEVERITY_LABEL[s] + '</option>'; }).join('') +
          '</select></div>' +
        '</div>' +
        '<div style="display:flex;gap:10px;">' +
          '<button class="btn-primary" type="button" id="ckSave">Guardar</button>' +
          (editing ? '<button class="btn-ghost" type="button" id="ckCancel">Cancelar edición</button>' : '') +
        '</div>' +
      '</div>';

    const html =
      '<div class="modal-overlay" id="customKpiOverlay">' +
        '<div class="modal-card">' +
          '<div class="modal-head">' +
            '<div>' +
              '<div class="modal-title">Indicadores personalizados</div>' +
              '<div class="modal-sub">Agrega indicadores con una condición simple sobre un campo. Para reglas más complejas (cruces entre varios campos, duplicados, fechas futuras) pide el cambio a quien mantiene este informe.</div>' +
            '</div>' +
            '<button class="modal-close" type="button" id="ckClose" aria-label="Cerrar">&times;</button>' +
          '</div>' +
          '<div class="modal-body" style="padding:22px 26px;">' + listHtml + formHtml + '</div>' +
          '<div class="modal-foot">' +
            '<button class="btn-ghost" type="button" id="ckExport">Exportar configuración (.json)</button>' +
            '<button class="btn-ghost" type="button" id="ckImport">Importar configuración (.json)</button>' +
            '<input type="file" id="ckImportFile" accept="application/json" style="display:none">' +
            '<button class="btn-primary" type="button" id="ckDone">Listo</button>' +
          '</div>' +
        '</div>' +
      '</div>';

    document.body.insertAdjacentHTML('beforeend', html);
    wirePanel();
  }

  function wirePanel(){
    const overlay = document.getElementById('customKpiOverlay');

    function close(){ overlay.remove(); document.removeEventListener('keydown', onKey); }
    function onKey(e){ if(e.key === 'Escape') close(); }
    overlay.addEventListener('click', function(e){ if(e.target === overlay) close(); });
    document.addEventListener('keydown', onKey);
    document.getElementById('ckClose').addEventListener('click', close);
    document.getElementById('ckDone').addEventListener('click', close);

    function toggleValueField(){
      const op = document.getElementById('ckOperator').value;
      document.getElementById('ckValueWrap').style.display = NEEDS_VALUE[op] ? '' : 'none';
    }
    document.getElementById('ckField').addEventListener('change', function(){
      document.getElementById('ckOperator').innerHTML = operatorOptionsHtml(this.value, null);
      toggleValueField();
    });
    document.getElementById('ckOperator').addEventListener('change', toggleValueField);
    toggleValueField();

    document.querySelectorAll('[data-edit]').forEach(function(btn){
      btn.addEventListener('click', function(){ editingId = btn.dataset.edit; renderPanel(); });
    });
    document.querySelectorAll('[data-del]').forEach(function(btn){
      btn.addEventListener('click', function(){
        if(!confirm('¿Eliminar este indicador personalizado?')) return;
        panelRules = panelRules.filter(function(r){ return r.id !== btn.dataset.del; });
        saveRules(panelRules);
        if(editingId === btn.dataset.del) editingId = null;
        renderPanel();
        if(cfg.onChange) cfg.onChange();
      });
    });
    const cancelBtn = document.getElementById('ckCancel');
    if(cancelBtn) cancelBtn.addEventListener('click', function(){ editingId = null; renderPanel(); });

    document.getElementById('ckSave').addEventListener('click', function(){
      const title = document.getElementById('ckTitle').value.trim();
      const field = document.getElementById('ckField').value;
      const operator = document.getElementById('ckOperator').value;
      const value = document.getElementById('ckValue').value.trim();
      const severity = document.getElementById('ckSeverity').value;
      const subtitle = document.getElementById('ckSubtitle').value.trim();

      if(!title){ alert('Escribe un título para el indicador.'); return; }
      if(NEEDS_VALUE[operator] && !value){ alert('Escribe un valor para esta condición.'); return; }

      const rule = { id: editingId || genId(), title: title, subtitle: subtitle, field: field, operator: operator, value: value, severity: severity };
      panelRules = editingId
        ? panelRules.map(function(r){ return r.id === editingId ? rule : r; })
        : panelRules.concat([rule]);

      saveRules(panelRules);
      editingId = null;
      renderPanel();
      if(cfg.onChange) cfg.onChange();
    });

    document.getElementById('ckExport').addEventListener('click', function(){
      const blob = new Blob([JSON.stringify(panelRules, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'indicadores_personalizados_' + new Date().toISOString().slice(0, 10) + '.json';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    });

    const importInput = document.getElementById('ckImportFile');
    document.getElementById('ckImport').addEventListener('click', function(){ importInput.click(); });
    importInput.addEventListener('change', function(e){
      const file = e.target.files[0];
      if(!file) return;
      const reader = new FileReader();
      reader.onload = function(ev){
        try{
          const arr = JSON.parse(ev.target.result);
          if(!Array.isArray(arr)) throw new Error('formato inválido');
          if(!confirm('Esto reemplaza tus indicadores personalizados actuales por los del archivo. ¿Continuar?')) return;
          panelRules = arr;
          saveRules(panelRules);
          editingId = null;
          renderPanel();
          if(cfg.onChange) cfg.onChange();
        }catch(err){
          alert('No se pudo leer el archivo de configuración. Verifica que sea un .json exportado desde este mismo panel.');
        }
      };
      reader.readAsText(file);
      importInput.value = '';
    });
  }

  function init(options){
    cfg = options;
    fieldsByKey = {};
    cfg.fields.forEach(function(f){ fieldsByKey[f.key] = f; });
  }

  function mount(buttonId){
    const btn = document.getElementById(buttonId);
    if(btn) btn.addEventListener('click', openPanel);
  }

  window.CustomKPIs = { init: init, mount: mount, apply: apply };
})();
