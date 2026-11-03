#!/usr/bin/env node
/*
 * Convierte un documento Markdown de docs/ en PDF con la identidad de SABIA.
 *
 *   node docs/generar-pdf.js docs/05-corte-2026-11-03.md [salida.pdf]
 *
 * Sin la salida, el PDF queda junto al .md con el mismo nombre. Para los cortes,
 * el nombre que se publica es SABIA-corte-AAAA-MM-DD.pdf (se pasa como segundo argumento).
 *
 * - Markdown → HTML con el mismo marked del chat (rag/static/vendor/marked.min.js).
 * - HTML → PDF con Edge o Chrome en modo headless (sin dependencias de npm).
 *   Para usar otro navegador: variable de entorno BROWSER con la ruta del ejecutable.
 * - Las fuentes (DM Sans, JetBrains Mono) se descargan de Google Fonts y se incrustan.
 *   Sin internet, el PDF sale con las fuentes del sistema (y lo avisa).
 * - KEEP_HTML=1 conserva el HTML intermedio para revisarlo en el navegador.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { pathToFileURL } = require('url');

const REPO = path.resolve(__dirname, '..');
const { marked } = require(path.join(REPO, 'rag', 'static', 'vendor', 'marked.min.js'));

const BROWSERS = [
  process.env.BROWSER,
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].filter(Boolean);

const CSS = `
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
:root { --ink:#171614; --soft:#4a4743; --muted:#8a857d; --line:#e4dfd6; --bg:#faf8f4; --accent:#eb5a25; --code:#f3efe8; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin:0; font: 400 9.6pt/1.5 "DM Sans", "Segoe UI", Arial, sans-serif; color: var(--ink); }
.kicker { font: 500 7.5pt/1 "JetBrains Mono", Consolas, monospace; letter-spacing:.08em; text-transform:uppercase; color: var(--accent); margin: 0 0 10pt; }
h1 { font-weight:500; font-size:22pt; line-height:1.15; letter-spacing:-.02em; margin:0 0 12pt; padding-bottom:12pt; border-bottom:2px solid var(--ink); }
h2 { font-weight:500; font-size:14pt; letter-spacing:-.01em; margin:20pt 0 8pt; padding-top:4pt; break-after:avoid; }
h3 { font-weight:500; font-size:11pt; margin:14pt 0 6pt; break-after:avoid; }
h4 { font-weight:500; font-size:10pt; margin:12pt 0 4pt; break-after:avoid; }
p { margin: 0 0 7pt; }
ul, ol { margin: 0 0 8pt; padding-left: 16pt; }
li { margin: 1.5pt 0; }
li > ul, li > ol { margin: 2pt 0; }
a { color: var(--ink); text-decoration: underline; text-decoration-color: var(--accent); text-underline-offset: 2px; }
strong { font-weight: 600; }
hr { border: 0; border-top: 1px solid var(--line); margin: 16pt 0 4pt; }
code { font: 400 8.2pt "JetBrains Mono", Consolas, monospace; background: var(--code); padding: 0 3pt; border-radius: 2pt; }
pre { background: var(--code); padding: 8pt 9pt; border-radius: 3pt; margin: 0 0 9pt; overflow: hidden; break-inside: avoid; }
pre code { background: none; padding: 0; font-family: "Cascadia Mono", Consolas, monospace; font-size: 7pt; line-height: 1.2; white-space: pre; }
table { width: 100%; border-collapse: collapse; margin: 2pt 0 10pt; font-size: 8.4pt; line-height: 1.4; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { text-align: left; font-weight: 600; border-bottom: 1.5px solid var(--ink); padding: 4pt 6pt 4pt 0; vertical-align: bottom; }
td { border-bottom: 1px solid var(--line); padding: 4pt 6pt 4pt 0; vertical-align: top; }
td code, th code { font-size: 7.6pt; }
blockquote { margin: 0 0 9pt; padding: 6pt 10pt; border-left: 3px solid var(--accent); background: var(--bg); color: var(--soft); }
input[type=checkbox] { margin: 0 4pt 0 -12pt; vertical-align: -1pt; }
li:has(> input[type=checkbox]) { list-style: none; }
.foot { margin-top: 22pt; padding-top: 8pt; border-top: 1px solid var(--line); font: 400 7.5pt "JetBrains Mono", Consolas, monospace; color: var(--muted); display:flex; justify-content:space-between; }
`;

function findBrowser() {
  const found = BROWSERS.find((p) => fs.existsSync(p));
  if (!found) throw new Error('No encontré Edge ni Chrome. Define BROWSER con la ruta del navegador.');
  return found;
}

/*
 * Descarga DM Sans y JetBrains Mono y las incrusta en el HTML: el navegador headless
 * imprime antes de que terminen de cargar las fuentes web. Usa también los certificados
 * de Windows, porque la red corporativa inspecciona TLS con un certificado propio.
 */
