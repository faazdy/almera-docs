(function(){
  "use strict";

  // Nav general del sitio SABIA: botón flotante + panel offcanvas con todas las
  // páginas del sistema. Un solo archivo compartido (sin build, sin dependencias)
  // incluido con <script src=".../assets/nav.js" data-base="...">, donde data-base
  // es la ruta relativa de vuelta a la raíz del repo desde la página que lo carga.
  //
  // A propósito NO se incluye en almera/informe-documentos/ ni en
  // almera/control-documentos-sgc/: esas dos carpetas son herramientas
  // autocontenidas que se distribuyen por separado (ver docs/02-informes.md).

  var scriptEl = document.currentScript;
  var BASE = (scriptEl && scriptEl.getAttribute('data-base')) || './';

  var SECTIONS = [
    { title: 'Inicio', items: [
      { label: 'SABIA · Centro de recursos', href: 'index.html' }
    ]},
    { title: 'Almera · Documentación', items: [
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
    { title: 'Agentes de IA · Calidad', items: [
      { label: 'Visión general', href: 'calidad-ai-agents/index.html' },
      { label: 'Entregables (habilidades)', href: 'calidad-ai-agents/entregables/index.html' }
    ]},
    { title: 'Herramientas (informes)', items: [
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
    var css =
      '.sabnav-btn{position:fixed;top:20px;right:20px;z-index:1200;display:flex;align-items:center;gap:8px;' +
      'background:#faf9f7;color:#171614;border:1px solid rgba(23,22,20,.16);border-radius:999px;' +
      'padding:9px 16px 9px 13px;font:400 13px/1 "DM Sans",sans-serif;cursor:pointer;' +
      'box-shadow:0 4px 14px rgba(23,22,20,.1);}' +
      '.sabnav-btn:hover{border-color:rgba(23,22,20,.4);}' +
      '.sabnav-btn svg{flex-shrink:0;display:block;}' +
      '.sabnav-overlay{position:fixed;inset:0;background:rgba(23,22,20,.4);backdrop-filter:blur(2px);' +
      'z-index:1300;opacity:0;pointer-events:none;transition:opacity .18s ease;}' +
      '.sabnav-overlay.sabnav-open{opacity:1;pointer-events:auto;}' +
      '.sabnav-panel{position:fixed;top:0;left:0;height:100%;width:min(320px,86vw);background:#faf9f7;' +
      'box-shadow:0 0 40px rgba(23,22,20,.25);transform:translateX(-100%);transition:transform .2s ease;' +
      'display:flex;flex-direction:column;overflow:hidden;}' +
      '.sabnav-overlay.sabnav-open .sabnav-panel{transform:translateX(0);}' +
      '.sabnav-head{display:flex;align-items:center;justify-content:space-between;padding:20px 20px 16px;' +
      'border-bottom:1px solid rgba(23,22,20,.1);flex-shrink:0;}' +
      '.sabnav-title{font:400 14px/1 "DM Sans",sans-serif;color:#171614;display:flex;align-items:center;gap:7px;}' +
      '.sabnav-title .dot{width:5px;height:5px;border-radius:50%;background:#eb5a25;flex-shrink:0;}' +
      '.sabnav-close{background:none;border:none;font-size:20px;line-height:1;color:#a5a096;cursor:pointer;padding:2px 6px;border-radius:4px;}' +
      '.sabnav-close:hover{color:#171614;}' +
      '.sabnav-body{overflow:auto;padding:8px 14px 24px;}' +
      '.sabnav-group-title{font:500 10px/1 "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;' +
      'color:#a5a096;margin:18px 10px 6px;}' +
      '.sabnav-link{display:block;padding:9px 10px;border-radius:6px;font:400 13.5px/1.3 "DM Sans",sans-serif;' +
      'color:#3d3a34;text-decoration:none;}' +
      '.sabnav-link:hover{background:rgba(23,22,20,.05);color:#171614;}' +
      '.sabnav-link.sabnav-current{background:rgba(235,90,37,.1);color:#b7472a;font-weight:500;}' +
      '@media (max-width:640px){.sabnav-btn{padding:9px;}.sabnav-btn span{display:none;}}';
    var style = document.createElement('style');
    style.setAttribute('data-sabnav', '');
    style.textContent = css;
    document.head.appendChild(style);
  }

  function buildMenuHtml(){
    return SECTIONS.map(function(section){
      var itemsHtml = section.items.map(function(item){
        var cls = 'sabnav-link' + (isCurrent(item.href) ? ' sabnav-current' : '');
        return '<a class="' + cls + '" href="' + escapeHtml(resolveHref(item.href)) + '">' + escapeHtml(item.label) + '</a>';
      }).join('');
      return '<div class="sabnav-group-title">' + escapeHtml(section.title) + '</div>' + itemsHtml;
    }).join('');
  }

  function render(){
    injectStyles();

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'sabnav-btn';
    btn.setAttribute('aria-label', 'Abrir menú del sitio');
    btn.innerHTML =
      '<svg width="15" height="11" viewBox="0 0 15 11" fill="none"><path d="M0 1H15M0 5.5H15M0 10H15" stroke="currentColor" stroke-width="1.4"></path></svg>' +
      '<span>Menú</span>';

    var overlay = document.createElement('div');
    overlay.className = 'sabnav-overlay';
    overlay.innerHTML =
      '<div class="sabnav-panel" role="dialog" aria-label="Menú del sitio">' +
        '<div class="sabnav-head">' +
          '<span class="sabnav-title"><span class="dot"></span>SABIA · Navegación</span>' +
          '<button type="button" class="sabnav-close" aria-label="Cerrar">&times;</button>' +
        '</div>' +
        '<div class="sabnav-body">' + buildMenuHtml() + '</div>' +
      '</div>';

    document.body.appendChild(btn);
    document.body.appendChild(overlay);

    function open(){ overlay.classList.add('sabnav-open'); document.addEventListener('keydown', onKey); }
    function close(){ overlay.classList.remove('sabnav-open'); document.removeEventListener('keydown', onKey); }
    function onKey(e){ if(e.key === 'Escape') close(); }

    btn.addEventListener('click', open);
    overlay.addEventListener('click', function(e){ if(e.target === overlay) close(); });
    overlay.querySelector('.sabnav-close').addEventListener('click', close);
  }

  if(document.body){
    render();
  }else{
    document.addEventListener('DOMContentLoaded', render);
  }
})();
