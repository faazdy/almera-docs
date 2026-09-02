// Empaqueta un .html de presentación en un único archivo autocontenido:
// reemplaza cada token {{ruta}} por un data: URI leído de ./marca/<ruta>.
// Debe vivir junto a la carpeta marca/ (o sea, en assets/).
//
//   node empaquetar-html.js  [entrada.src.html]  [salida.html]
//
// Rutas relativas a assets/. Por defecto usa el ejemplo:
//   ejemplos-generados/html/ejemplo-gestion-integral.src.html
//     ->  ejemplos-generados/html/ejemplo-gestion-integral.html
const fs = require('fs');
const path = require('path');

const DIR   = __dirname;
const MARCA = path.join(DIR, 'marca');
const SRC   = path.join(DIR, process.argv[2] || 'ejemplos-generados/html/ejemplo-gestion-integral.src.html');
const OUT   = path.join(DIR, process.argv[3] || 'ejemplos-generados/html/ejemplo-gestion-integral.html');

const MIME = { '.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.png':'image/png', '.svg':'image/svg+xml' };

let html = fs.readFileSync(SRC, 'utf8');
html = html.replace(/\{\{([^}]+)\}\}/g, (_, rel) => {
  const file = path.join(MARCA, rel.trim());
  const buf  = fs.readFileSync(file);
  const mime = MIME[path.extname(file).toLowerCase()] || 'application/octet-stream';
  return `data:${mime};base64,${buf.toString('base64')}`;
});

fs.writeFileSync(OUT, html);
console.log('OK ->', OUT, '(' + (html.length / 1024 / 1024).toFixed(2) + ' MB)');
