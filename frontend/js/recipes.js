let allRecipes = [];

document.addEventListener('DOMContentLoaded', function() {
    console.log('Recipes page loaded, fetching recipes...');
    
    // Fetch all recipes from the API endpoint
    fetch('/.netlify/functions/get-recipes')
        .then(response => {
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(recipes => {
            console.log('Recipes received:', recipes);
            allRecipes = recipes;
            displayRecipes(allRecipes);
        })
        .catch(error => {
            console.error('Error fetching recipes:', error);
            document.getElementById('recipes-container').innerHTML = 
                `<p>Error loading recipes: ${error.message}. Please try again later.</p>`;
        });
});

const searchInput = document.getElementById('recipe-search');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        const query = searchInput.value.toLowerCase().trim();
        console.log('Search query:', query);
        
        const filtered = allRecipes.filter(recipe =>
        recipe.name?.toLowerCase().includes(query) ||
        recipe.author?.toLowerCase().includes(query) ||
        recipe.type?.toLowerCase().includes(query)
        );
        
        console.log('Filtered recipes:', filteredRecipes);
        displayRecipes(filteredRecipes);
    });
}

function displayRecipes(recipes) {
  const recipesContainer = document.getElementById('recipes-container');

  if (!recipes || recipes.length === 0) {
    recipesContainer.innerHTML = '<p class="text-muted text-center">No recipes found.</p>';
    return;
  }

  let html = '';

  recipes.forEach(recipe => {
    html += `
      <div class="col-12 col-sm-6 col-md-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">${recipe.name}</h5>
            <h6 class="card-subtitle mb-2 text-muted">By ${recipe.author || 'Unknown'}</h6>
            <p class="card-text">
              <span class="badge bg-secondary">${recipe.category || 'Uncategorized'}</span>
            </p>
            <a href="recipe-detail.html?title=${encodeURIComponent(recipe.name)}" class="btn btn-primary mt-auto">
              View Recipe
            </a>
          </div>
        </div>
      </div>
    `;
  });

  recipesContainer.innerHTML = html;
}