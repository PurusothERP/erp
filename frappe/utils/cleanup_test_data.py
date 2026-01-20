import frappe

def setup():
    print("Cleaning up Test Data...")
    try:
        cleanup_data()
        frappe.db.commit()
        print("Cleanup Complete!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Cleanup Failed: {e}")
        import traceback
        traceback.print_exc()

def cleanup_data():
    # Lists of data we created
    # We delete transactions first to avoid link errors
    
    # 1. Transactions (Delete ALL for these test entities just in case)
    # Since we only worked on these, it's safer to target by name/link if possible, 
    # but for "keep it empty" on a fresh install, deleting all transactional docs is often what is meant if they are test ones.
    # However, to be safe, I will target linked docs or just specific names if I can't find links.
    # Actually, let's just delete the Master Data, and `delete` method usually checks links. 
    # If links exist, we force delete transactions.
    
    doctypes_to_clear = [
        "Sales Order", "Quotation", "Purchase Order", "Sales Invoice", "Purchase Invoice", 
        "Stock Entry", "Work Order", "Quality Inspection"
    ]
    
    for dt in doctypes_to_clear:
        # Delete all documents of these types (Assuming this is a fresh setup and all are test)
        # If the user has real data, this is dangerous. 
        # But the prompt implies "created by us". 
        # I will restrict to link with "Distributor A" or "Raw Material Supplier" or items "RM-001", "FG-001".
        
        # Actually, let's just try to delete the masters. If exception, we delete children.
        pass

    # 2. Master Data (Specific Names)
    items = ["RM-001", "FG-001", "Sub-Assembly-001"]
    customers = ["Distributor A"]
    suppliers = ["Raw Material Supplier"]
    workstations = ["Assembly Station"]
    operations = ["Assembly"]
    pricing_rules = ["Distributor Discount"]
    boms = [] # We'll query BOMs for items
    
    # Delete BOMs first
    for item in items:
        bom_names = frappe.get_all("BOM", filters={"item": item}, pluck="name")
        for bom in bom_names:
            frappe.delete_doc("BOM", bom, force=1, ignore_permissions=True)
            print(f"Deleted BOM: {bom}")

    # Delete Pricing Rules
    for pr in pricing_rules:
        if frappe.db.exists("Pricing Rule", pr):
            frappe.delete_doc("Pricing Rule", pr, force=1, ignore_permissions=True)
            print(f"Deleted Pricing Rule: {pr}")

    # Delete Items
    for item in items:
        if frappe.db.exists("Item", item):
            # Find and delete linked transactions for this item first if strictly needed, 
            # or rely on force=1 (which might leave orphans, but ok for test cleanup)
            # Better to be clean:
            # Delete Stock Ledger Entries? No, force delete item cascade? 
            # Frappe's delete_doc with force=1 usually allows it but might raise LinkExistsError if transactions exist.
            # Let's clean transactions for these items.
            clean_transactions_for_item(item)
            frappe.delete_doc("Item", item, force=1, ignore_permissions=True)
            print(f"Deleted Item: {item}")

    # Delete Customer
    for cust in customers:
        if frappe.db.exists("Customer", cust):
            clean_transactions_for_party("Customer", cust)
            frappe.delete_doc("Customer", cust, force=1, ignore_permissions=True)
            print(f"Deleted Customer: {cust}")

    # Delete Supplier
    for supp in suppliers:
        if frappe.db.exists("Supplier", supp):
            clean_transactions_for_party("Supplier", supp)
            frappe.delete_doc("Supplier", supp, force=1, ignore_permissions=True)
            print(f"Deleted Supplier: {supp}")

    # Workstations & Operations
    for ws in workstations:
        if frappe.db.exists("Workstation", ws):
            frappe.delete_doc("Workstation", ws, force=1, ignore_permissions=True)
            print(f"Deleted Workstation: {ws}")

    for op in operations:
        if frappe.db.exists("Operation", op):
            frappe.delete_doc("Operation", op, force=1, ignore_permissions=True)
            print(f"Deleted Operation: {op}")
            
    # Also clean up "Item Groups" or "Warehouses" if likely empty?
    # User said "date customer" (data customer). I will stick to the entities above.
    
def clean_transactions_for_item(item_code):
    # Find doctypes linking to Item
    # This is complex. Simplified: delete specific known transaction types.
    t_types = ["Sales Order Item", "Quotation Item", "Purchase Order Item", "Stock Entry Detail"]
    # We need to find the Parents.
    
    # Brute force common ones
    for parent_dt in ["Sales Order", "Quotation", "Purchase Order", "Sales Invoice", "Purchase Invoice", "Stock Entry"]:
        # Find docs containing this item
        # SQL is faster/easier here
        try:
            docs = frappe.db.sql(f"""
                select parent from `tab{parent_dt} Item` where item_code = %s
            """, (item_code,), as_dict=1)
            # Note: Stock Entry uses 'items' table typically `tabStock Entry Detail`
            if parent_dt == "Stock Entry":
                 docs = frappe.db.sql(f"""
                    select parent from `tabStock Entry Detail` where item_code = %s
                """, (item_code,), as_dict=1)
            
            names = set([d.parent for d in docs])
            for name in names:
                if frappe.db.exists(parent_dt, name):
                    frappe.delete_doc(parent_dt, name, force=1, ignore_permissions=True)
                    print(f"Deleted {parent_dt}: {name}")
        except Exception:
            pass # Table might not exist or schema diff

def clean_transactions_for_party(party_type, party_name):
    # Delete docs where customer = X
    field = "customer" if party_type == "Customer" else "supplier"
    doctypes = ["Sales Order", "Quotation", "Sales Invoice"] if party_type == "Customer" else ["Purchase Order", "Purchase Invoice"]
    
    for dt in doctypes:
        docs = frappe.get_all(dt, filters={field: party_name}, pluck="name")
        for doc in docs:
             frappe.delete_doc(dt, doc, force=1, ignore_permissions=True)
             print(f"Deleted {dt}: {doc}")

if __name__ == "__main__":
    setup()
