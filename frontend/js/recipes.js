document.addEventListener('DOMContentLoaded', function() {
    // Fetch all recipes
    fetch('/recipes')
        .then(response => response.json())
        .then(recipes => {
            displayRecipes(recipes);
        })
        .catch(error => {
            console.error('Error fetching recipes:', error);
            document.getElementById('recipes-container').innerHTML = 
                '<p>Error loading recipes. Please try again later.</p>';
        });
});

function displayRecipes(recipes) {
    const recipesContainer = document.getElementById('recipes-container');
    
    if (recipes.length === 0) {
        recipesContainer.innerHTML = '<p>No recipes found.</p>';
        return;
    }
    
    let html = '';
    
    recipes.forEach(recipe => {
        html += `
            <div class="recipe-card">
                <h3>${recipe.name}</h3>
                <p class="author">By ${recipe.author}</p>
                <p class="category">${recipe.type}</p>
                <a href="/recipe-detail.html?title=${encodeURIComponent(recipe.name)}" 
                   class="view-recipe">View Recipe</a>
            </div>
        `;
    });
    
    recipesContainer.innerHTML = html;
}