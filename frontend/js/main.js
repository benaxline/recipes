// js/main.js

document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('featured-container');
  if (!grid) return;

  try {
    const recipes = await fetchAllRecipes();

    if (!Array.isArray(recipes) || recipes.length === 0) {
      grid.innerHTML = '<p>No recipes found.</p>';
      return;
    }

    // If you ever add a "featured" flag, prefer those; otherwise use all
    const featured = recipes.filter(r =>
      r?.featured === true ||
      r?.isFeatured === true ||
      (Array.isArray(r?.tags) && r.tags.includes('featured'))
    );

    const pool = featured.length ? featured : recipes;
    const pick = shuffle(pool).slice(0, 6); // random 6

    grid.innerHTML = pick.map(cardHTML).join('');
  } catch (err) {
    console.error('Error loading featured recipes:', err);
    grid.innerHTML = `<p>Error loading featured recipes: ${err?.message || 'Unknown error'}</p>`;
  }
});

/** Fetch all recipes (same endpoint used on All Recipes page). */
async function fetchAllRecipes() {
  const res = await fetch('/api/recipes');
  if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
  return res.json();
}

/** Fisher–Yates shuffle (crypto-backed when available). */
function shuffle(arr) {
  const a = arr.slice();
  if (window.crypto?.getRandomValues) {
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

/** Build a card that matches the All Recipes markup/styles. */
function cardHTML(recipe) {
  const name = recipe.name || 'Untitled';
  const author = recipe.author ?? 'Unknown';
  const type = recipe.type ?? '';

  // Keep legacy title-based routing so your current recipe-detail page works.
  // If you switch detail to use ID, change this to `?id=${recipe.id}`.
  const href = `/recipe-detail.html?title=${encodeURIComponent(name)}`;

  return `
    <div class="recipe-card">
      <h3>${name}</h3>
      <p class="author">By ${author}</p>
      <p class="category">${type}</p>
      <a href="${href}" class="view-recipe">View Recipe</a>
    </div>
  `;
}
