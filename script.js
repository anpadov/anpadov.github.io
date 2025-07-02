let pointer = 0;
let list = [];
let loading = false;

async function fetchList() {
  const res = await fetch('poem-list.json');
  list = await res.json();
}

async function loadNext() {
  if (loading || pointer >= list.length) return;
  loading = true;

  const {file, title} = list[pointer];
  pointer++;

  const res  = await fetch(file);
  const body = await res.text();

  const div = document.createElement('div');
  div.className = 'poem';
  div.innerHTML = `<h2>${title}</h2><pre>${body.split('\n').slice(1).join('\n')}</pre>`;
  document.getElementById('poems-container').appendChild(div);

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
