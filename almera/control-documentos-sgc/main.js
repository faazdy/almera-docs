(function(){
  "use strict";

  // ---------- estado ----------
  let rawData = [];
  let filtered = [];
  let charts = {};
  let currentPage = 1;
  const PAGE_SIZE = 50;
  let sortState = { col: '_fechaUltimaActualizacion', dir: 'desc' };
  let ageField = 'ultimaActualizacion'; // 'ultimaActualizacion' | 'elaboracion'

  const PALETTE = ['#eb5a25','#2563eb','#7c3aed','#16a34a','#f59e0b','#0891b2','#db2777','#64748b','#84cc16','#e11d48'];

  const uploadZone = document.getElementById('uploadZone');
  const fileInput = document.getElementById('fileInput');
  const LIBS_OK = (typeof XLSX !== 'undefined') && (typeof Chart !== 'undefined');

  if(!LIBS_OK){
    uploadZone.innerHTML =
      '<div class="upload-title lib-error">No se pudieron cargar los componentes necesarios.</div>' +
      '<div class="upload-sub">Falta la carpeta "vendor" junto a este archivo (xlsx.full.min.js / chart.umd.min.js). Vuelve a descargar la herramienta completa, sin separar el index.html de su carpeta.</div>';
    uploadZone.style.cursor = 'default';
  }

  // ---------- resolución de columnas (encabezados con saltos de línea / espacios inconsistentes) ----------
  function normKey(s){
    return String(s == null ? '' : s)
      .toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]/g, '');
  }

  // Mapa: nombre lógico -> columna real detectada en el archivo cargado
  let COL = {};

  function resolveColumns(cols){
    const norm = cols.map(function(c){ return { raw: c, n: normKey(c) }; });
    function findExact(target){
      const hit = norm.filter(function(x){ return x.n === target; });
      return hit.length ? hit[0].raw : null;
    }
    function findStarts(prefix){
      const hit = norm.filter(function(x){ return x.n.indexOf(prefix) === 0; });
      return hit.length ? hit[0].raw : null;
    }
    function findIncludesAll(){
      const needles = Array.prototype.slice.call(arguments);
      const hit = norm.filter(function(x){ return needles.every(function(nd){ return x.n.indexOf(nd) !== -1; }); });
      return hit.length ? hit[0].raw : null;
    }

    const map = {
      proceso: findExact('proceso'),
      subproceso: findExact('subproceso'),
      tipo: findExact('tipodedocumento'),
      codigo: findExact('codigodeldocumento'),
      nombre: findExact('nombredeldocumento'),
      estado: findExact('estadodeldocumento'),
      seguimiento: findExact('seguimientoalestadodeldocumento'),
      fechaElaboracion: findStarts('fechadeelaboracion'),
      fechaUltimaActualizacion: findStarts('fechaultima'),
      fechaDerogacion: findStarts('fechadederogacion'),
      versionInicial: findIncludesAll('version', 'inicial'),
      ultimaVersionCompleta: findExact('ultimaversiondeldocumento'),
      ultimaVersion: findExact('ultimaversion'),
      observacion: findExact('observacion'),
      cargoElaboracion: findExact('cargodelresponsabledelaelaboracion'),
      cargoAprobacion: findExact('cargodelresponsabledelaaprobacion'),
      profesionalDEP: findIncludesAll('nombreprofesional'),
      cons: findExact('cons'),
    };

    // "Requiere actualización" puede aparecer en más de una vigencia (ej. Feb 2024/2025 y 2026).
    // Usamos la más reciente (la que menciona el año más alto) como campo de referencia.
    const reqCols = norm.filter(function(x){ return x.n.indexOf('requiereactualizacion') !== -1; });
    reqCols.sort(function(a, b){
      const ya = (a.n.match(/\d{4}/) || [0])[0];
      const yb = (b.n.match(/\d{4}/) || [0])[0];
      return Number(yb) - Number(ya);
    });
    map.requiereActualizacion = reqCols.length ? reqCols[0].raw : null;

    // Columnas de "Fecha N Actualización" (histórico de versiones, formato ancho)
    map.fechasActualizacionHistorico = norm.filter(function(x){ return /^fecha\d+actualizacion/.test(x.n); }).map(function(x){ return x.raw; });

    return map;
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

  function clean(v){
    if(v === null || v === undefined) return '';
    return String(v).trim();
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
    const d = ageField === 'elaboracion' ? row._fechaElaboracion : row._fechaUltimaActualizacion;
    return d ? (new Date() - d) / (1000*60*60*24*365.25) : null;
  }

  // Normaliza el campo libre "Requiere Actualización" a un bucket manejable.
  function requiereBucket(v){
    const s = clean(v).toLowerCase();
    if(!s) return 'Sin dato';
    if(s.indexOf('derogado') === 0) return 'Derogado';
    if(s.indexOf('si') === 0 || s.indexOf('sí') === 0) return 'SI';
    if(s.indexOf('no') === 0) return 'NO';
    return 'Otro';
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
    row._proceso = clean(COL.proceso ? row[COL.proceso] : '') || null;
    row._subproceso = clean(COL.subproceso ? row[COL.subproceso] : '') || null;
    row._tipo = clean(COL.tipo ? row[COL.tipo] : '');
    // normaliza casing (ej. "procedimiento" vs "Procedimiento")
    row._tipoNorm = row._tipo ? row._tipo.charAt(0).toUpperCase() + row._tipo.slice(1).toLowerCase() : null;
    row._codigo = clean(COL.codigo ? row[COL.codigo] : '') || null;
    row._nombre = clean(COL.nombre ? row[COL.nombre] : '') || null;
    row._estado = clean(COL.estado ? row[COL.estado] : '') || null;
    row._observacion = clean(COL.observacion ? row[COL.observacion] : '') || null;
    row._fechaElaboracion = parseDate(COL.fechaElaboracion ? row[COL.fechaElaboracion] : null);
    row._fechaUltimaActualizacion = parseDate(COL.fechaUltimaActualizacion ? row[COL.fechaUltimaActualizacion] : null) || row._fechaElaboracion;
    row._fechaDerogacion = parseDate(COL.fechaDerogacion ? row[COL.fechaDerogacion] : null);
    row._requiereRaw = COL.requiereActualizacion ? row[COL.requiereActualizacion] : null;
    row._requiereBucket = requiereBucket(row._requiereRaw);
    row._numActualizaciones = COL.fechasActualizacionHistorico.filter(function(c){ return row[c] !== null && row[c] !== undefined && row[c] !== ''; }).length;
    row._sinCodigo = !row._codigo;
    row._esDerogado = row._estado === 'Derogado';
    row._esVigente = row._estado === 'Vigente';
    row._derogadoSinFecha = row._esDerogado && !row._fechaDerogacion;
    return row;
  }

  function computeDuplicateCodes(rows){
    const counts = {};
    rows.forEach(function(r){
      if(r._codigo) counts[r._codigo] = (counts[r._codigo] || 0) + 1;
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
        'Código': r._codigo,
        'Nombre': r._nombre,
        'Proceso': r._proceso,
        'SubProceso': r._subproceso,
        'Tipo de documento': r._tipoNorm,
        'Estado': r._estado,
        'Fecha de elaboración': formatDate(r._fechaElaboracion),
        'Fecha última actualización': formatDate(r._fechaUltimaActualizacion),
        'Requiere actualización': r._requiereBucket,
        'Antigüedad': ageBucketLabel(getRowYears(r)),
        'Observación': r._observacion,
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
    XLSX.writeFile(wb, 'control_documentos_sgc_' + safe + '_' + new Date().toISOString().slice(0,10) + '.xlsx');
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
        '<td>' + escapeHtml(r._codigo || '—') + (r._codigoDuplicado ? '<span class="tag-dup">duplicado</span>' : '') + '</td>' +
        '<td class="wrap">' + escapeHtml(r._nombre || '—') + '</td>' +
        '<td class="wrap">' + escapeHtml(r._proceso || '—') + '</td>' +
        '<td>' + escapeHtml(r._estado || '—') + '</td>' +
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
            '<thead><tr><th>Código</th><th>Nombre</th><th>Proceso</th><th>Estado</th><th>Antigüedad</th></tr></thead>' +
            '<tbody>' + (rowsHtml || '<tr><td colspan="5" style="color:var(--ink-faint);padding:24px;text-align:center;">Sin resultados.</td></tr>') + '</tbody>' +
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

  // ---------- render: KPIs (clicables) ----------
  function renderKPIs(){
    const total = filtered.length;
    const totalAll = rawData.length;
    document.getElementById('kpiScope').innerHTML = (total === totalAll)
      ? 'Mostrando <strong>todos</strong> los ' + totalAll + ' registros del listado. Haz clic en cualquier indicador para ver el detalle.'
      : 'Mostrando <strong>' + total + '</strong> de ' + totalAll + ' registros (filtros activos). Haz clic en cualquier indicador para ver el detalle.';

    const vigentes = filtered.filter(function(r){ return r._esVigente; });

    const sets = {
      sincodigo: filtered.filter(function(r){ return r._sinCodigo; }),
      duplicados: filtered.filter(function(r){ return r._codigoDuplicado; }).slice().sort(function(a,b){
        return String(a._codigo||'').localeCompare(String(b._codigo||''));
      }),
      requiereact: vigentes.filter(function(r){ return r._requiereBucket === 'SI'; }),
      antiguedad2: vigentes.filter(function(r){ const y = getRowYears(r); return y !== null && y > 2; }),
      derogadosinfecha: filtered.filter(function(r){ return r._derogadoSinFecha; }),
    };

    const SEV = {
      problem: { dot:'#b7472a', label:'Requiere acción' },
      warn:    { dot:'#c08a1e', label:'Atención' },
      info:    { dot:'var(--muted-soft)', label:'Informativo' }
    };

    const pct = function(n){ return total ? (n/total*100).toFixed(1).replace('.', ',') + '%' : '0,0%'; };

    const cardDefs = [
      { key:'sincodigo',        sev:'problem', title:'Sin código asignado', subtitle:'Campo Código vacío', modalTitle:'Documentos sin código asignado' },
      { key:'duplicados',       sev:'problem', title:'Códigos duplicados', subtitle:'Mismo código repetido', modalTitle:'Documentos con código duplicado' },
      { key:'requiereact',      sev:'warn',    title:'Vigentes marcados para actualizar', subtitle:'Campo "Requiere actualización" = Sí', modalTitle:'Documentos vigentes marcados para actualizar' },
      { key:'antiguedad2',      sev:'warn',    title:'Vigentes con más de 2 años sin tocar', subtitle:'Sin revisión reciente (' + (ageField === 'elaboracion' ? 'Fecha de elaboración' : 'Fecha última actualización') + ')', modalTitle:'Documentos vigentes con más de 2 años de antigüedad' },
      { key:'derogadosinfecha', sev:'info',    title:'Derogados sin fecha de derogación', subtitle:'Dato faltante en el listado', modalTitle:'Documentos derogados sin fecha de derogación' },
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
    renderDonut('chartEstado', groupCount(filtered, '_estado'), '_estado', 'Estado');
    renderDonut('chartTipo', groupCount(filtered, '_tipoNorm'), '_tipoNorm', 'Tipo de documento');
    renderHBar('chartProceso', topN(groupCount(filtered, '_proceso'), 10), '_proceso', 'Proceso');
    renderHBar('chartSubproceso', topN(groupCount(filtered, '_subproceso'), 10), '_subproceso', 'SubProceso');

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
    rawData.forEach(function(r){ if(r._codigoDuplicado) dupCodesSet.add(r._codigo); });
    const dupRows = rawData.filter(function(r){ return r._codigoDuplicado; }).length;
    const sinCodigo = rawData.filter(function(r){ return r._sinCodigo; }).length;
    const derogadosSinFecha = rawData.filter(function(r){ return r._derogadoSinFecha; }).length;
    const derogados = rawData.filter(function(r){ return r._esDerogado; }).length;
    const derogadosSinObs = rawData.filter(function(r){ return r._esDerogado && !r._observacion; }).length;
    const tipoVariants = {};
    rawData.forEach(function(r){ if(r._tipo) tipoVariants[r._tipo] = (tipoVariants[r._tipo] || 0) + 1; });
    const tipoNormCount = new Set(Object.keys(tipoVariants).map(function(t){ return t.toLowerCase(); })).size;
    const tipoRawCount = Object.keys(tipoVariants).length;
    const reqVariants = new Set();
    rawData.forEach(function(r){ if(r._requiereRaw) reqVariants.add(clean(r._requiereRaw)); });

    const items = [];

    items.push({
      type: dupCodesSet.size > 0 ? 'warn' : 'good',
      text: dupCodesSet.size > 0
        ? '<strong>' + dupCodesSet.size + ' códigos</strong> están duplicados entre varios registros (' + dupRows + ' filas afectadas en total). Puede tratarse de un documento derogado y su reemplazo compartiendo el mismo código, o de un duplicado real por revisar.'
        : 'No se encontraron códigos duplicados.'
    });

    if(sinCodigo > 0){
      items.push({ type:'warn', text: '<strong>' + sinCodigo + ' registros</strong> (' + (sinCodigo/total*100).toFixed(1) + '%) no tienen código asignado.' });
    }

    if(derogadosSinFecha > 0){
      items.push({ type:'warn', text: '<strong>' + derogadosSinFecha + ' documento(s) derogados</strong> no tienen registrada su fecha de derogación en el listado.' });
    }

    items.push({ type:'note', text: 'De los <strong>' + derogados + ' documentos derogados</strong>, ' + derogadosSinObs + ' (' + (derogados ? (derogadosSinObs/derogados*100).toFixed(0) : 0) + '%) no tienen una observación registrada explicando el motivo.' });

    if(tipoRawCount > tipoNormCount){
      items.push({ type:'note', text: 'El campo <strong>Tipo de documento</strong> trae ' + tipoRawCount + ' variantes de texto que se agrupan en ' + tipoNormCount + ' categorías reales al normalizar mayúsculas/minúsculas (ej. "procedimiento" vs "Procedimiento"). El gráfico "Por tipo de documento" ya usa la versión normalizada.' });
    }

    if(reqVariants.size > 6){
      items.push({ type:'note', text: 'El campo <strong>Requiere actualización</strong> es texto libre y trae ' + reqVariants.size + ' variantes distintas en este archivo (comentarios, fechas, "para derogar", etc.). Para los gráficos y filtros se agrupó en cuatro categorías: Sí / No / Derogado / En gestión (otro texto).' });
    }

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
    if(key === '_fechaUltimaActualizacion') return row._fechaUltimaActualizacion ? row._fechaUltimaActualizacion.getTime() : -Infinity;
    if(key === '_antiguedad'){ const y = getRowYears(row); return (y === null) ? -Infinity : y; }
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
      return '<tr>' +
        '<td>' + escapeHtml(r._codigo || '—') + (r._codigoDuplicado ? '<span class="tag-dup">duplicado</span>' : '') + '</td>' +
        '<td class="wrap">' + escapeHtml(r._nombre || '—') + '</td>' +
        '<td class="wrap">' + escapeHtml(r._proceso || '—') + '</td>' +
        '<td class="wrap">' + escapeHtml(r._subproceso || '—') + '</td>' +
        '<td>' + escapeHtml(r._tipoNorm || '—') + '</td>' +
        '<td>' + escapeHtml(r._estado || '—') + '</td>' +
        '<td>' + formatDate(r._fechaUltimaActualizacion) + '</td>' +
        '<td>' + escapeHtml(r._requiereBucket) + '</td>' +
        '<td><span class="age-dot ' + dot + '"></span>' + bucket + '</td>' +
      '</tr>';
    }).join('');

    document.getElementById('tableCount').textContent = sorted.length.toLocaleString('es-CO') + ' registros';
    renderPagination(totalPages);
  }

  // ---------- filtros ----------
  function getFilterValues(){
    return {
      estado: document.getElementById('fEstado').value,
      tipo: document.getElementById('fTipo').value,
      proceso: document.getElementById('fProceso').value,
      subproceso: document.getElementById('fSubproceso').value,
      requiere: document.getElementById('fRequiere').value,
      bucket: document.getElementById('fAntiguedad').value,
      search: document.getElementById('fSearch').value.trim().toLowerCase(),
    };
  }

  function applyFilters(){
    const f = getFilterValues();
    filtered = rawData.filter(function(r){
      if(f.estado && r._estado !== f.estado) return false;
      if(f.tipo && r._tipoNorm !== f.tipo) return false;
      if(f.proceso && r._proceso !== f.proceso) return false;
      if(f.subproceso && r._subproceso !== f.subproceso) return false;
      if(f.requiere && r._requiereBucket !== f.requiere) return false;
      if(f.bucket && ageBucketLabel(getRowYears(r)) !== f.bucket) return false;
      if(f.search){
        const hay = String(r._nombre || '').toLowerCase().indexOf(f.search) !== -1 ||
                    String(r._codigo || '').toLowerCase().indexOf(f.search) !== -1;
        if(!hay) return false;
      }
      return true;
    });
    currentPage = 1;
    renderKPIs();
    renderCharts();
    renderTable();
  }

  function resetFilterControls(){
    ['fEstado','fTipo','fProceso','fSubproceso','fRequiere','fAntiguedad'].forEach(function(id){
      document.getElementById(id).value = '';
    });
    document.getElementById('fSearch').value = '';
  }

  function populateFilterOptions(){
    fillSelect('fEstado', uniqueSorted(rawData, '_estado'), 'Todos');
    fillSelect('fTipo', uniqueSorted(rawData, '_tipoNorm'), 'Todos');
    fillSelect('fProceso', uniqueSorted(rawData, '_proceso'), 'Todos');
    fillSelect('fSubproceso', uniqueSorted(rawData, '_subproceso'), 'Todas');
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
        // El archivo trae varias hojas de apoyo (pivotes, hojas sueltas); la lista fila-a-fila
        // suele ser la primera hoja o una llamada "LISTADO_MAESTRO".
        const preferred = wb.SheetNames.filter(function(n){ return /listado.?maestro/i.test(n); })[0];
        const sheetName = preferred || wb.SheetNames[0];
        const sheet = wb.Sheets[sheetName];
        json = XLSX.utils.sheet_to_json(sheet, { defval: null });
      }catch(err){
        console.error('Error leyendo el Excel:', err);
        alert('No se pudo leer el archivo. Verifica que sea un Excel (.xlsx/.xls) válido y que no esté dañado o protegido con contraseña.\n\nDetalle técnico: ' + err.message);
        return;
      }

      if(!json || !json.length){
        alert('El archivo se leyó correctamente pero no tiene filas de datos.');
        return;
      }

      // --- Paso 2: resolver columnas y validar que sea el listado correcto ---
      const cols = Object.keys(json[0]);
      COL = resolveColumns(cols);
      const missingLabels = [];
      if(!COL.nombre) missingLabels.push('Nombre del Documento');
      if(!COL.codigo) missingLabels.push('Codigo _del documento');
      if(!COL.estado) missingLabels.push('Estado del documento');
      if(!COL.proceso && !COL.subproceso) missingLabels.push('Proceso / SubProceso');
      if(missingLabels.length){
        alert('Este archivo no parece ser el Listado Maestro de Control de Documentos del SGC.\n\n' +
              'No se encontraron columnas equivalentes a: ' + missingLabels.join(', ') + '.\n\n' +
              'Sube el archivo tal como se consolida en la carpeta compartida, sin renombrar sus encabezados.');
        return;
      }

      // --- Paso 3: procesar y renderizar (errores aquí no significan archivo inválido) ---
      try{
        rawData = json.map(processRow).filter(function(r){ return r._nombre || r._codigo; });
        const dupSet = computeDuplicateCodes(rawData);
        rawData.forEach(function(r){ r._codigoDuplicado = r._codigo ? dupSet.has(r._codigo) : false; });
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
  ['fEstado','fTipo','fProceso','fSubproceso','fRequiere','fAntiguedad'].forEach(function(id){
    document.getElementById(id).addEventListener('change', applyFilters);
  });
  document.getElementById('fSearch').addEventListener('input', debounce(applyFilters, 250));

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
