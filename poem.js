function getParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

async function loadPoem() {
  const file = getParam('file');
  if (!file) return;

  const raw = await (await fetch(file)).text();
  const lines = raw.split('\n');

  const title = lines[0];
  let bodyStart = 1;

  if (
    lines.length > 1 &&
    /^\d{4}[--]\d{2}[--]\d{2}$/.test(lines[1].trim())
  ) {
    bodyStart = 2;
  }

  const body = lines.slice(bodyStart).join('\n');

  const div = document.getElementById('poem');
  div.innerHTML = `
    <h1>${title}</h1>
    <pre>${body}</pre>
  `;
}

window.addEventListener('DOMContentLoaded', loadPoem);
