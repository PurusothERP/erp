import frappe

def run():
    logo_path = "/files/techxle_desk_logo.png"
    
    # 1. SET LOGO IN SETTINGS
    if not frappe.db.exists("Navbar Settings", "Navbar Settings"):
        frappe.get_doc({"doctype": "Navbar Settings"}).insert()
    
    frappe.db.set_value("Navbar Settings", "Navbar Settings", "app_logo", logo_path)
    frappe.db.set_value("Navbar Settings", "Navbar Settings", "logo", logo_path)
    
    # 2. INJECT CSS FOR DESKTOP NAVBAR
    # We need to make sure the logo is big enough and the default "E" icon is hidden if present
    
    navbar_css = """
    <style>
        /* Force Logo Size and Position */
        .navbar-brand img, .navbar-brand .app-logo {
            max-height: 40px !important;
            width: auto !important;
            padding: 2px 0 !important;
        }
        
        /* Hide default 'E' icon just in case */
        .navbar-brand .frappe-icon {
            display: none !important;
        }

        /* Ensure Navbar has space */
        .navbar-brand {
            padding-left: 15px !important;
            min-width: 150px;
        }
    </style>
    """
    
    # Append to Website Settings head/brand_html to ensure it loads
    # Note: ERPNext Desk uses 'Navbar Settings', but sometimes 'Website Settings' affects global styles.
    # For Desk specifically, we rely on the standard "app_logo" setting working, but 
    # if we need CSS, we might need a custom app hook or inject it into 'app_include_css' (but that requires a file).
    # For now, let's rely on the settings primarily, as V15 is good about this.
    
    # However, to be SAFE, we update the Title too.
    frappe.db.set_value("Website Settings", "Website Settings", "app_title", "Techxl")
    frappe.db.set_value("Website Settings", "Website Settings", "app_name", "Techxl")
    
    frappe.clear_cache()
    print("SUCCESS: Desk Logo Updated to techxle_desk_logo.png")

if __name__ == "__main__":
    run()
