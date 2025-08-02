from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_recipe(recipe):
    """Insert a new recipe into Supabase"""
    response = supabase.table("recipes").insert(recipe).execute()
    if response.error:
        raise Exception(response.error.message)
    