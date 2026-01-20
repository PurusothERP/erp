import frappe

def setup():
    print("Starting Cleanup V5 (Fixing previous rollback)...")
    try:
        delete_cancelled_documents()
        frappe.db.commit() # COMMIT HERE to ensure invoices are gone even if next step fails
        print("Cancelled documents deleted and committed.")
        
        cleanup_orphaned_customers()
        frappe.db.commit()
        print("Customers cleaned and committed.")
        
        print("Cleanup V5 Complete!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Cleanup Failed: {e}")
        import traceback
        traceback.print_exc()

def delete_cancelled_documents():
    doctypes = [
        "Sales Invoice", "Sales Order", "Delivery Note", "Quotation",
        "Purchase Invoice", "Purchase Order", "Purchase Receipt", "Supplier Quotation",
        "Material Request", "Stock Entry", "Work Order", "Payment Entry",
        "Journal Entry"
    ]
    
    for dt in doctypes:
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
    test_customers = ["Axle", "Distributor A", "Test Customer", "Test", "Customer 1"]
    
    for cust in test_customers:
        if frappe.db.exists("Customer", cust):
            print(f"Checking Customer: {cust}")
            has_links = False
            
            # Check Sales Invoice/Order (uses 'customer')
            for dt in ["Sales Invoice", "Sales Order", "Delivery Note"]:
                if frappe.get_all(dt, filters={"customer": cust, "docstatus": ["<", 2]}):
                    has_links = True
                    print(f" - Active {dt} found.")
                    break
            
            # Check Quotation (uses 'party_name')
            if not has_links:
                if frappe.get_all("Quotation", filters={"party_name": cust, "docstatus": ["<", 2]}):
                    has_links = True
                    print(f" - Active Quotation found.")

            if not has_links:
                try:
                    frappe.delete_doc("Customer", cust, force=1, ignore_permissions=True)
                    print(f" - Deleted Customer: {cust}")
                except Exception as e:
                    print(f" - Could not delete {cust}: {e}")
            else:
                print(f" - Skipping {cust} due to active links.")
                
if __name__ == "__main__":
    setup()
