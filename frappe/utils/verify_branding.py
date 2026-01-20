import frappe

def verify():
    print("Verifying Techxle Branding...")
    
    # Verify Company
    company = frappe.db.exists("Company", "Techxle CRM")
    print(f"Company 'Techxle CRM': {'OK' if company else 'MISSING'}")

    # Verify Website Settings
    ws = frappe.get_single("Website Settings")
    print(f"Website Title: {ws.app_title} ({'OK' if ws.app_title == 'Techxle CRM' else 'MISMATCH'})")

    # Verify Print Format
    pf = frappe.db.exists("Print Format", "Techxle Bilingual")
    print(f"Print Format 'Techxle Bilingual': {'OK' if pf else 'MISSING'}")

    if company and ws.app_title == 'Techxle CRM' and pf:
        print("BRANDING VERIFICATION SUCCESSFUL")
    else:
        print("BRANDING VERIFICATION FAILED")
