import frappe

def setup():
    print("Forcing Sidebar Branding with HTML...")
    try:
        force_branding()
        frappe.db.commit()
        frappe.clear_cache()
        print("Branding Forced & Cache Cleared!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Force Branding Failed: {e}")
        import traceback
        traceback.print_exc()

def force_branding():
    # Fetch Settings
    ws = frappe.get_single("Website Settings")
    ns = frappe.get_single("Navbar Settings")

    logo_url = "/files/techxle_logo.jpg"
    brand_text = "Techxle Consulting"
    
    # 1. Navbar Settings (The modern place for the Desk Sidebar)
    # If standard 'app_name' isn't showing because of logo, we use brand_html
    # However, Navbar settings usually just takes 'app_logo'.
    
    # Let's try setting the Website Settings 'brand_html' which propagates to many places
    brand_html = f"""
    <div style="display: flex; align-items: center;">
        <img src="{logo_url}" style="height: 24px; margin-right: 8px;">
        <span style="font-weight: bold; font-size: 16px;">{brand_text}</span>
    </div>
    """
    
    ws.brand_html = brand_html
    ws.app_name = brand_text # Fallback
    ws.app_logo = logo_url   # Fallback
    ws.save(ignore_permissions=True)
    
    # 2. Navbar Settings specific override
    # Sometimes Navbar Settings completely overrides Website Settings for the Desk
    ns.app_logo = logo_url
    # There is no 'brand_text' in Navbar Settings, it uses app_name from system or website settings.
    # But checking if we can inject it via help menu or similar is overkill.
    # The most common issue is that if valid logo is mapped, text is hidden.
    # Let's ensure the Logo itself isn't effectively JUST the image.
    
    # If the user wants TEXT + IMAGE, usually standard ERPNext hides text if image is there.
    # We might need to rely on the brand_html being picked up, or customization.
    
    print("Set brand_html to FORCE display.")

if __name__ == "__main__":
    setup()
