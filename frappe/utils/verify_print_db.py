import frappe

def run():
    name = "Techxle Sales Order Format"
    if not frappe.db.exists("Print Format", name):
        print(f"ERROR: {name} does not exist.")
        return

    val = frappe.db.get_value("Print Format", name, ["html", "custom_format", "print_format_type", "standard"], as_dict=True)
    
    print("-" * 30)
    print(f"Format: {name}")
    print(f"Custom Format: {val.custom_format}")
    print(f"Type: {val.print_format_type}")
    print(f"Standard: {val.standard}")
    print("-" * 30)
    
    snippet = val.html[:300] if val.html else "NONE"
    print("HTML HEAD:\n", snippet)
    
    if "{{ doc.doctype" in val.html:
        print("\n✅ SUCCESS: Found double braces '{{ doc.doctype'")
    elif "{ doc.doctype" in val.html:
        print("\n❌ FAILURE: Found single braces '{ doc.doctype' -> Jinja Broken!")
    else:
        print("\n❓ UNKNOWN pattern.")

if __name__ == "__main__":
    run()
