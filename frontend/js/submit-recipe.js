// js/submit-recipe.js

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('recipe-form');
  const submitBtn = document.getElementById('submit-btn');
  const msg = document.getElementById('submission-message');

  function showAlert(type, text) {
    msg.innerHTML = `
      <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${text}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
  }

  function setSubmitting(isSubmitting) {
    submitBtn.disabled = isSubmitting;
    submitBtn.querySelector('.submit-text').classList.toggle('d-none', isSubmitting);
    submitBtn.querySelector('.submit-spinner').classList.toggle('d-none', !isSubmitting);
  }

  // Robust ingredient parsing: support commas OR newlines
  function parseIngredients(raw) {
    return raw
      .split(/[\n,]+/g)
      .map(s => s.trim())
      .filter(Boolean);
  }

  // One step per line; ignore empty lines
  function parseInstructions(raw) {
    return raw
      .split(/\n+/g)
      .map(s => s.trim())
      .filter(Boolean);
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Bootstrap validation
    if (!form.checkValidity()) {
      form.classList.add('was-validated');
      return;
    }

    setSubmitting(true);
    msg.innerHTML = '';

    const recipe = {
      name: document.getElementById('name').value.trim(),
      author: document.getElementById('author').value.trim(),
      type: document.getElementById('type').value.trim(),
      ingredients: parseIngredients(document.getElementById('ingredients').value),
      instructions: parseInstructions(document.getElementById('instructions').value),
      secret: document.getElementById('secret').value.trim()
    };

    try {
      const res = await fetch('/.netlify/functions/post-recipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(recipe)
      });

      if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(text || 'Failed to submit recipe.');
      }

      showAlert('success', '🎉 Recipe submitted for approval!');
      form.reset();
      form.classList.remove('was-validated');
    } catch (err) {
      showAlert('danger', `Error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  });
});
