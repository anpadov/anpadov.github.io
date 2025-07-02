let pointer = 0;
let list = [];
let loading = false;

async function fetchList() {
  const res = await fetch('poem-list.json');
  list = await res.json();
}

// … (list, idx, fetchList без reverse)

async function loadNext() {
  if (loading || idx >= list.length) return;
  loading = true;

  const {file, title, date} = list[idx++];
  const text = await (await fetch(file)).text();
  const body = text.split('\n').slice(2).join('\n');   // пропускаем 1‑ю и 2‑ю строки

  const d = document.createElement('div');
  d.className = 'poem';
  d.innerHTML = `
    <h2>${title}</h2>
    <p class="date">${date}</p>
    <pre>${body}</pre>`;
  document.getElementById('poems-container').appendChild(d);

  // … остальное без изменений

  loading = false;
  if (pointer === list.length) {
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
