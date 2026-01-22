import frappe
import os

def run():
    print("Starting Debug & Fix Process...")
    
    # 1. Read Valid File
    file_path = "/Users/purusothaman/Desktop/erpnext/erpnext-bench/techxle_template.html"
    with open(file_path, "r") as f:
        file_html = f.read()
    
    # 2. Check Target Format
    fmt_name = "Techxle Sales Order Format"
    if not frappe.db.exists("Print Format", fmt_name):
        print(f"Format {fmt_name} does not exist! Creating...")
        doc = frappe.new_doc("Print Format")
        doc.name = fmt_name
        doc.doc_type = "Sales Order"
        doc.standard = "No"
        doc.custom_format = 1
        doc.print_format_type = "Jinja"
        doc.html = file_html
        doc.save()
        print("Created via ORM.")
    else:
        # Read existing
        db_html = frappe.db.get_value("Print Format", fmt_name, "html") or ""
        
        # Compare
        if "{{ doc.doctype }}" in file_html and "{ doc.doctype }" in db_html:
            print("DETECTED CORRUPTION: File has {{ but DB has {")
        elif db_html == file_html:
            print("Content matches perfectly.")
        else:
            print("Content differs (size mismatch). Updating...")

        # Force Update via ORM (doc.save handles events/cache better than raw SQL sometimes)
        doc = frappe.get_doc("Print Format", fmt_name)
        doc.html = file_html
        doc.custom_format = 1
        doc.print_format_type = "Jinja"
        doc.save()
        print("Updated via ORM save().")

    # 3. VERIFICATION
    final_html = frappe.db.get_value("Print Format", fmt_name, "html")
    snippet = final_html[400:800] # Look at the header area
    
    print("\n--- FINAL DB CHECK ---")
    if "{{ doc.doctype" in final_html:
        print("✅ SUCCESS: DB contains '{{ doc.doctype'")
    elif "{ doc.doctype" in final_html:
        print("❌ FAILURE: DB contains '{ doc.doctype'")
    else:
        print("⚠️ WARNING: Could not find tag pattern. Dump:")
        print(snippet)

    # 4. Apply to ALL (if verifying passed)
    if "{{ doc.doctype" in final_html:
        targets = [
            "Quotation", "Sales Order", "Delivery Note", "Sales Invoice", 
            "Purchase Order", "Purchase Receipt", "Purchase Invoice", "Payment Entry", "Material Request"
        ]
        for doctype in targets:
            fname = f"Techxle {doctype} Format"
            if fname == fmt_name: continue
            
            # Clean old
            frappe.db.sql("DELETE FROM `tabPrint Format` WHERE doc_type=%s AND name LIKE 'Techxle%%' AND name != %s", (doctype, fname))

            # Update
            if not frappe.db.exists("Print Format", fname):
                d = frappe.new_doc("Print Format")
                d.name = fname
                d.doc_type = doctype
                d.standard = "No"
                d.custom_format = 1
                d.print_format_type = "Jinja"
                d.html = file_html
                d.save()
            else:
                d = frappe.get_doc("Print Format", fname)
                d.html = file_html
                d.save()
            print(f"Applied to {fname}")
        
    frappe.db.commit()
    print("Commited.")

if __name__ == "__main__":
    run()
