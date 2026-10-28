(function(){
  "use strict";

  // Nav general del sitio SABIA (diseño 1c "Círculo con hairline"): botón circular
  // de 44px que abre un menú a pantalla completa en oscuro. Un solo archivo
  // compartido (sin build, sin dependencias) incluido con
  // <script src=".../assets/nav.js" data-base="...">, donde data-base es la ruta
  // relativa de vuelta a la raíz del repo desde la página que lo carga.
  //
  // Dónde se monta el botón: en un elemento [data-sabnav] si la página lo tiene;
  // si no, se agrega al final del header (.m-header / .site-header); y si no hay
  // header, queda fijo arriba a la derecha.
  //
  // A propósito NO se incluye en almera/informe-documentos/ ni en
  // almera/control-documentos-sgc/: esas dos carpetas son herramientas
  // autocontenidas que se distribuyen por separado (ver docs/02-informes.md).

  var scriptEl = document.currentScript;
  var BASE = (scriptEl && scriptEl.getAttribute('data-base')) || './';

  // Columna 01: accesos grandes. "asistente/" la sirve el servidor de rag/ junto
  // con el sitio; con un servidor estático solo (npx serve, Pages) ese enlace da 404.
  var HOME = [
    { label: 'SABIA', desc: 'Centro de recursos', href: 'index.html' },
    { label: 'Pregúntale a SABIA', desc: 'Asistente de Almera', href: 'asistente/' }
  ];

  var GROUPS = [
    { num: '02', title: 'Almera · Documentación', wide: true, items: [
      { label: 'Visión general', href: 'almera/index.html' },
      { label: 'Gestión documental', href: 'almera/modulo-documentos/gestion-documentos/index.html' },
      { label: 'Mapa de procesos', href: 'almera/modulo-documentos/mapa-procesos/index.html' },
      { label: 'Mecanismos de integración', href: 'almera/modulo-documentos/mecanismos-integracion/index.html' },
      { label: 'Modelos de gestión', href: 'almera/modulo-documentos/modelos-gestion/index.html' },
      { label: 'Evaluaciones', href: 'almera/modulo-evaluaciones/evaluaciones/index.html' },
      { label: 'Indicadores', href: 'almera/modulo-evaluaciones/indicadores/index.html' },
      { label: 'Planes de mejora', href: 'almera/modulo-evaluaciones/planes-de-mejora/index.html' },
      { label: 'Proyectos', href: 'almera/modulo-proyectos/index.html' },
      { label: 'Códigos de estructura organizacional', href: 'almera/codigos-estructura-organizacional/index.html' },
      { label: 'Habilidades de IA (Almera)', href: 'almera/almera-IA/index.html' }
    ]},
    { num: '03', title: 'Agentes de IA · Calidad', items: [
      { label: 'Visión general', href: 'calidad-ai-agents/index.html' },
      { label: 'Entregables (habilidades)', href: 'calidad-ai-agents/entregables/index.html' }
    ]},
    { num: '04', title: 'Herramientas · Informes', items: [
      { label: 'Informe de documentos Almera', href: 'almera/informe-documentos/index.html' },
      { label: 'Control de documentos del SGC', href: 'almera/control-documentos-sgc/index.html' }
    ]}
  ];

  function escapeHtml(s){
    return String(s === null || s === undefined ? '' : s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function resolveHref(href){
    return BASE + href;
  }

  function isCurrent(href){
    try{
      var target = new URL(resolveHref(href), location.href);
      var norm = function(p){ return p.replace(/\/index\.html$/, '/'); };
      return norm(target.pathname) === norm(location.pathname);
    }catch(e){ return false; }
  }

  function injectStyles(){
    var light = 'rgba(250,249,247,';
    var css =
      // botón (estado cerrado)
      '.sabnav-btn{width:44px;height:44px;flex:0 0 44px;border-radius:50%;border:1px solid rgba(23,22,20,.16);' +
      'background:transparent;cursor:pointer;position:relative;padding:0;transition:border-color .25s ease;}' +
      '.sabnav-btn:hover{border-color:rgba(23,22,20,.4);}' +
      '.sabnav-btn:focus-visible{outline:2px solid #eb5a25;outline-offset:3px;}' +
      '.sabnav-btn i{position:absolute;left:14px;right:14px;height:1px;background:#171614;transition:top .3s ease,transform .3s ease,background .25s ease;}' +
      '.sabnav-btn i:first-child{top:18px;}.sabnav-btn i:last-child{top:24px;}' +
      '.sabnav-btn.sabnav-fixed{position:fixed;top:20px;right:20px;z-index:1200;background:#faf9f7;box-shadow:0 4px 14px rgba(23,22,20,.1);}' +
      '.sabnav-right{display:flex;align-items:center;gap:22px;}' +
      '[data-sabnav]{display:flex;}' +
      // botón dentro del menú (estado abierto → X)
      '.sabnav-close{position:absolute;border-color:' + light + '.28);}' +
      '.sabnav-close:hover{border-color:' + light + '.6);}' +
      '.sabnav-close i{background:#faf9f7;}' +
      '.sabnav-ov.sabnav-open .sabnav-close i{top:21px;}' +
      '.sabnav-ov.sabnav-open .sabnav-close i:first-child{transform:rotate(45deg);}' +
      '.sabnav-ov.sabnav-open .sabnav-close i:last-child{transform:rotate(-45deg);}' +
      // menú a pantalla completa
      '.sabnav-ov{position:fixed;inset:0;z-index:1300;background:#17161a;color:#faf9f7;overflow-y:auto;' +
      'opacity:0;visibility:hidden;transition:opacity .35s ease,visibility 0s linear .35s;' +
      '-webkit-font-smoothing:antialiased;font-family:"DM Sans","Helvetica Neue",Helvetica,sans-serif;}' +
      '.sabnav-ov.sabnav-open{opacity:1;visibility:visible;transition:opacity .35s ease;}' +
      '.sabnav-ov a{color:inherit;text-decoration:none;}' +
      '.sabnav-eyebrow{position:absolute;display:flex;align-items:center;gap:9px;font:500 10.5px/1 "JetBrains Mono",monospace;' +
      'letter-spacing:.14em;text-transform:uppercase;color:#8a8579;}' +
      '.sabnav-dot{width:5px;height:5px;border-radius:50%;background:#eb5a25;flex:0 0 auto;}' +
      '.sabnav-meta{position:absolute;font:500 10.5px/1 "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:#8a8579;}' +
      '.sabnav-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr) minmax(0,1fr);gap:56px;align-items:start;' +
      'padding-bottom:56px;opacity:0;transform:translateY(12px);transition:opacity .45s ease .08s,transform .45s ease .08s;}' +
      '.sabnav-ov.sabnav-open .sabnav-grid{opacity:1;transform:none;}' +
      '.sabnav-col{display:flex;flex-direction:column;gap:44px;}' +
      '.sabnav-block{display:flex;flex-direction:column;gap:18px;}' +
      '.sabnav-kicker{font:500 10px/1 "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:' + light + '.4);}' +
      '.sabnav-big{display:flex;align-items:center;gap:12px;font:300 34px/1.08 "DM Sans",sans-serif;letter-spacing:-.03em;color:#faf9f7;transition:opacity .2s ease;}' +
      '.sabnav-big:hover{opacity:.75;}' +
      '.sabnav-big .sabnav-dot{width:6px;height:6px;}' +
      '.sabnav-big.sabnav-small{font-size:24px;}' +
      '.sabnav-big.sabnav-small .sabnav-dot{background:' + light + '.35);}' +
      '.sabnav-big.sabnav-current .sabnav-dot{background:#eb5a25;}' +
      '.sabnav-desc{font:400 13px/1.4 "DM Sans",sans-serif;color:' + light + '.45);margin-top:-8px;}' +
      '.sabnav-list{display:flex;flex-direction:column;border-top:1px solid ' + light + '.12);}' +
      '.sabnav-list.sabnav-wide{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px;}' +
      '.sabnav-link{display:flex;align-items:baseline;justify-content:space-between;gap:12px;padding:11px 0;' +
      'border-bottom:1px solid ' + light + '.12);font:400 15px/1.3 "DM Sans",sans-serif;color:' + light + '.82);' +
      'transition:color .2s ease,padding .3s ease;}' +
      '.sabnav-link:hover{color:#faf9f7;padding-left:6px;}' +
      '.sabnav-arrow{font:400 10.5px/1 "JetBrains Mono",monospace;color:' + light + '.3);flex:0 0 auto;}' +
      '.sabnav-link.sabnav-current{color:#faf9f7;}' +
      '.sabnav-link.sabnav-current .sabnav-arrow{width:5px;height:5px;border-radius:50%;background:#eb5a25;font-size:0;transform:translateY(-2px);}' +
      'html.sabnav-lock{overflow:hidden;}' +
      '@media (max-width:980px){.sabnav-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:44px 40px;}' +
      '.sabnav-grid > .sabnav-col:nth-child(2){grid-column:1 / -1;grid-row:2;}}' +
      '@media (max-width:640px){.sabnav-grid{grid-template-columns:minmax(0,1fr);gap:40px;}' +
      '.sabnav-grid > .sabnav-col:nth-child(2){grid-row:auto;}' +
      '.sabnav-list.sabnav-wide{grid-template-columns:minmax(0,1fr);}' +
      '.sabnav-big{font-size:28px;}.sabnav-big.sabnav-small{font-size:21px;}' +
      '.sabnav-meta{display:none;}' +
      '.sabnav-right > :not([data-sabnav]){display:none;}' +
      '.sabnav-btn.sabnav-fixed{top:14px;right:14px;}}' +
      '@media (prefers-reduced-motion:reduce){.sabnav-ov,.sabnav-grid,.sabnav-btn i{transition:none !important;}}';
    var style = document.createElement('style');
    style.setAttribute('data-sabnav-style', ''); // no "data-sabnav": ese es el slot del botón
    style.textContent = css;
    document.head.appendChild(style);
  }

  function linkAttrs(href){
    var current = isCurrent(href);
    return {
      href: escapeHtml(resolveHref(href)),
      cls: current ? ' sabnav-current' : '',
      aria: current ? ' aria-current="page"' : ''
    };
  }

  function buildHomeHtml(){
    var blocks = HOME.map(function(item, i){
      var a = linkAttrs(item.href);
      return '<div class="sabnav-block">' +
        (i === 0 ? '<span class="sabnav-kicker">01 · Inicio</span>' : '') +
        '<a class="sabnav-big' + (i ? ' sabnav-small' : '') + a.cls + '" href="' + a.href + '"' + a.aria + '>' +
          '<span class="sabnav-dot"></span>' + escapeHtml(item.label) + '</a>' +
        '<span class="sabnav-desc">' + escapeHtml(item.desc) + '</span>' +
      '</div>';
    }).join('');
    return '<div class="sabnav-col">' + blocks + '</div>';
  }

  function buildGroupHtml(group){
    var links = group.items.map(function(item){
      var a = linkAttrs(item.href);
      return '<a class="sabnav-link' + a.cls + '" href="' + a.href + '"' + a.aria + '>' +
        escapeHtml(item.label) + '<span class="sabnav-arrow">→</span></a>';
    }).join('');
    return '<div class="sabnav-block">' +
      '<span class="sabnav-kicker">' + group.num + ' · ' + escapeHtml(group.title) + '</span>' +
      '<div class="sabnav-list' + (group.wide ? ' sabnav-wide' : '') + '">' + links + '</div>' +
    '</div>';
  }

  function buildMenuHtml(){
    var wide = GROUPS.filter(function(g){ return g.wide; });
    var rest = GROUPS.filter(function(g){ return !g.wide; });
    return buildHomeHtml() +
      '<div class="sabnav-col">' + wide.map(buildGroupHtml).join('') + '</div>' +
      '<div class="sabnav-col">' + rest.map(buildGroupHtml).join('') + '</div>';
  }

  function lines(){ return '<i></i><i></i>'; }

  function findSlot(){
    var slot = document.querySelector('[data-sabnav]');
    if(slot){ return slot; }
    var header = document.querySelector('header.m-header, header.site-header');
    if(!header){ return null; }
    // Agrupa lo que ya estaba a la derecha del header (enlace "volver", nav) con el botón
    var right = document.createElement('div');
    right.className = 'sabnav-right';
    if(header.children.length > 1){ right.appendChild(header.lastElementChild); }
    slot = document.createElement('span');
    slot.setAttribute('data-sabnav', '');
    right.appendChild(slot);
    header.appendChild(right);
    header.style.alignItems = 'center';
    return slot;
  }

  function render(){
    injectStyles();

    var slot = findSlot();
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'sabnav-btn' + (slot ? '' : ' sabnav-fixed');
    btn.setAttribute('aria-label', 'Abrir menú del sitio');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = lines();

    var overlay = document.createElement('div');
    overlay.className = 'sabnav-ov';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Menú del sitio');
    overlay.innerHTML =
      '<div class="sabnav-eyebrow"><span class="sabnav-dot"></span>Capital Salud · SGC</div>' +
      '<span class="sabnav-meta">SABIA</span>' +
      '<button type="button" class="sabnav-btn sabnav-close" aria-label="Cerrar menú">' + lines() + '</button>' +
      '<nav class="sabnav-grid">' + buildMenuHtml() + '</nav>';

    if(slot){ slot.appendChild(btn); } else { document.body.appendChild(btn); }
    document.body.appendChild(overlay);

    var closeBtn = overlay.querySelector('.sabnav-close');
    var eyebrow = overlay.querySelector('.sabnav-eyebrow');
    var meta = overlay.querySelector('.sabnav-meta');
    var grid = overlay.querySelector('.sabnav-grid');

    // Calca la posición del botón y del eyebrow de la página para que, al abrir,
    // el header se quede quieto y solo cambie el fondo (como en el diseño).
    function layout(){
      var vw = document.documentElement.clientWidth;
      var r = btn.getBoundingClientRect();
      var visible = r.bottom > 0 && r.top < window.innerHeight && r.width > 0;
      var top = visible ? r.top : 20;
      var right = visible ? vw - r.right : 20;
      var pageEyebrow = document.querySelector('header .eyebrow');
      var er = pageEyebrow && pageEyebrow.getBoundingClientRect();
      var left = er && er.width && er.bottom > 0 ? er.left : Math.max(right, Math.min(56, vw * 0.06));
      if(pageEyebrow){
        eyebrow.innerHTML = '<span class="sabnav-dot"></span>' + escapeHtml(pageEyebrow.textContent.trim());
      }

      closeBtn.style.top = top + 'px';
      closeBtn.style.right = right + 'px';
      eyebrow.style.top = (top + 22 - 5) + 'px';
      eyebrow.style.left = left + 'px';
      meta.style.top = eyebrow.style.top;
      meta.style.right = (right + 44 + 20) + 'px';
      grid.style.padding = (top + 44 + 48) + 'px ' + right + 'px 56px ' + left + 'px';
    }

    function open(){
      layout();
      overlay.scrollTop = 0;
      document.documentElement.classList.add('sabnav-lock');
      overlay.classList.add('sabnav-open');
      btn.setAttribute('aria-expanded', 'true');
      document.addEventListener('keydown', onKey);
      window.addEventListener('resize', layout);
      closeBtn.focus({ preventScroll: true });
    }
    function close(){
      overlay.classList.remove('sabnav-open');
      document.documentElement.classList.remove('sabnav-lock');
      btn.setAttribute('aria-expanded', 'false');
      document.removeEventListener('keydown', onKey);
      window.removeEventListener('resize', layout);
      btn.focus({ preventScroll: true });
    }
    function onKey(e){ if(e.key === 'Escape') close(); }

    btn.addEventListener('click', open);
    closeBtn.addEventListener('click', close);
  }

  if(document.body){
    render();
  }else{
    document.addEventListener('DOMContentLoaded', render);
  }
})();
