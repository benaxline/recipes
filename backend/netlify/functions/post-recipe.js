const supabase = require('./helpers/supabase');

exports.handler = async function(event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const data = JSON.parse(event.body || '{}');
  const { name, author, type, ingredients, instructions } = data;

  if (!name || !ingredients || !instructions) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'name, ingredients, and instructions are required' })
    };
  }

  try {
    // Check for duplicates
    const { data: dup, error: dupError } = await supabase
      .from('Recipes')
      .select('id')
      .eq('name', name)
      .eq('author', author)
      .limit(1);

    if (dupError) throw dupError;
    if (dup.length > 0) {
      return { statusCode: 409, body: JSON.stringify({ error: 'Recipe already exists' }) };
    }

    const payload = {
      name,
      author,
      type,
      ingredients: ingredients.join('\n'),
      instructions: instructions.join('\n')
    };

    const { data: newRecipe, error } = await supabase
      .from('Recipes')
      .insert(payload)
      .select()
      .single();

    if (error) throw error;

    newRecipe.ingredients = newRecipe.ingredients?.split('\n') || [];
    newRecipe.instructions = newRecipe.instructions?.split('\n') || [];

    return {
      statusCode: 201,
      body: JSON.stringify(newRecipe)
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