async function fontsCss() {
  const tls = require('tls');
  if (tls.setDefaultCACertificates && tls.getCACertificates) {
    tls.setDefaultCACertificates([...tls.getCACertificates('default'), ...tls.getCACertificates('system')]);
  }
  const ua = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36' };
  try {
    const css = await (await fetch(FONTS_URL, { headers: ua })).text();
    // Solo los subconjuntos latinos: el resto (cirílico, vietnamita…) no se usa
    const blocks = css.split(/(?=\/\* )/).filter((b) => /^\/\* latin(-ext)? \*\//.test(b));
    if (!blocks.length) throw new Error('respuesta inesperada de Google Fonts');
    const out = [];
    for (const block of blocks) {
      const url = block.match(/url\((https:[^)]+)\)/)[1];
      const font = Buffer.from(await (await fetch(url)).arrayBuffer()).toString('base64');
      out.push(block.replace(url, `data:font/woff2;base64,${font}`));
    }
    return out.join('\n');
  } catch (err) {
    console.warn(`Aviso: no se pudieron descargar las fuentes (${err.cause?.code || err.message}); se usan las del sistema.`);
    return '';
  }
}

const FONTS_URL = 'https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=block';

function render(mdPath, fonts) {
  const md = fs.readFileSync(mdPath, 'utf8');
  const title = (md.match(/^#\s+(.+)$/m) || [, path.basename(mdPath, '.md')])[1].replace(/^\d+\.\s*/, '');
  const body = marked.parse(md, { gfm: true });
  const today = new Date().toISOString().slice(0, 10);
  return `<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>SABIA — ${title}</title>
<style>${fonts}\n${CSS}</style></head>
<body>
<div class="kicker">SABIA · Calidad · Capital Salud</div>
${body}
<div class="foot"><span>almera-docs/docs/${path.basename(mdPath)}</span><span>Generado ${today}</span></div>
</body></html>`;
}

async function main() {
  const [input, output] = process.argv.slice(2);
  if (!input) {
    console.error('Uso: node docs/generar-pdf.js <documento.md> [salida.pdf]');
    process.exit(1);
  }
  const mdPath = path.resolve(input);
  const pdfPath = path.resolve(output || mdPath.replace(/\.md$/i, '.pdf'));
  const htmlPath = path.join(os.tmpdir(), `sabia-${process.pid}.html`);
  fs.writeFileSync(htmlPath, render(mdPath, await fontsCss()), 'utf8');

  try {
    execFileSync(findBrowser(), [
      '--headless=new',
      '--disable-gpu',
      '--no-first-run',
      '--no-pdf-header-footer',
      '--virtual-time-budget=5000', // espera a que el navegador decodifique las fuentes incrustadas
      `--print-to-pdf=${pdfPath}`,
      pathToFileURL(htmlPath).href,
    ], { stdio: 'ignore' });
  } finally {
    if (!process.env.KEEP_HTML) fs.rmSync(htmlPath, { force: true });
    else console.log(`HTML intermedio: ${htmlPath}`);
  }
  if (!fs.existsSync(pdfPath)) throw new Error('El navegador no generó el PDF.');
  console.log(`PDF: ${path.relative(process.cwd(), pdfPath)} (${Math.round(fs.statSync(pdfPath).size / 1024)} KB)`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
