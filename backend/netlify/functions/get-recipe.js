const supabase = require('./helpers/supabase');

exports.handler = async function(event) {
  const name = event.queryStringParameters.name;
  if (!name) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Missing name param' }) };
  }

  try {
    const { data, error } = await supabase
      .from('Recipes')
      .select('*')
      .ilike('name', name);

    if (error) throw error;
    if (!data || data.length === 0)
      return { statusCode: 404, body: JSON.stringify({ error: 'Not found' }) };

    const recipe = data[0];
    recipe.ingredients = recipe.ingredients?.split('\n') || [];
    recipe.instructions = recipe.instructions?.split('\n') || [];

    return {
      statusCode: 200,
      body: JSON.stringify(recipe)
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
