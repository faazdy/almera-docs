(function(){
  "use strict";

  // ---------- estado ----------
  let rawData = [];
  let filtered = [];
  let charts = {};
  let currentPage = 1;
  const PAGE_SIZE = 50;
  let sortState = { col: '_fechaModificacion', dir: 'desc' };
  let ageField = 'Fecha modificación';

  const ageFieldMap = {
    'Fecha modificación': '_fechaModificacion',
    'Fecha documento': '_fechaDocumento',
    'Fecha creación': '_fechaCreacion',
  };

  const KNOWN_EXT = ['pdf','docx','doc','xlsx','xls','xlsm','xlsb','pptx','ppt','jpg','jpeg','png','url','zip','rtf'];
  const PALETTE = ['#eb5a25','#2563eb','#7c3aed','#16a34a','#f59e0b','#0891b2','#db2777','#64748b','#84cc16','#e11d48'];
  const REQUIRED_COLS = ['Nombre','Asociado a'];
  let hasClasificacion = true;

  const uploadZone = document.getElementById('uploadZone');
  const fileInput = document.getElementById('fileInput');
  const LIBS_OK = (typeof XLSX !== 'undefined') && (typeof Chart !== 'undefined');

  if(!LIBS_OK){
    uploadZone.innerHTML =
      '<div class="upload-title lib-error">No se pudieron cargar los componentes necesarios.</div>' +
      '<div class="upload-sub">Falta la carpeta "vendor" junto a este archivo (xlsx.full.min.js / chart.umd.min.js). Vuelve a descargar la herramienta completa, sin separar el index.html de su carpeta.</div>';
    uploadZone.style.cursor = 'default';
  }

  // ---------- helpers generales ----------
  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function formatDate(d){
    if(!d) return '—';
    const dd = String(d.getDate()).padStart(2,'0');
    const mm = String(d.getMonth()+1).padStart(2,'0');
    const yy = d.getFullYear();
    return dd + '/' + mm + '/' + yy;
  }

  function parseDate(v){
    if(v === null || v === undefined || v === '') return null;
    if(v instanceof Date) return isNaN(v.getTime()) ? null : v;
    if(typeof v === 'number'){
      try{
        const d = XLSX.SSF.parse_date_code(v);
        if(!d) return null;
        return new Date(d.y, d.m - 1, d.d);
      }catch(e){ return null; }
    }
    if(typeof v === 'string'){
      const s = v.trim();
      const m = s.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
      if(m){
        const day = Number(m[1]), month = Number(m[2]), year = Number(m[3]);
        if(month < 1 || month > 12 || day < 1 || day > 31) return null;
        const d = new Date(year, month - 1, day);
        return isNaN(d.getTime()) ? null : d;
      }
      const d = new Date(s);
      return isNaN(d.getTime()) ? null : d;
    }
    return null;
  }

  function extractExt(v){
    if(!v) return 'sin archivo';
    const parts = String(v).split(/[,;\n]/).map(function(s){ return s.trim(); }).filter(Boolean);
    const first = parts[0] || '';
    const m = first.match(/\.([A-Za-z0-9]+)\s*$/);
    if(m && KNOWN_EXT.indexOf(m[1].toLowerCase()) !== -1) return m[1].toLowerCase();
    return 'otro';
  }

  function ageBucketLabel(years){
    if(years === null || years === undefined) return 'Sin fecha';
    if(years < 0.5) return '< 6 meses';
    if(years < 1) return '6 meses - 1 año';
    if(years < 2) return '1 - 2 años';
    if(years < 3) return '2 - 3 años';
    return '> 3 años';
  }

  function ageDotClass(years){
    if(years === null || years === undefined) return 'gray';
    if(years < 1) return 'green';
    if(years < 2) return 'yellow';
    return 'red';
  }

  function getRowYears(row){
    const d = row[ageFieldMap[ageField]];
    return d ? (new Date() - d) / (1000*60*60*24*365.25) : null;
  }

  function debounce(fn, ms){
    let t;
    return function(){
      const args = arguments;
      clearTimeout(t);
      t = setTimeout(function(){ fn.apply(null, args); }, ms);
    };
  }

  function processRow(row){
    const fc = parseDate(row['Fecha creación']);
    const fd = parseDate(row['Fecha documento']);
    const fm = parseDate(row['Fecha modificación']);
    const ext = extractExt(row['Nombres archivos']);
    row._fechaCreacion = fc;
    row._fechaDocumento = fd;
    row._fechaModificacion = fm;
    row._extension = ext;
    row._esPDF = ext === 'pdf';
    row._sinArchivo = !row['Nombres archivos'];
    row._sinCodigo = !row['Código'];
    return row;
  }

  function computeDuplicateCodes(rows){
    const counts = {};
    rows.forEach(function(r){
      if(r['Código']) counts[r['Código']] = (counts[r['Código']] || 0) + 1;
    });
    const dup = new Set();
    Object.keys(counts).forEach(function(k){ if(counts[k] > 1) dup.add(k); });
    return dup;
  }

  function uniqueSorted(rows, key){
    const set = new Set();
    rows.forEach(function(r){ if(r[key]) set.add(r[key]); });
    return Array.from(set).sort(function(a,b){ return String(a).localeCompare(String(b), 'es'); });
  }

  function fillSelect(id, values, placeholder){
    const sel = document.getElementById(id);
    const current = sel.value;
    sel.innerHTML = '<option value="">' + placeholder + '</option>' +
      values.map(function(v){ return '<option value="' + escapeHtml(v) + '">' + escapeHtml(v) + '</option>'; }).join('');
    sel.value = current;
  }

  function groupCount(rows, key){
    const m = {};
    rows.forEach(function(r){
      const v = r[key] || 'Sin dato';
      m[v] = (m[v] || 0) + 1;
    });
    return m;
  }

  function topN(map, n){
    return Object.entries(map).sort(function(a,b){ return b[1]-a[1]; }).slice(0, n);
  }

  function destroyChart(id){
    if(charts[id]){ charts[id].destroy(); delete charts[id]; }
  }

  // ---------- exportar a Excel ----------
  function buildExportRows(rows){
    return rows.map(function(r){
      return {
        'ID': r['ID'],
        'Código': r['Código'],
        'Nombre': r['Nombre'],
        'Clasificación': r['Clasificación'],
        'Tipo': r['Tipo'],
        'Clase': r['Clase'],
        'Proceso / Subproceso': r['Asociado a'],
        'Emisor': r['Emisor'],
        'Estado': r['Estado'],
        'Versión': r['Versión'],
        'Fecha documento': formatDate(r._fechaDocumento),
        'Fecha modificación': formatDate(r._fechaModificacion),
        'Antigüedad': ageBucketLabel(getRowYears(r)),
        'Archivo': r['Nombres archivos'],
      };
    });
  }

  function exportRows(rows, hint){
    if(!rows.length) return;
    const ws = XLSX.utils.json_to_sheet(buildExportRows(rows));
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Documentos');
    const safe = String(hint || 'informe').toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 40) || 'informe';
    XLSX.writeFile(wb, 'informe_documentos_' + safe + '_' + new Date().toISOString().slice(0,10) + '.xlsx');
  }

  // ---------- modal de detalle ----------
  function openDetailModal(title, rows){
    const CAP = 300;
    const capped = rows.slice(0, CAP);

    const rowsHtml = capped.map(function(r){
      const y = getRowYears(r);
      const dot = ageDotClass(y);
      const bucket = ageBucketLabel(y);
      return '<tr>' +
        '<td>' + (r['ID'] !== null && r['ID'] !== undefined ? r['ID'] : '—') + '</td>' +
        '<td>' + escapeHtml(r['Código'] || '—') + (r._codigoDuplicado ? '<span class="tag-dup">duplicado</span>' : '') + '</td>' +
        '<td class="wrap">' + escapeHtml(r['Nombre'] || '—') + '</td>' +
        '<td class="wrap">' + escapeHtml(r['Asociado a'] || '—') + '</td>' +
        '<td>' + escapeHtml(r['Clase'] || '—') + '</td>' +
        '<td><span class="age-dot ' + dot + '"></span>' + bucket + '</td>' +
      '</tr>';
    }).join('');

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML =
      '<div class="modal-card">' +
        '<div class="modal-head">' +
          '<div>' +
            '<div class="modal-title">' + escapeHtml(title) + '</div>' +
            '<div class="modal-sub">' + rows.length.toLocaleString('es-CO') + ' documento(s)' + (rows.length > CAP ? ' — mostrando los primeros ' + CAP : '') + '</div>' +
          '</div>' +
          '<button class="modal-close" type="button" aria-label="Cerrar">&times;</button>' +
        '</div>' +
        '<div class="modal-body">' +
          '<table class="data-table modal-table">' +
            '<thead><tr><th>ID</th><th>Código</th><th>Nombre</th><th>Proceso / Subproceso</th><th>Clase</th><th>Antigüedad</th></tr></thead>' +
            '<tbody>' + (rowsHtml || '<tr><td colspan="6" style="color:var(--ink-faint);padding:24px;text-align:center;">Sin resultados.</td></tr>') + '</tbody>' +
          '</table>' +
        '</div>' +
        '<div class="modal-foot">' +
          '<button class="btn-ghost" id="modalExportBtn" type="button">Exportar esta lista (.xlsx)</button>' +
          '<button class="btn-primary" id="modalCloseBtn2" type="button">Cerrar</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);

    function close(){
      overlay.remove();
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e){ if(e.key === 'Escape') close(); }

    overlay.addEventListener('click', function(e){ if(e.target === overlay) close(); });
    overlay.querySelector('.modal-close').addEventListener('click', close);
    overlay.querySelector('#modalCloseBtn2').addEventListener('click', close);
    overlay.querySelector('#modalExportBtn').addEventListener('click', function(){ exportRows(rows, title); });
    document.addEventListener('keydown', onKey);
  }

  // ---------- render: KPIs (minimalismo, clicables) ----------
  function renderKPIs(){
    const total = filtered.length;
    const totalAll = rawData.length;
    document.getElementById('kpiScope').innerHTML = (total === totalAll)
      ? 'Mostrando <strong>todos</strong> los ' + totalAll + ' registros del listado. Haz clic en cualquier indicador para ver el detalle.'
      : 'Mostrando <strong>' + total + '</strong> de ' + totalAll + ' registros (filtros activos). Haz clic en cualquier indicador para ver el detalle.';

    const sets = {
      sincodigo: filtered.filter(function(r){ return r._sinCodigo; }),
      duplicados: filtered.filter(function(r){ return r._codigoDuplicado; }).slice().sort(function(a,b){
        return String(a['Código']||'').localeCompare(String(b['Código']||''));
      }),
      sinarchivo: filtered.filter(function(r){ return r._sinArchivo; }),
      antiguedad2: filtered.filter(function(r){ const y = getRowYears(r); return y !== null && y > 2; }),
      pdf: filtered.filter(function(r){ return r._esPDF; }),
    };

    const SEV = {
      problem: { dot:'#b7472a', label:'Requiere acción' },
      warn:    { dot:'#c08a1e', label:'Atención' },
      info:    { dot:'var(--muted-soft)', label:'Informativo' }
    };

    const pct = function(n){ return total ? (n/total*100).toFixed(1).replace('.', ',') + '%' : '0,0%'; };

    const cardDefs = [
      { key:'sincodigo',   sev:'problem', title:'Sin código asignado', subtitle:'Campo Código vacío', modalTitle:'Documentos sin código asignado' },
      { key:'duplicados',  sev:'problem', title:'Códigos duplicados', subtitle:'Mismo código repetido', modalTitle:'Documentos con código duplicado' },
      { key:'sinarchivo',  sev:'problem', title:'Sin archivo adjunto', subtitle:'Campo Nombres archivos vacío', modalTitle:'Documentos sin archivo adjunto' },
      { key:'antiguedad2', sev:'warn',    title:'Más de 2 años de antigüedad', subtitle:'Sin revisión reciente (' + ageField + ')', modalTitle:'Documentos con más de 2 años de antigüedad (' + ageField + ')' },
      { key:'pdf',         sev:'info',    title:'Cargados como PDF', subtitle:'Sin edición en línea', modalTitle:'Documentos cargados como PDF' },
    ];

    const cards = cardDefs.map(function(c){
      const n = sets[c.key].length;
      return Object.assign({}, c, {
        dot: SEV[c.sev].dot,
        valueFmt: n.toLocaleString('es-CO'),
        pctStr: pct(n),
        width: total ? (n/total*100).toFixed(2) + '%' : '0%'
      });
    });

    const legendHtml = Object.keys(SEV).map(function(k){
      return '<span class="kpi-legend-item"><span class="kpi-legend-dot" style="background:' + SEV[k].dot + '"></span>' + SEV[k].label + '</span>';
    }).join('');

    document.getElementById('kpiGrid').innerHTML =
      '<div class="kpi-summary">' +
        '<div class="kpi-summary-total">' +
          '<span class="kpi-summary-value">' + total.toLocaleString('es-CO') + '</span>' +
          '<span class="kpi-summary-label">registros totales</span>' +
        '</div>' +
        '<div class="kpi-legend">' + legendHtml + '</div>' +
      '</div>' +
      '<div class="kpi-list">' +
        cards.map(function(c){
          return '<button type="button" class="kpi-row" data-kpi="' + c.key + '">' +
            '<span class="kpi-row-value-wrap">' +
              '<span class="kpi-row-dot" style="background:' + c.dot + '" title="' + c.title + '"></span>' +
              '<span class="kpi-row-value">' + c.valueFmt + '</span>' +
            '</span>' +
            '<span class="kpi-row-text">' +
              '<span class="kpi-row-title">' + c.title + '</span>' +
              '<span class="kpi-row-subtitle">' + c.subtitle + '</span>' +
            '</span>' +
            '<span class="kpi-row-pct-wrap">' +
              '<span class="kpi-row-pct">' + c.pctStr + '</span>' +
              '<span class="kpi-row-bar"><span class="kpi-row-bar-fill" style="width:' + c.width + ';background:' + c.dot + '"></span></span>' +
            '</span>' +
            '<svg class="kpi-row-chevron" width="13" height="13" viewBox="0 0 16 16" fill="none"><path d="M6 3.5L10.5 8L6 12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>' +
          '</button>';
        }).join('') +
      '</div>';

    document.querySelectorAll('#kpiGrid .kpi-row').forEach(function(btn){
      btn.addEventListener('click', function(){
        const key = btn.dataset.kpi;
        const cfg = cards.filter(function(c){ return c.key === key; })[0];
        openDetailModal(cfg.modalTitle, sets[key]);
      });
    });
  }

  // ---------- render: gráficos (clicables) ----------
  function renderDonut(canvasId, map, keyName, labelPrefix){
    const entries = Object.entries(map).sort(function(a,b){ return b[1]-a[1]; });
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId).getContext('2d');
    charts[canvasId] = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: entries.map(function(e){ return e[0]; }),
        datasets: [{ data: entries.map(function(e){ return e[1]; }), backgroundColor: PALETTE, borderWidth: 0 }]
      },
      options: {
        maintainAspectRatio: false,
        plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: { size: 11 } } } },
        onClick: function(evt, elements){
          if(!elements.length) return;
          const label = entries[elements[0].index][0];
          const rows = filtered.filter(function(r){ return (r[keyName] || 'Sin dato') === label; });
          openDetailModal(labelPrefix + ': ' + label, rows);
        }
      }
    });
  }

  function renderHBar(canvasId, entries, keyName, labelPrefix){
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId).getContext('2d');
    charts[canvasId] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: entries.map(function(e){ return e[0]; }),
        datasets: [{ data: entries.map(function(e){ return e[1]; }), backgroundColor: '#eb5a25', borderRadius: 4 }]
      },
      options: {
        indexAxis: 'y',
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { beginAtZero: true, grid: { color: '#ececec' }, ticks: { font: { size: 11 } } },
          y: { grid: { display: false }, ticks: { font: { size: 11 } } }
        },
        onClick: function(evt, elements){
          if(!elements.length) return;
          const label = entries[elements[0].index][0];
          const rows = filtered.filter(function(r){ return (r[keyName] || 'Sin dato') === label; });
          openDetailModal(labelPrefix + ': ' + label, rows);
        }
      }
    });
  }

  function renderVBarAntiguedad(labels, data){
    destroyChart('chartAntiguedad');
    const ctx = document.getElementById('chartAntiguedad').getContext('2d');
    const colors = labels.map(function(l){
      if(l === '> 3 años') return '#dc2626';
      if(l === '2 - 3 años') return '#f59e0b';
      if(l === 'Sin fecha') return '#94a3b8';
      return '#dffc3a';
    });
    charts.chartAntiguedad = new Chart(ctx, {
      type: 'bar',
      data: { labels: labels, datasets: [{ data: data, backgroundColor: colors, borderRadius: 6 }] },
      options: {
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: '#ececec' } },
          x: { grid: { display: false } }
        },
        onClick: function(evt, elements){
          if(!elements.length) return;
          const bucket = labels[elements[0].index];
          const rows = filtered.filter(function(r){ return ageBucketLabel(getRowYears(r)) === bucket; });
          openDetailModal('Antigüedad: ' + bucket, rows);
        }
      }
    });
  }

  function renderCharts(){
    renderPeriodChart();
    const clasifCard = document.getElementById('cardClasificacion');
    if(hasClasificacion){
      if(clasifCard) clasifCard.style.display = '';
      renderDonut('chartClasificacion', groupCount(filtered, 'Clasificación'), 'Clasificación', 'Clasificación');
    }else{
      destroyChart('chartClasificacion');
      if(clasifCard) clasifCard.style.display = 'none';
    }
    renderDonut('chartExtension', groupCount(filtered, '_extension'), '_extension', 'Tipo de archivo');
    renderHBar('chartProceso', topN(groupCount(filtered, 'Asociado a'), 10), 'Asociado a', 'Proceso');
    renderHBar('chartClase', topN(groupCount(filtered, 'Clase'), 10), 'Clase', 'Clase');

    const buckets = ['< 6 meses','6 meses - 1 año','1 - 2 años','2 - 3 años','> 3 años','Sin fecha'];
    const counts = {};
    buckets.forEach(function(b){ counts[b] = 0; });
    filtered.forEach(function(r){
      const y = getRowYears(r);
      counts[ageBucketLabel(y)]++;
    });
    renderVBarAntiguedad(buckets, buckets.map(function(b){ return counts[b]; }));
  }

  // ---------- render: calidad de datos ----------
  function renderDataQuality(){
    const total = rawData.length;
    const dupCodesSet = new Set();
    rawData.forEach(function(r){ if(r._codigoDuplicado) dupCodesSet.add(r['Código']); });
    const dupRows = rawData.filter(function(r){ return r._codigoDuplicado; }).length;
    const sinCodigo = rawData.filter(function(r){ return r._sinCodigo; }).length;
    const sinArchivoDocs = rawData.filter(function(r){ return r._sinArchivo && r['Tipo'] === 'Documento especifico'; }).length;
    const hoy = new Date();
    const futuros = rawData.filter(function(r){ return r._fechaDocumento && r._fechaDocumento > hoy; }).length;
    const estados = new Set(rawData.map(function(r){ return r['Estado']; }));
    const estructurales = rawData.filter(function(r){ return r['Tipo'] === 'Proceso' || r['Tipo'] === 'Subproceso'; }).length;
    const origenIgualAsociado = rawData.filter(function(r){ return r['Origen'] === r['Asociado a']; }).length;

    const items = [];

    items.push({
      type: dupCodesSet.size > 0 ? 'warn' : 'good',
      text: dupCodesSet.size > 0
        ? '<strong>' + dupCodesSet.size + ' códigos</strong> están duplicados entre varios registros (' + dupRows + ' filas afectadas en total). Vale la pena revisar si son versiones mal registradas o duplicados reales.'
        : 'No se encontraron códigos duplicados.'
    });

    items.push({
      type: 'note',
      text: '<strong>' + sinCodigo + ' registros</strong> (' + (sinCodigo/total*100).toFixed(1) + '%) no tienen código asignado en el campo Código.'
    });

    if(sinArchivoDocs > 0){
      items.push({ type:'warn', text: '<strong>' + sinArchivoDocs + ' documentos específicos</strong> no tienen ningún archivo adjunto registrado en "Nombres archivos".' });
    }

    if(futuros > 0){
      items.push({ type:'warn', text: '<strong>' + futuros + ' registro(s)</strong> tienen "Fecha documento" posterior a hoy — vale la pena revisar si es un error de digitación.' });
    }

    if(estructurales > 0){
      items.push({ type:'note', text: 'El listado incluye <strong>' + estructurales + ' filas estructurales</strong> de tipo Proceso/Subproceso (no son documentos como tal). Usa el filtro "Tipo = Documento especifico" en la tabla si quieres ver solo documentos.' });
    }

    if(estados.size === 1){
      items.push({ type:'note', text: 'Este listado solo trae registros en estado <strong>' + Array.from(estados)[0] + '</strong> — es el comportamiento por defecto del Listado Maestro de Almera. Para ver Obsoletos, Anulados o No publicados, hay que exportar sin ese filtro y volver a subir el archivo aquí.' });
    }

    items.push({ type:'note', text: 'Los campos <strong>Origen</strong> y <strong>Asociado a</strong> coinciden en el ' + (origenIgualAsociado/total*100).toFixed(0) + '% de las filas de este export — el informe usa <strong>Asociado a</strong> como el proceso/subproceso de referencia en gráficos, filtros y el modal de detalle.' });

    const TYPE_LABEL = { warn: 'Cuidado', good: 'Confirmado', note: 'Nota' };
    const TYPE_CLASS = { warn: 'is-warn', good: 'is-good', note: '' };
    document.getElementById('dqGrid').innerHTML = items.map(function(i){
      return '<div class="note-box">' +
        '<div class="note-label ' + (TYPE_CLASS[i.type] || '') + '">' + (TYPE_LABEL[i.type] || 'Nota') + '</div>' +
        '<p class="note-text">' + i.text + '</p>' +
      '</div>';
    }).join('');
  }

  // ---------- render: tabla ----------
  function sortValue(row, key){
    if(key === '_fechaDocumento') return row._fechaDocumento ? row._fechaDocumento.getTime() : -Infinity;
    if(key === '_fechaModificacion') return row._fechaModificacion ? row._fechaModificacion.getTime() : -Infinity;
    if(key === '_antiguedad'){ const y = getRowYears(row); return (y === null) ? -Infinity : y; }
    if(key === 'Versión') return row['Versión'] || 0;
    if(key === '_extension') return row._extension || '';
    return (row[key] || '').toString().toLowerCase();
  }

  function renderPagination(totalPages){
    const el = document.getElementById('pagination');
    el.innerHTML =
      '<button id="prevPage" ' + (currentPage <= 1 ? 'disabled' : '') + '>&larr; Anterior</button>' +
      '<span>Página ' + currentPage + ' de ' + totalPages + '</span>' +
      '<button id="nextPage" ' + (currentPage >= totalPages ? 'disabled' : '') + '>Siguiente &rarr;</button>';
    document.getElementById('prevPage').onclick = function(){ if(currentPage > 1){ currentPage--; renderTable(); } };
    document.getElementById('nextPage').onclick = function(){ currentPage++; renderTable(); };
  }

  function renderTable(){
    const sorted = filtered.slice().sort(function(a,b){
      const va = sortValue(a, sortState.col), vb = sortValue(b, sortState.col);
      let cmp = va < vb ? -1 : (va > vb ? 1 : 0);
      return sortState.dir === 'asc' ? cmp : -cmp;
    });

    const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
    if(currentPage > totalPages) currentPage = totalPages;
    const start = (currentPage - 1) * PAGE_SIZE;
    const pageRows = sorted.slice(start, start + PAGE_SIZE);

    document.getElementById('tableBody').innerHTML = pageRows.map(function(r){
      const y = getRowYears(r);
      const dot = ageDotClass(y);
      const bucket = ageBucketLabel(y);
      const versionTxt = (r['Versión'] !== null && r['Versión'] !== undefined && !isNaN(r['Versión'])) ? r['Versión'] : '—';
      const archivoTxt = r._extension === 'pdf'
        ? '<span class="tag-pdf">PDF</span>'
        : escapeHtml(r._extension || '—');
      return '<tr>' +
        '<td>' + escapeHtml(r['Código'] || '—') + (r._codigoDuplicado ? '<span class="tag-dup">duplicado</span>' : '') + '</td>' +
        '<td class="wrap">' + escapeHtml(r['Nombre'] || '—') + '</td>' +
        '<td>' + escapeHtml(r['Clasificación'] || '—') + '</td>' +
        '<td class="wrap">' + escapeHtml(r['Clase'] || '—') + '</td>' +
        '<td class="wrap">' + escapeHtml(r['Asociado a'] || '—') + '</td>' +
        '<td>' + escapeHtml(r['Emisor'] || '—') + '</td>' +
        '<td>' + versionTxt + '</td>' +
        '<td>' + formatDate(r._fechaDocumento) + '</td>' +
        '<td>' + formatDate(r._fechaModificacion) + '</td>' +
        '<td><span class="age-dot ' + dot + '"></span>' + bucket + '</td>' +
        '<td>' + archivoTxt + '</td>' +
      '</tr>';
    }).join('');

    document.getElementById('tableCount').textContent = sorted.length.toLocaleString('es-CO') + ' registros';
    renderPagination(totalPages);
  }

  // ---------- filtros por periodo / año ----------
  const MONTHS = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
  const PERIOD_TYPES = {
    mensual:    { size: 1, name: 'Mes' },
    bimestral:  { size: 2, name: 'Bimestre' },
    trimestral: { size: 3, name: 'Trimestre' },
    semestral:  { size: 6, name: 'Semestre' }
  };
  const DATE_PROPS = ["_fechaModificacion", "_fechaDocumento", "_fechaCreacion"];

  function periodLabel(type, i){
    const t = PERIOD_TYPES[type];
    const a = i * t.size, b = a + t.size - 1;
    if(t.size === 1) return MONTHS[a];
    return t.name + ' ' + (i + 1) + ' (' + MONTHS[a].slice(0,3) + '–' + MONTHS[b].slice(0,3) + ')';
  }

  function refreshPeriodOptions(){
    const type = document.getElementById('fPeriodType').value;
    const sel = document.getElementById('fPeriod');
    if(!type){
      sel.innerHTML = '<option value="">—</option>';
      sel.value = '';
      sel.disabled = true;
      return;
    }
    const n = 12 / PERIOD_TYPES[type].size;
    let html = '<option value="">Todos</option>';
    for(let i = 0; i < n; i++) html += '<option value="' + i + '">' + periodLabel(type, i) + '</option>';
    sel.innerHTML = html;
    sel.disabled = false;
  }

  function populateYearOptions(){
    const years = new Set();
    rawData.forEach(function(r){
      DATE_PROPS.forEach(function(p){ if(r[p]) years.add(r[p].getFullYear()); });
    });
    const list = Array.from(years).sort(function(a,b){ return b - a; });
    const sel = document.getElementById('fYear');
    sel.innerHTML = '<option value="">Todos</option>' + list.map(function(y){ return '<option value="' + y + '">' + y + '</option>'; }).join('');
  }

  function matchesPeriod(r, f){
    if(!f.year && f.period === '' && !f.from && !f.to) return true;
    const d = r[f.dateProp];
    if(!d) return false;
    if(f.year && d.getFullYear() !== Number(f.year)) return false;
    if(f.periodType && f.period !== ''){
      if(Math.floor(d.getMonth() / PERIOD_TYPES[f.periodType].size) !== Number(f.period)) return false;
    }
    if(f.from && d < new Date(f.from + 'T00:00:00')) return false;
    if(f.to && d > new Date(f.to + 'T23:59:59')) return false;
    return true;
  }

  // ---------- gráfico de barras por periodo ----------
  function renderPeriodChart(){
    const f = getFilterValues();
    const type = f.periodType || (f.year ? 'mensual' : 'anual');
    const size = type === 'anual' ? 12 : PERIOD_TYPES[type].size;
    const perYear = 12 / size;
    const short = function(i){
      if(type === 'mensual') return MONTHS[i].slice(0,3);
      return { bimestral:'Bim ', trimestral:'Trim ', semestral:'Sem ' }[type] + (i + 1);
    };

    const buckets = {};
    let sinFecha = 0, minY = Infinity, maxY = -Infinity;
    filtered.forEach(function(r){
      const d = r[f.dateProp];
      if(!d){ sinFecha++; return; }
      const y = d.getFullYear();
      const i = type === 'anual' ? 0 : Math.floor(d.getMonth() / size);
      const k = y * 100 + i;
      (buckets[k] = buckets[k] || []).push(r);
      if(y < minY) minY = y;
      if(y > maxY) maxY = y;
    });

    const labels = [], rowsByBar = [];
    if(minY !== Infinity){
      if(f.year){ minY = maxY = Number(f.year); }
      for(let y = minY; y <= maxY; y++){
        const n = type === 'anual' ? 1 : perYear;
        for(let i = 0; i < n; i++){
          labels.push(type === 'anual' ? String(y) : (f.year ? short(i) : y + ' · ' + short(i)));
          rowsByBar.push(buckets[y * 100 + i] || []);
        }
      }
    }

    const typeName = { anual:'año', mensual:'mes', bimestral:'bimestre', trimestral:'trimestre', semestral:'semestre' }[type];
    const dateLabel = document.getElementById('fDateField').selectedOptions[0].textContent;
    document.getElementById('periodChartSub').textContent =
      'Por ' + typeName + ', según «' + dateLabel + '» y los filtros activos.' +
      (sinFecha ? ' ' + sinFecha.toLocaleString('es-CO') + ' registro(s) sin esa fecha no se grafican.' : '') +
      ' Haz clic en una barra para ver sus documentos.';

    destroyChart('chartPeriodo');
    const ctx = document.getElementById('chartPeriodo').getContext('2d');
    charts.chartPeriodo = new Chart(ctx, {
      type: 'bar',
      data: { labels: labels, datasets: [{ data: rowsByBar.map(function(r){ return r.length; }), backgroundColor: '#eb5a25', borderRadius: 4 }] },
      options: {
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: '#ececec' }, ticks: { precision: 0 } },
          x: { grid: { display: false }, ticks: { font: { size: 11 }, maxRotation: 60 } }
        },
        onClick: function(evt, elements){
          if(!elements.length) return;
          const i = elements[0].index;
          openDetailModal('Periodo: ' + labels[i], rowsByBar[i]);
        }
      }
    });
  }

  // ---------- filtros ----------
  function getFilterValues(){
    return {
      clasificacion: document.getElementById('fClasificacion').value,
      tipo: document.getElementById('fTipo').value,
      proceso: document.getElementById('fProceso').value,
      clase: document.getElementById('fClase').value,
      bucket: document.getElementById('fAntiguedad').value,
      search: document.getElementById('fSearch').value.trim().toLowerCase(),
      dateProp: document.getElementById('fDateField').value,
      year: document.getElementById('fYear').value,
      periodType: document.getElementById('fPeriodType').value,
      period: document.getElementById('fPeriod').value,
      from: document.getElementById('fFrom').value,
      to: document.getElementById('fTo').value,
    };
  }

  function applyFilters(){
    const f = getFilterValues();
    filtered = rawData.filter(function(r){
      if(f.clasificacion && r['Clasificación'] !== f.clasificacion) return false;
      if(f.tipo && r['Tipo'] !== f.tipo) return false;
      if(f.proceso && r['Asociado a'] !== f.proceso) return false;
      if(f.clase && r['Clase'] !== f.clase) return false;
      if(f.bucket && ageBucketLabel(getRowYears(r)) !== f.bucket) return false;
      if(f.search){
        const hay = String(r['Nombre'] || '').toLowerCase().indexOf(f.search) !== -1 ||
                    String(r['Código'] || '').toLowerCase().indexOf(f.search) !== -1;
        if(!hay) return false;
      }
      if(!matchesPeriod(r, f)) return false;
      return true;
    });
    currentPage = 1;
    renderKPIs();
    renderCharts();
    renderTable();
  }

  function resetFilterControls(){
    ['fClasificacion','fTipo','fProceso','fClase','fAntiguedad'].forEach(function(id){
      document.getElementById(id).value = '';
    });
    document.getElementById('fSearch').value = '';
    ['fYear','fPeriodType','fFrom','fTo'].forEach(function(id){ document.getElementById(id).value = ''; });
    document.getElementById('fDateField').selectedIndex = 0;
    refreshPeriodOptions();
  }

  function populateFilterOptions(){
    populateYearOptions();
    const clasifGroup = document.getElementById('groupClasificacion');
    if(hasClasificacion){
      if(clasifGroup) clasifGroup.style.display = '';
      fillSelect('fClasificacion', uniqueSorted(rawData, 'Clasificación'), 'Todas');
    }else{
      if(clasifGroup) clasifGroup.style.display = 'none';
      document.getElementById('fClasificacion').value = '';
    }
    fillSelect('fTipo', uniqueSorted(rawData, 'Tipo'), 'Todos');
    fillSelect('fProceso', uniqueSorted(rawData, 'Asociado a'), 'Todos');
    fillSelect('fClase', uniqueSorted(rawData, 'Clase'), 'Todas');
  }

  // ---------- carga de archivo ----------
  uploadZone.addEventListener('click', function(){ if(LIBS_OK) fileInput.click(); });
  uploadZone.addEventListener('dragover', function(e){ if(!LIBS_OK) return; e.preventDefault(); uploadZone.classList.add('dragover'); });
  uploadZone.addEventListener('dragleave', function(){ uploadZone.classList.remove('dragover'); });
  uploadZone.addEventListener('drop', function(e){
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if(!LIBS_OK) return;
    if(e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener('change', function(e){
    if(e.target.files.length) handleFile(e.target.files[0]);
  });

  function showLoadedState(name, count){
    uploadZone.classList.add('loaded');
    uploadZone.innerHTML =
      '<div class="upload-loaded-row">' +
        '<div class="upload-meta">' +
          '<div class="upload-title">Archivo cargado <span class="upload-check">✓</span></div>' +
          '<div><span class="upload-filename">' + escapeHtml(name) + '</span> &nbsp;·&nbsp; <span class="upload-count">' + count.toLocaleString('es-CO') + ' registros</span></div>' +
        '</div>' +
      '</div>' +
      '<button class="btn-ghost" id="btnChangeFile" type="button">Cambiar archivo</button>';
    document.getElementById('btnChangeFile').addEventListener('click', function(ev){
      ev.stopPropagation();
      fileInput.click();
    });
  }

  function handleFile(file){
    if(!LIBS_OK){
      alert('No se pudieron cargar los componentes necesarios (XLSX/Chart.js). Verifica que la carpeta "vendor" esté junto a este archivo.');
      return;
    }

    const reader = new FileReader();
    reader.onload = function(e){

      // --- Paso 1: leer el Excel ---
      let json;
      try{
        const data = new Uint8Array(e.target.result);
        const wb = XLSX.read(data, { type:'array', cellDates:true });
        const sheet = wb.Sheets[wb.SheetNames[0]];
        json = XLSX.utils.sheet_to_json(sheet, { defval: null });
      }catch(err){
        console.error('Error leyendo el Excel:', err);
        alert('No se pudo leer el archivo. Verifica que sea un Excel (.xlsx) válido y que no esté dañado o protegido con contraseña.\n\nDetalle técnico: ' + err.message);
        return;
      }

      if(!json || !json.length){
        alert('El archivo se leyó correctamente pero no tiene filas de datos.');
        return;
      }

      // --- Paso 2: validar que sea un listado de documentos de Almera ---
      const cols = Object.keys(json[0]);
      const missing = REQUIRED_COLS.filter(function(c){ return cols.indexOf(c) === -1; });
      if(missing.length){
        alert('Este archivo no parece ser un listado de documentos de Almera.\n\n' +
              'Faltan las columnas: ' + missing.join(', ') + '.\n\n' +
              'Expórtalo desde: Gestión de calidad → Listados maestros → Listado maestro de documentos.');
        return;
      }
      hasClasificacion = cols.indexOf('Clasificación') !== -1;

      // --- Paso 3: procesar y renderizar (errores aquí no significan archivo inválido) ---
      try{
        rawData = json.map(processRow);
        const dupSet = computeDuplicateCodes(rawData);
        rawData.forEach(function(r){ r._codigoDuplicado = r['Código'] ? dupSet.has(r['Código']) : false; });
        filtered = rawData.slice();
        currentPage = 1;

        showLoadedState(file.name, rawData.length);
        resetFilterControls();
        populateFilterOptions();
        document.getElementById('dashboardContent').classList.remove('dash-hidden');

        renderKPIs();
        renderDataQuality();
        renderTable();
      }catch(err){
        console.error('Error generando indicadores/tabla:', err);
        alert('El archivo se leyó correctamente, pero ocurrió un error generando el informe. Abre la consola del navegador (F12) para más detalle y compártelo si el problema persiste.\n\nDetalle técnico: ' + err.message);
        return;
      }

      // Los gráficos van aparte: si Chart.js falla, el resto del informe ya quedó visible.
      try{
        renderCharts();
      }catch(err){
        console.error('Error generando los gráficos:', err);
        const grid = document.getElementById('graficos');
        if(grid){
          const warnDiv = document.createElement('div');
          warnDiv.className = 'note-box';
          warnDiv.style.marginBottom = '26px';
          warnDiv.innerHTML = '<div class="note-label is-warn">Cuidado</div><p class="note-text">No se pudieron generar los gráficos en este navegador. Los indicadores, la calidad de datos y la tabla de abajo siguen funcionando con normalidad.</p>';
          grid.insertBefore(warnDiv, grid.firstChild.nextSibling);
        }
      }
    };
    reader.readAsArrayBuffer(file);
  }

  // ---------- eventos: filtros ----------
  ['fClasificacion','fTipo','fProceso','fClase','fAntiguedad'].forEach(function(id){
    document.getElementById(id).addEventListener('change', applyFilters);
  });
  document.getElementById('fSearch').addEventListener('input', debounce(applyFilters, 250));
  ['fDateField','fYear','fPeriod','fFrom','fTo'].forEach(function(id){
    document.getElementById(id).addEventListener('change', applyFilters);
  });
  document.getElementById('fPeriodType').addEventListener('change', function(){
    refreshPeriodOptions();
    applyFilters();
  });

  document.getElementById('btnClearFilters').addEventListener('click', function(){
    resetFilterControls();
    applyFilters();
  });

  document.getElementById('btnExport').addEventListener('click', function(){
    exportRows(filtered, 'filtrado');
  });

  // ---------- descargar informe en PDF (impresión del navegador) ----------
  document.getElementById('btnPrintPdf').addEventListener('click', function(){
    window.print();
  });

  // ---------- eventos: antigüedad (pills) ----------
  document.querySelectorAll('#ageFieldPills .filter-pill').forEach(function(btn){
    btn.addEventListener('click', function(){
      document.querySelectorAll('#ageFieldPills .filter-pill').forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      ageField = btn.dataset.field;
      applyFilters();
    });
  });

  // ---------- eventos: orden de tabla ----------
  document.querySelectorAll('#dataTable thead th[data-key]').forEach(function(th){
    th.addEventListener('click', function(){
      const key = th.dataset.key;
      if(sortState.col === key){
        sortState.dir = sortState.dir === 'asc' ? 'desc' : 'asc';
      }else{
        sortState.col = key;
        sortState.dir = key.indexOf('_fecha') === 0 ? 'desc' : 'asc';
      }
      document.querySelectorAll('#dataTable thead th').forEach(function(t){ t.classList.remove('sorted'); });
      th.classList.add('sorted');
      renderTable();
    });
  });

})();
