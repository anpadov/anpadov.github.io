async function loadList() {
  const res = await fetch('poem-list.json');
  const poems = await res.json();

  const container = document.getElementById('poem-list');

  poems.forEach(p => {
    const a = document.createElement('a');
    a.href = `poem.html?file=${encodeURIComponent(p.file)}`;
    a.className = 'poem-link';

    const date = formatDate(p.ts);

    a.innerHTML = `
      <span class="title">${p.title}</span>
      <span class="date">${date}</span>
    `;

    container.appendChild(a);
  });
}

function formatDate(ts) {
  // ts = YYYYMMDDHH
  const y = ts.slice(0, 4);
  const m = ts.slice(4, 6);
  const d = ts.slice(6, 8);

  return `${y}-${m}-${d}`;
}

window.addEventListener('DOMContentLoaded', loadList);
