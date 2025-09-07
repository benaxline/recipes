// js/main.js

document.addEventListener('DOMContentLoaded', initFeaturedSection);

async function initFeaturedSection() {
  const grid = document.getElementById('featured-container');
  if (!grid) return;

  try {
    const recipes = await fetchRecipes();

    // Prefer items explicitly marked featured; otherwise use all
    const featuredSubset = (recipes || []).filter(r =>
      r?.featured === true ||
      r?.isFeatured === true ||
      (Array.isArray(r?.tags) && r.tags.includes('featured'))
    );

    const pool = featuredSubset.length ? featuredSubset : recipes;

    // Randomize and take 6
    const pick = shuffle(pool).slice(0, 6);

    grid.innerHTML = pick.map(cardHTML).join('');
  } catch (err) {
    console.error('Failed to load featured recipes:', err);
    const msg = err?.message || 'Unknown error';
    document.getElementById('featured-container').innerHTML =
      `<p>Error loading featured recipes: ${msg}</p>`;
  }
}

/** Fetch all recipes (adjust the endpoint if needed). */
async function fetchRecipes() {
  const res = await fetch('/api/recipes');
  if (!res.ok) {
    throw new Error(`HTTP error! Status: ${res.status}`);
  }
  // Expecting an array of recipe objects with at least: id, name
  return res.json();
}

/** Robust Fisher–Yates shuffle. Uses crypto if available. */
function shuffle(arr) {
  const a = arr.slice();
  if (window.crypto && window.crypto.getRandomValues) {
    for (let i = a.length - 1; i > 0; i--) {
      const rand = new Uint32Array(1);
      window.crypto.getRandomValues(rand);
      const j = rand[0] % (i + 1);
      [a[i], a[j]] = [a[j], a[i]];
    }
  } else {
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
  }
  return a;
}

/** Build a simple card; link by ID so detail page reads ?id=... */
function cardHTML(r) {
  const id = r.id; // required per your note
  const name = r.name || 'Untitled recipe';
  const author = r.author ?? 'Unknown';
  const type = r.type ?? '';
  const img = r.image || r.cover || r.photo || 'https://picsum.photos/600/400?blur=1';

  const href = `/recipe-detail.html?id=${encodeURIComponent(String(id))}`;

  return `
    <a href="${href}" class="recipe-card">
      <div class="recipe-card__image-wrap">
        <img src="${img}" alt="${name}">
      </div>
      <div class="recipe-card__body">
        <h3>${name}</h3>
        <p class="author">By ${author}</p>
        ${type ? `<p class="category">${type}</p>` : ''}
      </div>
    </a>
  `;
}
