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
    // Confirm existence
    const { data: existing, error: getErr } = await supabase
      .from('Recipes')
      .select('id')
      .eq('id', id)
      .limit(1);

    if (getErr) throw getErr;
    if (!existing.length) return { statusCode: 404, body: JSON.stringify({ error: 'Not found' }) };

    await supabase.from('Recipes').delete().eq('id', id);

    return { statusCode: 200, body: JSON.stringify({ message: 'Deleted' }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
