import frappe

def setup():
    print("Starting Cleanup V6: Nuclear GL Scrub...")
    try:
        cleanup_gl_entries()
        cleanup_stock_ledger()
        cleanup_orphans()
        frappe.db.commit()
        print("Nuclear GL Scrub Complete!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Cleanup Failed: {e}")
        import traceback
        traceback.print_exc()

def cleanup_gl_entries():
    # 1. Delete GL Entries for Axle
    # GL Entries link to party via `party_type` and `party` OR `voucher_no`
    
    customers = ["Axle", "Distributor A", "Test Customer"]
    
    for cust in customers:
        # Find by Party
        gls = frappe.get_all("GL Entry", filters={"party_type": "Customer", "party": cust}, pluck="name")
        if gls:
            print(f"Found {len(gls)} GL Entries for {cust}. Deleting...")
            for gl in gls:
                try:
                    frappe.delete_doc("GL Entry", gl, force=1, ignore_permissions=True)
                    print(f" - Deleted GL: {gl}")
                except Exception as e:
                    print(f" ! Error deleting GL {gl}: {e}")

def cleanup_stock_ledger():
    # Sometimes Stock Ledger Entries also block deletion
    # They don't have Party usually, but voucher does.
    # Since we deleted vouchers (Invoices/Delivery Notes), SLEs might be hanging if force deleted? 
    # Usually they go with parent. But let's check orphan SLEs if needed.
    # Avoiding for now as user error was specifically GL Entry.
    pass

def cleanup_orphans():
    customers = ["Axle", "Distributor A"]
    
    for cust in customers:
        if frappe.db.exists("Customer", cust):
            print(f"Attempting to delete Customer: {cust}")
            # Try delete again
            try:
                frappe.delete_doc("Customer", cust, force=1, ignore_permissions=True)
                print(f" - Deleted Customer: {cust}")
            except Exception as e:
                print(f" - Failed to delete {cust}: {e}")
                
    # Also clean Address/Contact linked to these?
    # Addresses
    for cust in customers:
        links = frappe.get_all("Dynamic Link", filters={"link_doctype": "Customer", "link_name": cust}, fields=["parent", "parenttype"])
        for link in links:
            if link.parenttype in ["Address", "Contact"]:
                print(f"Deleting {link.parenttype}: {link.parent}")
                try:
                    frappe.delete_doc(link.parenttype, link.parent, force=1, ignore_permissions=True)
                except Exception:
                    pass

if __name__ == "__main__":
    setup()
