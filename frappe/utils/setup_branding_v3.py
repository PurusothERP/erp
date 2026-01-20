import frappe

def setup():
    print("Applying Final Sidebar & Brand Polish...")
    try:
        update_sidebar_brand()
        frappe.db.commit()
        print("Brand Polish Applied Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Brand Polish Failed: {e}")
        import traceback
        traceback.print_exc()

def update_sidebar_brand():
    print("Updating Dashboard Brand Name...")
    
    # 1. Update Website Settings (App Name controls the top-left text usually)
    ws = frappe.get_single("Website Settings")
    ws.app_name = "Techxle Consulting"
    ws.app_title = "Techxle Consultancy Services" # Re-confirming login title
    ws.save(ignore_permissions=True)
    
    # 2. Update Navbar Settings for Logo consistency
    # Ensure the logo is set app-wide
    ns = frappe.get_single("Navbar Settings")
    if not ns.app_logo:
         ns.app_logo = "/files/techxle_logo.jpg"
    
    # Sometimes 'Logo Width' can help if logo looks too small
    # Check if field exists (version dependent)
    if hasattr(ns, "logo_width"):
        # standard is often auto or blank, but if users want "good ui", sometimes a fixed width helps if logo is weird aspect ratio
        pass 
        
    ns.save(ignore_permissions=True)
    
    print("Dashboard Brand set to 'Techxle Consulting'")

if __name__ == "__main__":
    setup()
