const supabase = require('./helpers/supabase');

exports.handler = async function () {
  try {
    const { data, error } = await supabase
      .from('Recipes')
      .select('*')
      .order('created_at', { ascending: true });

    if (error) throw error;

    const formatted = data.map(recipe => ({
      ...recipe,
      ingredients: recipe.ingredients?.split('\n') || [],
      instructions: recipe.instructions?.split('\n') || []
    }));

    return {
      statusCode: 200,
      body: JSON.stringify(formatted)
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};
