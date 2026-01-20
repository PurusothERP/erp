import frappe

def setup():
    print("Applying V4 Aggressive Branding (Stacked Layout)...")
    try:
        force_system_branding()
        frappe.db.commit()
        frappe.clear_cache()
        print("V4 Branding Applied & Cache Cleared!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Branding V4 Failed: {e}")
        import traceback
        traceback.print_exc()

def force_system_branding():
    brand_text = "Techxle Consulting"
    logo_url = "/files/techxle_logo.jpg"
    
    # 1. Update SYSTEM SETTINGS (The root of the "ERPNext" text)
    # This is often the hidden override.
    ss = frappe.get_single("System Settings")
    if hasattr(ss, "app_name"):
        ss.app_name = brand_text
        ss.save(ignore_permissions=True)
        print("Updated System Settings: app_name")

    # 2. Update WEBSITE SETTINGS
    ws = frappe.get_single("Website Settings")
    ws.app_name = brand_text
    ws.app_title = "Techxle Consultancy Services"
    
    # Custom HTML for "Logo Top, Name Bottom"
    # Note: Depending on the sidebar width, this might look tight, but we will try.
    # The sidebar header height is fixed, so 'bottom place' might just mean next to it or under it in a flex box.
    # Let's try a compact side-by-side first as 'bottom' inside the 40px header is hard.
    # But user said "bottom place", maybe they mean the footer? 
    # Usually "Logo of Techxl and in bottom place the name" implies a vertical stack.
    # We will try a Flex Column.
    
    stacked_html = f"""
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: start; line-height: 1.1;">
        <img src="{logo_url}" style="max-height: 25px; width: auto; margin-bottom: 2px;">
        <span style="font-size: 10px; font-weight: bold; color: inherit;">{brand_text}</span>
    </div>
    """
    
    # Or strict replacement
    ws.brand_html = stacked_html
    ws.app_logo = logo_url # Ensure logo is strictly linked
    ws.save(ignore_permissions=True)
    print("Updated Website Settings: brand_html")

    # 3. NavBar Settings
    ns = frappe.get_single("Navbar Settings")
    ns.app_logo = logo_url
    ns.save(ignore_permissions=True)

if __name__ == "__main__":
    setup()
