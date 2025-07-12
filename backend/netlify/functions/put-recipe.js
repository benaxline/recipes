const supabase = require('./helpers/supabase');

exports.handler = async function(event) {
  if (event.httpMethod !== 'PUT') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const id = event.queryStringParameters.id;
  if (!id) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Missing recipe ID' }) };
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
    const { data: existing, error: fetchErr } = await supabase
      .from('Recipes')
      .select('id')
      .eq('id', id)
      .limit(1);

    if (fetchErr) throw fetchErr;
    if (!existing.length) return { statusCode: 404, body: JSON.stringify({ error: 'Not found' }) };

    const { data: dup, error: dupErr } = await supabase
      .from('Recipes')
      .select('id')
      .eq('name', name)
      .eq('author', author)
      .neq('id', id)
      .limit(1);

    if (dupErr) throw dupErr;
    if (dup.length > 0) {
      return { statusCode: 409, body: JSON.stringify({ error: 'Another recipe with that name exists' }) };
    }

    const payload = {
      name,
      author,
      type,
      ingredients: ingredients.join('\n'),
      instructions: instructions.join('\n')
    };

    const { data: updated, error } = await supabase
      .from('Recipes')
      .update(payload)
      .eq('id', id)
      .select()
      .single();

    if (error) throw error;

    updated.ingredients = updated.ingredients?.split('\n') || [];
    updated.instructions = updated.instructions?.split('\n') || [];

    return { statusCode: 200, body: JSON.stringify(updated) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
