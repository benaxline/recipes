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
            displayRecipes(recipes);
        })
        .catch(error => {
            console.error('Error fetching recipes:', error);
            document.getElementById('recipes-container').innerHTML = 
                `<p>Error loading recipes: ${error.message}. Please try again later.</p>`;
        });
});

function displayRecipes(recipes) {
    const recipesContainer = document.getElementById('recipes-container');
    
    if (!recipes || recipes.length === 0) {
        recipesContainer.innerHTML = '<p>No recipes found.</p>';
        return;
    }
    
    let html = '';
    
    recipes.forEach(recipe => {
        html += `
            <div class="recipe-card">
                <h3>${recipe.name}</h3>
                <p class="author">By ${recipe.author}</p>
                <p class="category">${recipe.category}</p>
                <a href="/recipe-detail.html?title=${encodeURIComponent(recipe.name)}" 
                   class="view-recipe">View Recipe</a>
            </div>
        `;
    });
    
    recipesContainer.innerHTML = html;
}
