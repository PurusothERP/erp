import frappe
import os

def run():
    # READ FILE
    file_path = "/Users/purusothaman/Desktop/erpnext/erpnext-bench/techxle_template.html"
    with open(file_path, "r") as f:
        html_content = f.read()

    targets = [
        "Quotation", "Sales Order", "Delivery Note", "Sales Invoice", 
        "Purchase Order", "Purchase Receipt", "Purchase Invoice", "Payment Entry", "Material Request"
    ]
    
    for doctype in targets:
        fmt_name = f"Techxle {doctype} Format"

        if not frappe.db.exists("Print Format", fmt_name):
             d = frappe.new_doc("Print Format")
             d.name = fmt_name
             d.doc_type = doctype
             d.insert()
        
        # KEY FIX: Set format_data to NULL to prevent JSON overriding HTML
        frappe.db.sql("""
            UPDATE `tabPrint Format` 
            SET html=%s, 
                custom_format=1, 
                print_format_type='Jinja', 
                disabled=0,
                format_data=NULL 
            WHERE name=%s
        """, (html_content, fmt_name))
        
        # Ensure Default
        frappe.db.set_value("DocType", doctype, "default_print_format", fmt_name)
        
        print(f"Aggressively Updated: {fmt_name}")

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: Full White UI Applied.")

if __name__ == "__main__":
    run()
