let idx = 0;            // ← единая переменная‑счётчик
let list = [];
let loading = false;

async function fetchList() {
  const res = await fetch('poem-list.json');
  list = await res.json();
}

async function loadNext() {
  if (loading || idx >= list.length) return;
  loading = true;

  const { file, title, date } = list[idx++];
  const raw = await (await fetch(file)).text();
  const lines = raw.split('\n');

  // --- выдёргиваем тело стиха, учитывая, есть ли дата ---
  let bodyStart = 1;                              // по умолчанию пропускаем заголовок
  if (lines.length > 1 && /^\d{4}-\d{2}-\d{2}$/.test(lines[1].trim())) {
    bodyStart = 2;                                // есть строка‑дата → пропускаем две
  }
  const body = lines.slice(bodyStart).join('\n');

  // --- рендер ---
  const div = document.createElement('div');
  div.className = 'poem';
  div.innerHTML = `
    <h2>${title}</h2>
    ${date !== '1900-01-01' ? `<p class="date">${date}</p>` : ''}
    <pre>${body}</pre>`;
  document.getElementById('poems-container').appendChild(div);

  loading = false;
  if (idx === list.length) {
    document.getElementById('loader').innerText = 'Все стихи загружены';
    window.removeEventListener('scroll', handleScroll);
  }
}

function handleScroll() {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 300) {
    loadNext();
  }
}

window.addEventListener('DOMContentLoaded', async () => {
  await fetchList();
  loadNext();
  window.addEventListener('scroll', handleScroll);
});
