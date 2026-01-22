import frappe

def run():
    # The user is getting "Format not found" because the default is pointing to an old/deleted name.
    # We need to update the 'default_print_format' field in the DocType (or Property Setter).
    
    targets = [
        "Quotation", "Sales Order", "Delivery Note", "Sales Invoice", 
        "Purchase Order", "Purchase Receipt", "Purchase Invoice", "Payment Entry", "Material Request"
    ]
    
    for doctype in targets:
        valid_format = f"Techxle {doctype} Format"
        
        # 1. Update the actual DocType property (for standard persistence)
        # We use Property Setter to avoid modifying standard JSONs if possible, 
        # but for defaults, direct DB update is often more reliable in local setups.
        
        # Check if Property Setter exists for this
        frappe.make_property_setter({
            "doctype": doctype,
            "doctype_or_field": "DocType",
            "property": "default_print_format",
            "value": valid_format
        })
        
        print(f"Set Default for {doctype} -> {valid_format}")

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: All Default Formats updated to new Techxle versions.")

if __name__ == "__main__":
    run()
