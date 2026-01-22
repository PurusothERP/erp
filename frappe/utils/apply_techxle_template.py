import frappe
import os

def run():
    # 1. Read the HTML File
    file_path = "/Users/purusothaman/Desktop/erpnext/erpnext-bench/techxle_template.html"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return
        
    with open(file_path, "r") as f:
        html_content = f.read()

    # 2. Check integrity
    if "{{" not in html_content:
        print("CRITICAL ERROR: Double curly braces not found in template file!")
        return
    else:
        print("Template file looks correct (contains {{ ).")

    # 3. Apply to targets
    targets = [
        "Quotation", "Sales Order", "Delivery Note", "Sales Invoice", 
        "Purchase Order", "Purchase Receipt", "Purchase Invoice", "Payment Entry", "Material Request"
    ]
    
    for doctype in targets:
        fmt_name = f"Techxle {doctype} Format"

        # Cleanup duplicates
        frappe.db.sql("DELETE FROM `tabPrint Format` WHERE doc_type=%s AND name LIKE 'Techxle%%' AND name != %s", (doctype, fmt_name))

        # Ensure Exists
        if not frappe.db.exists("Print Format", fmt_name):
             frappe.get_doc({
                "doctype": "Print Format",
                "name": fmt_name,
                "doc_type": doctype,
                "standard": "No",
                "custom_format": 1,
                "print_format_type": "Jinja",
                "html": "TEMP"
            }).insert()

        # Update
        frappe.db.sql("""
            UPDATE `tabPrint Format` 
            SET html=%s, custom_format=1, print_format_type='Jinja', disabled=0
            WHERE name=%s
        """, (html_content, fmt_name))
        
        print(f"Applied Template to: {fmt_name}")

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: Templates Updated from File Source.")

if __name__ == "__main__":
    run()
