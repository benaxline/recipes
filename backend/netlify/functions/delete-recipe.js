const supabase = require('./helpers/supabase');

exports.handler = async function(event) {
  if (event.httpMethod !== 'DELETE') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const id = event.queryStringParameters.id;
  if (!id) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Missing recipe ID' }) };
  }

  try {
    const { data: existing, error: fetchErr } = await supabase
      .from('Recipes')
      .select('id')
      .eq('id', id)
      .limit(1);

    if (fetchErr) throw fetchErr;
    if (!existing.length) return { statusCode: 404, body: JSON.stringify({ error: 'Not found' }) };

    await supabase.from('Recipes').delete().eq('id', id);

    return { statusCode: 200, body: JSON.stringify({ message: 'Deleted' }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
