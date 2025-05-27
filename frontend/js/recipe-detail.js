document.addEventListener('DOMContentLoaded', function() {
    // Get recipe title from URL
    const urlParams = new URLSearchParams(window.location.search);
    const recipeTitle = urlParams.get('title');
    
    if (!recipeTitle) {
        document.getElementById('recipe-detail').innerHTML = '<p>Recipe not found</p>';
        return;
    }
    
    // Fetch recipe details from the API endpoint
    fetch(`/api/recipes/${encodeURIComponent(recipeTitle)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(recipe => {
            displayRecipe(recipe);
        })
        .catch(error => {
            console.error('Error fetching recipe:', error);
            document.getElementById('recipe-detail').innerHTML = 
                `<p>Error loading recipe: ${error.message}</p>`;
        });
});

function displayRecipe(recipe) {
    const recipeDetail = document.getElementById('recipe-detail');
    
    const html = `
        <h2>${recipe.name}</h2>
        <p class="author">By ${recipe.author}</p>
        <p class="category">${recipe.type}</p>
        
        <h3>Ingredients</h3>
        <ul class="ingredients">
            ${recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
        </ul>
        
        <h3>Instructions</h3>
        <ol class="instructions">
            ${recipe.instructions.map(step => `<li>${step}</li>`).join('')}
        </ol>
    `;
    
    recipeDetail.innerHTML = html;
}

function fetchComments(recipeTitle) {
    // Fetch blogs related to this recipe
    fetch('/blogs')
        .then(response => response.json())
        .then(blogs => {
            const relatedBlogs = blogs.filter(blog => 
                blog.recipe_title && blog.recipe_title.toLowerCase() === recipeTitle.toLowerCase()
            );
            
            if (relatedBlogs.length > 0) {
                displayComments(relatedBlogs);
            } else {
                document.getElementById('comments-container').innerHTML = 
                    '<p>No comments yet. Be the first to comment!</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching comments:', error);
        });
}

function displayComments(blogs) {
    const commentsContainer = document.getElementById('comments-container');
    let html = '';
    
    blogs.forEach(blog => {
        html += `
            <div class="comment">
                <h4>${blog.title}</h4>
                <p class="meta">By ${blog.author} on ${new Date(blog.time).toLocaleString()}</p>
                <div class="content">${blog.content}</div>
            </div>
        `;
    });
    
    commentsContainer.innerHTML = html;
}

function postComment(recipeTitle) {
    const author = document.getElementById('author').value;
    const content = document.getElementById('content').value;
    
    const commentData = {
        title: `Comment on ${recipeTitle}`,
        content: content,
        author: author,
        recipe_title: recipeTitle
    };
    
    fetch('/blogs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(commentData)
    })
    .then(response => response.json())
    .then(data => {
        // Clear form
        document.getElementById('author').value = '';
        document.getElementById('content').value = '';
        
        // Refresh comments
        fetchComments(recipeTitle);
    })
    .catch(error => {
        console.error('Error posting comment:', error);
        alert('Failed to post comment. Please try again.');
    });
}
