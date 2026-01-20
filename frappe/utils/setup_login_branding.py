import frappe

def setup():
    print("Applying Login Page Branding...")
    try:
        update_login_settings()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Branding Applied!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Login Branding Failed: {e}")
        import traceback
        traceback.print_exc()

def update_login_settings():
    # Images paths (public files)
    hero_image = "/files/techxle_login_hero.jpg"
    logo_image = "/files/techxle_login_logo.jpg"
    
    brand_text = "Techxl"
    
    # 1. Update Website Settings (Global)
    ws = frappe.get_single("Website Settings")
    ws.app_logo = logo_image
    ws.splash_image = hero_image
    
    # Since we previously used 'brand_html' to override the Logo+Text in the user's dashboard sidebar,
    # we need to make sure this doesn't break the Login Page or if the Login Page uses it.
    # The user wants "Techxl in text near the secound image logo".
    # We can update the `brand_html` to specifically use the NEW logo and NEW text.
    
    # Let's verify what `brand_html` does. It usually replaces the navbar brand.
    # On login page, usually the Logo is shown, then the App Title.
    
    # We will update the `brand_html` to reuse the new logo and the requested "Techxl" text.
    # We'll use a clean flex layout.
    
    new_brand_html = f"""
    <div class="techxle-brand" style="display: flex; align-items: center; justify-content: center;">
        <img src="{logo_image}" style="max-height: 30px; margin-right: 10px; width: auto;">
        <span style="font-size: 16px; font-weight: bold; color: inherit;">{brand_text}</span>
    </div>
    """
    ws.brand_html = new_brand_html
    ws.app_name = brand_text # Update system name to match request
    
    # Also update 'Banner Image' if it exists (some themes use it)
    if hasattr(ws, "banner_image"):
        ws.banner_image = hero_image
        
    ws.save(ignore_permissions=True)
    print("Updated Website Settings (Logo, Splash, Brand HTML)")

    # 2. Navbar Settings (Backup)
    ns = frappe.get_single("Navbar Settings")
    ns.app_logo = logo_image
    ns.save(ignore_permissions=True)
    print("Updated Navbar Settings")

if __name__ == "__main__":
    setup()
