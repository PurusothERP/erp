import frappe

def setup():
    print("Starting Cleanup V4 (Delete Cancelled & Orphans)...")
    try:
        delete_cancelled_documents()
        cleanup_orphaned_customers()
        frappe.db.commit()
        print("Cleanup V4 Complete!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Cleanup Failed: {e}")
        import traceback
        traceback.print_exc()

def delete_cancelled_documents():
    # List of doctypes to check for Cancelled docs (docstatus=2)
    doctypes = [
        "Sales Invoice", "Sales Order", "Delivery Note", "Quotation",
        "Purchase Invoice", "Purchase Order", "Purchase Receipt", "Supplier Quotation",
        "Material Request", "Stock Entry", "Work Order", "Payment Entry"
    ]
    
    for dt in doctypes:
        # Find all cancelled docs
        cancelled_docs = frappe.get_all(dt, filters={"docstatus": 2}, pluck="name")
        
        if cancelled_docs:
            print(f"Found {len(cancelled_docs)} Cancelled {dt}(s). Deleting...")
            for name in cancelled_docs:
                try:
                    frappe.delete_doc(dt, name, force=1, ignore_permissions=True)
                    print(f" - Deleted: {name}")
                except Exception as e:
                    print(f" ! Error deleting {name}: {e}")

def cleanup_orphaned_customers():
    # Specific cleanup for "Axle" or similar test customers
    test_customers = ["Axle", "Distributor A", "Test Customer"]
    
    for cust in test_customers:
        if frappe.db.exists("Customer", cust):
            # Double check if any transactions exist (Draft or Submitted)
            # If so, cleanup script might fail if not cancelled first.
            # But we assumed user wants this gone.
            
            # Check for any linked docs in common places
            has_links = False
            for dt in ["Sales Invoice", "Sales Order", "Quotation"]:
                if frappe.get_all(dt, filters={"customer": cust, "docstatus": ["<", 2]}):
                    has_links = True
                    print(f"Skipping {cust}: Has active {dt}")
                    break
            
            if not has_links:
                try:
                    frappe.delete_doc("Customer", cust, force=1, ignore_permissions=True)
                    print(f"Deleted Customer: {cust}")
                except Exception as e:
                    print(f"Could not delete Customer {cust}: {e}")

if __name__ == "__main__":
    setup()
