import frappe

def run():
    logo_path = "/files/techxle_nav_logo.png"

    # 1. Update Navbar Settings (The Top Bar)
    if not frappe.db.exists("Navbar Settings", "Navbar Settings"):
        frappe.get_doc({"doctype": "Navbar Settings"}).insert()
    
    frappe.db.set_value("Navbar Settings", "Navbar Settings", "app_logo", logo_path)
    frappe.db.set_value("Navbar Settings", "Navbar Settings", "logo", logo_path) # Some versions use this

    # 2. Update Website Settings (Global fallback)
    frappe.db.set_value("Website Settings", "Website Settings", "app_logo", logo_path)
    frappe.db.set_value("Website Settings", "Website Settings", "banner_image", logo_path)

    # 3. Clear Cache
    frappe.clear_cache()
    print(f"SUCCESS: Navbar Logo updated into {logo_path}")

if __name__ == "__main__":
    run()
