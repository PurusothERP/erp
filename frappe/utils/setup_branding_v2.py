import frappe

def setup():
    print("Applying Dashboard & Login Branding Updates...")
    try:
        update_branding_names()
        frappe.db.commit()
        print("Branding Updates Successful!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Branding Update Failed: {e}")
        import traceback
        traceback.print_exc()

def update_branding_names():
    print("Updating System Titles...")
    
    # Website Settings
    ws = frappe.get_single("Website Settings")
    
    # Login Page Title & Browser Tab Title
    ws.app_title = "Techxle Consultancy Services"
    
    # Brand Name (Dashboard Top-Left)
    ws.app_name = "Techxle"
    
    # Also explicitly set brand html if needed to override logo text fallbacks
    # ws.brand_html = '<img src="/files/techxle_logo.jpg" style="max-height: 30px;"> Techxle' 
    # But usually just setting app_name is cleaner if logo is already set.
    
    ws.save(ignore_permissions=True)
    
    # System Settings (sometimes overrides or works in tandem)
    try:
        ss = frappe.get_single("System Settings")
        # In recent v14/v15, System Settings might read from Website Settings, 
        # but let's check field existence safely just in case.
        if hasattr(ss, "app_name"): # V13/V14 specific
             pass 
    except:
        pass

if __name__ == "__main__":
    setup()
