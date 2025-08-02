// js/submit-recipe.js
document.getElementById('recipe-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const recipe = {
        name: document.getElementById('name').value.trim(),
        author: document.getElementById('author').value.trim(),
        type: document.getElementById('type').value.trim(),
        ingredients: document.getElementById('ingredients').value.trim().split(',').map(i => i.trim()),
        instructions: document.getElementById('instructions').value.trim().split('\n').map(i => i.trim()),
        secret: document.getElementById('secret').value.trim()
    };

    fetch('/.netlify/functions/post-recipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(recipe)
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to submit recipe.');
        return response.json();
    })
    .then(() => {
        document.getElementById('submission-message').innerHTML =
        '<p style="color:green;">Recipe submitted for approval!</p>';
        document.getElementById('recipe-form').reset();
    })
    .catch(err => {
        document.getElementById('submission-message').innerHTML =
        `<p style="color:red;">Error: ${err.message}</p>`;
    });
});