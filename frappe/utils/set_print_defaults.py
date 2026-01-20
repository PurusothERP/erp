import frappe

def setup():
    print("Setting Techxle Print Formats as Default...")
    try:
        set_defaults()
        frappe.db.commit()
        print("Defaults Set Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Failed to set defaults: {e}")
        import traceback
        traceback.print_exc()

def set_defaults():
    # Map DocType to Print Format Name (created in V4)
    mapping = {
        "Sales Invoice": "Techxle SalesInvoice",
        "Sales Order": "Techxle SalesOrder",
        "Purchase Order": "Techxle PurchaseOrder"
    }
    
    for doctype, format_name in mapping.items():
        if frappe.db.exists("Print Format", format_name):
            print(f"Setting default for {doctype} -> {format_name}")
            
            # Method 1: Property Setter (Best Practice for overrides)
            frappe.make_property_setter({
                "doctype": doctype,
                "doctype_or_field": "DocType",
                "property": "default_print_format",
                "value": format_name,
                "property_type": "Data"
            })
            
            # Method 2: Customize Form (Fallback if property setter doesn't strictly take priority in view)
            # Fetch custom doc perm doesn't usually handle this, Property Setter is the core way.
        else:
            print(f"Warning: Print Format '{format_name}' not found. Skipping.")

if __name__ == "__main__":
    setup()
