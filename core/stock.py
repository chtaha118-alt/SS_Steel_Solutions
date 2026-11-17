"""Database functions for products / stock."""
from core.supabase_client import supabase

CATEGORIES = ["plate", "round_bar", "rebar", "square_bar", "flat_bar", "pipe", "angle", "beam"]


def list_products():
    return supabase.table("products").select("*").order("id").execute().data


def add_product(name, category, size_label, grade, price_per_kg, stock_pieces, stock_kg):
    if not name.strip():
        raise ValueError("Product name is required.")
    if category not in CATEGORIES:
        raise ValueError("Invalid category.")
    return supabase.table("products").insert({
        "name": name.strip(),
        "category": category,
        "size_label": size_label.strip(),
        "grade": grade.strip(),
        "price_per_kg": price_per_kg,
        "stock_pieces": stock_pieces,
        "stock_kg": stock_kg,
    }).execute().data
