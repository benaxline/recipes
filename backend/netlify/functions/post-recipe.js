const supabase = require('./helpers/supabase');

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const data = JSON.parse(event.body || '{}');
  const { name, author, category, ingredients, instructions, secret } = data;

  // 🔍 Log all incoming values
  console.log('📥 Incoming data:', data);
  console.log('🔐 Submitted secret:', secret);
  console.log('🔐 Expected secret:', process.env.RECIPE_API_SECRET);

  if (secret !== process.env.RECIPE_API_SECRET) {
    console.log('⛔ Unauthorized attempt');
    return {
      statusCode: 401,
      body: JSON.stringify({ error: 'Unauthorized' })
    };
  }

  if (!name || !ingredients || !instructions) {
    console.log('⚠️ Missing required fields');
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'name, ingredients, and instructions are required' })
    };
  }

  try {
    const { data: dup, error: dupErr } = await supabase
      .from('Recipes')
      .select('id')
      .eq('name', name)
      .eq('author', author)
      .limit(1);

    if (dupErr) throw dupErr;
    if (dup && dup.length > 0) {
      console.log('⚠️ Duplicate recipe found');
      return {
        statusCode: 409,
        body: JSON.stringify({ error: 'Recipe already exists' })
      };
    }

    const safeIngredients = Array.isArray(ingredients) ? ingredients.join('\n') : '';
    const safeInstructions = Array.isArray(instructions) ? instructions.join('\n') : '';

    const payload = {
      name,
      author,
      category,
      ingredients: safeIngredients,
      instructions: safeInstructions,
      approved: true
    };

    console.log('📦 Payload to insert:', payload);

    const { data: inserted, error } = await supabase
      .from('Recipes')
      .insert(payload)
      .select()
      .single();

    if (error) throw error;

    inserted.ingredients = inserted.ingredients?.split('\n') || [];
    inserted.instructions = inserted.instructions?.split('\n') || [];

    console.log('✅ Recipe inserted successfully');
    return {
      statusCode: 201,
      body: JSON.stringify(inserted)
    };
  } catch (err) {
    console.error('🔥 Server error:', err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message || 'Internal Server Error' })
    };
  }
};
