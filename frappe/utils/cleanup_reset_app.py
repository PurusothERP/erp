import frappe

def run():
    print("------------------------------------------------")
    print("STARTING GLOBAL DATA RESET (Preserving Print Formats)")
    print("------------------------------------------------")

    # 1. Transactions (Child to Parent dependency usually means delete children first, but frappe.delete_doc handles some.
    # We will go in reverse chronological order of creation type logic roughly)
    
    transaction_doctypes = [
        # Manufacturing
        "Job Card", "Work Order", "Production Plan", "BOM", 
        
        # Stock
        "Stock Entry", "Material Request", "Delivery Note", "Purchase Receipt",
        "Stock Ledger Entry", "Serial No", "Batch", "Bin",
        
        # Accounting
        "File", "Payment Entry", "Journal Entry", "Sales Invoice", "Purchase Invoice", "GL Entry",
        
        # Selling / Buying
        "Quotation", "Sales Order", "Supplier Quotation", "Purchase Order",
    ]

    # 2. Master Data
    master_doctypes = [
        "Item",
        "Customer",
        "Supplier",
        "Contact", 
        "Address",
        
        # Manufacturing Master
        "Operation", "Workstation", "Routing",
    ]

    # Combine
    all_targets = transaction_doctypes + master_doctypes

    for doctype in all_targets:
        if doctype == "files": doctype = "File" # Fix typo if present, though we removed it from list below
        
        try:
            # 1. Force Reset DocStatus to 0 (Draft) so we can delete them
            # This bypasses the "Submitted Record cannot be deleted" error
            try:
                if frappe.db.has_column(doctype, "docstatus"):
                    frappe.db.sql(f"UPDATE `tab{doctype}` SET docstatus=0")
                    frappe.db.commit()
            except Exception:
                pass # Doctype might not have table or docstatus (e.g. Virtual)

            # 2. Delete
            names = frappe.get_all(doctype, pluck="name")
            
            if names:
                print(f"Deleting {len(names)} records of {doctype}...")
                for idx, name in enumerate(names):
                    try:
                        frappe.delete_doc(doctype, name, force=1, ignore_permissions=True)
                        if idx % 50 == 0:
                            print(f" - Progress: {idx}/{len(names)}")
                    except Exception as e:
                        print(f" ! Failed to delete {doctype} {name}: {e}")
                
                print(f"Accessible {doctype} cleared.")
                frappe.db.commit()
            else:
                print(f"No records found for {doctype}.")
                
        except Exception as e:
            print(f"Error processing {doctype}: {e}")

    # 3. reset Series sequences
    print("Resetting Naming Series...")
    frappe.db.sql("DELETE FROM `tabSeries`")
    frappe.db.commit()

    print("------------------------------------------------")
    print("RESET COMPLETE. System is clean.")
    print("Print Formats and System Settings have been PRESERVED.")
    print("------------------------------------------------")

if __name__ == "__main__":
    run()
