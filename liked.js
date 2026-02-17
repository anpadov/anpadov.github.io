async function loadLiked() {
  const res = await fetch('liked-list.json');
  const list = await res.json();

  const container = document.getElementById('liked-container');
  const byAuthor = {};

  for (const item of list) {
    if (!byAuthor[item.author]) {
      byAuthor[item.author] = [];
    }
    byAuthor[item.author].push(item);
  }

  for (const author of Object.keys(byAuthor).sort()) {
    const h2 = document.createElement('h2');
    h2.textContent = author;
    container.appendChild(h2);

    const ul = document.createElement('ul');

    for (const poem of byAuthor[author]) {
      const li = document.createElement('li');
      li.innerHTML = `
        <a href="poem.html?file=${encodeURIComponent(poem.file)}">
          ${poem.title}
        </a>
      `;
      ul.appendChild(li);
    }

    container.appendChild(ul);
  }
}

document.addEventListener('DOMContentLoaded', loadLiked);
