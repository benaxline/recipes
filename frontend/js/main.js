// js/main.js — Home page: show 6 random featured recipes

document.addEventListener('DOMContentLoaded', initFeatured);

async function initFeatured() {
  const grid = document.getElementById('featured-container');
  if (!grid) return;

  try {
    const recipes = await fetchAllRecipes();

    if (!Array.isArray(recipes) || recipes.length === 0) {
      grid.innerHTML = '<p class="text-muted text-center">No recipes found.</p>';
      return;
    }

    // Prefer explicitly featured; otherwise use all
    const featured = recipes.filter(r =>
      r?.featured === true ||
      r?.isFeatured === true ||
      (Array.isArray(r?.tags) && r.tags.includes('featured'))
    );

    const pool = featured.length ? featured : recipes;

    // Randomize and take 6
    const pick = shuffle(pool).slice(0, 6);

    grid.innerHTML = pick.map(cardHTML).join('');
  } catch (err) {
    console.error('Error loading featured recipes:', err);
    grid.innerHTML = `<p>Error loading featured recipes: ${err?.message || 'Unknown error'}</p>`;
  }
}

/** Use your Netlify Function (same source as All Recipes). */
async function fetchAllRecipes() {
  const res = await fetch('/.netlify/functions/get-recipes', {
    headers: { 'accept': 'application/json' }
  });
  if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
  return res.json();
}

/** Fisher–Yates shuffle (crypto-backed when available). */
function shuffle(arr) {
  const a = arr.slice();
  if (window.crypto?.getRandomValues) {
    for (let i = a.length - 1; i > 0; i--) {
      const r = new Uint32Array(1);
      window.crypto.getRandomValues(r);
      const j = r[0] % (i + 1);
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

/** Card markup matching recipes.js (Bootstrap). */
function cardHTML(recipe) {
  const id = recipe.id ?? '';
  const name = recipe.name || 'Untitled';
  const author = recipe.author || 'Unknown';
  const type = recipe.type || 'Uncategorized';

  // Include both id and title for compatibility with the current detail page
  const href = `recipe-detail.html?id=${encodeURIComponent(String(id))}&title=${encodeURIComponent(name)}`;

  return `
    <div class="col-12 col-sm-6 col-md-4">
      <div class="card h-100 shadow-sm">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">${name}</h5>
          <h6 class="card-subtitle mb-2 text-muted">By ${author}</h6>
          <p class="card-text">
            <span class="badge bg-secondary">${type}</span>
          </p>
          <a href="${href}" class="btn btn-primary mt-auto">View Recipe</a>
        </div>
      </div>
    </div>
  `;
}
