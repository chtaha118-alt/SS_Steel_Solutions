"""Login, signup and logout using Supabase Auth."""
from core.supabase_client import supabase


class AuthError(Exception):
    """Message is safe to show to the user."""


def login(email, password):
    email = (email or "").strip()
    if not email or not password:
        raise AuthError("Enter your email and password.")
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as e:
        raise AuthError("Wrong email or password.") from e

    user = res.user
    rows = supabase.table("profiles").select("*").eq("id", user.id).execute().data
    if not rows:
        supabase.auth.sign_out()
        raise AuthError("Your account has no profile. Ask the admin to set it up.")
    p = rows[0]
    return {
        "id": user.id,
        "email": user.email,
        "full_name": p.get("full_name") or user.email,
        "role": p["role"],  # admin / staff / customer
    }


def signup_customer(email, password, full_name, phone=""):
    email = (email or "").strip()
    if not email or not full_name.strip():
        raise AuthError("Name and email are required.")
    if len(password or "") < 6:
        raise AuthError("Password must be at least 6 characters.")
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
    except Exception as e:
        raise AuthError(f"Could not create account: {e}") from e

    if res.session is None:
        raise AuthError(
            "Account created, but Supabase is waiting for email confirmation. "
            "Confirm the email, or turn off 'Confirm email' in Supabase "
            "(Authentication > Sign In / Providers > Email) while developing."
        )
    uid = res.user.id
    try:
        supabase.table("profiles").insert(
            {"id": uid, "full_name": full_name.strip(), "phone": phone, "role": "customer"}
        ).execute()
        supabase.table("customers").insert(
            {"user_id": uid, "name": full_name.strip(), "phone": phone}
        ).execute()
    except Exception as e:
        raise AuthError(f"Account created but profile failed: {e}") from e
    supabase.auth.sign_out()


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
