import frappe
from frappe.model.naming import make_autoname

def setup():
    print("Starting Forced Data Cleanup (Cancel & Delete)...")
    try:
        cleanup_force()
        frappe.db.commit()
        print("Forced Cleanup Complete!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Cleanup Failed: {e}")
        import traceback
        traceback.print_exc()

def cleanup_force():
    # Targets
    customers = ["Distributor A"]
    suppliers = ["Raw Material Supplier"]
    items = ["RM-001", "FG-001", "Sub-Assembly-001"]
    
    # Doctype Order: Children/Dependents first
    # Stock Entry -> Invoice -> Delivery/Receipt -> Order -> Quotation
    
    # 1. Cancel & Delete Transactions for Customers
    for cust in customers:
        process_linked_docs("Customer", cust)
        
    # 2. Cancel & Delete Transactions for Suppliers
    for supp in suppliers:
        process_linked_docs("Supplier", supp)
        
    # 3. Cancel & Delete Stock Transactions (for Items)
    # This catches manufacturing entries not linked directly to Customer/Supplier
    for item in items:
        process_stock_entries(item)

    # 4. Delete Manufacturing Records (Work Order, BOM)
    # Work Orders often link to Stock Entries (handled above hopefully)
    # We might need to handle Work Orders specifically
    process_manufacturing(items)

    # 5. Delete Master Data
    delete_masters(customers, suppliers, items)

def process_linked_docs(party_type, party_name):
    print(f"Processing transactions for {party_type}: {party_name}")
    
    # Map fields
    party_field = "customer" if party_type == "Customer" else "supplier"
    
    # Order matters: Downstream first
    # Payment Entry?
    # Journal Entry?
    # Sales Invoice / Purchase Invoice
    # Delivery Note / Purchase Receipt
    # Sales Order / Purchase Order
    # Quotation / Supplier Quotation
    
    doctypes = []
    if party_type == "Customer":
        doctypes = ["Payment Entry", "Sales Invoice", "Delivery Note", "Sales Order", "Quotation"]
    else:
        doctypes = ["Payment Entry", "Purchase Invoice", "Purchase Receipt", "Purchase Order", "Supplier Quotation"]
        
    for dt in doctypes:
        # Find docs
        filters = {party_field: party_name}
        if dt == "Payment Entry":
            filters = {"party_type": party_type, "party": party_name}
            
        docs = frappe.get_all(dt, filters=filters, pluck="name")
        for name in docs:
            cancel_and_delete(dt, name)

def process_stock_entries(item_code):
    # Find Stock Entries containing this item
    # This is a bit heavier, using SQL to find parent
    try:
        entries = frappe.db.sql(f"""
            select distinct parent from `tabStock Entry Detail` 
            where item_code = %s
        """, (item_code,), as_dict=True)
        
        for e in entries:
            cancel_and_delete("Stock Entry", e.parent)
    except Exception:
        pass

def process_manufacturing(items):
    # Linked to items usually
    for item in items:
        # Work Orders
        wos = frappe.get_all("Work Order", filters={"production_item": item}, pluck="name")
        for wo in wos:
            # Check for Stock Entries linked to this WO not yet deleted?
            # Usually they are deleted if we found them via item, but let's be safe.
            # Cancel WO
            cancel_and_delete("Work Order", wo)
            
        # BOMs
        boms = frappe.get_all("BOM", filters={"item": item}, pluck="name")
        for bom in boms:
            cancel_and_delete("BOM", bom)

def delete_masters(customers, suppliers, items):
    # Pricing Rules
    pr_list = frappe.get_all("Pricing Rule", filters={"title": "Distributor Discount"}, pluck="name")
    for pr in pr_list:
        frappe.delete_doc("Pricing Rule", pr, force=1, ignore_permissions=True)
        print(f"Deleted Pricing Rule: {pr}")

    # Items
    for item in items:
        if frappe.db.exists("Item", item):
            frappe.delete_doc("Item", item, force=1, ignore_permissions=True)
            print(f"Deleted Item: {item}")

    # Customer
    for cust in customers:
        if frappe.db.exists("Customer", cust):
            frappe.delete_doc("Customer", cust, force=1, ignore_permissions=True)
            print(f"Deleted Customer: {cust}")

    # Supplier
    for supp in suppliers:
        if frappe.db.exists("Supplier", supp):
            frappe.delete_doc("Supplier", supp, force=1, ignore_permissions=True)
            print(f"Deleted Supplier: {supp}")
            
    # Workstations & Operations
    for ws in ["Assembly Station", "Packing Station"]:
        if frappe.db.exists("Workstation", ws):
             frappe.delete_doc("Workstation", ws, force=1, ignore_permissions=True)
             
    for op in ["Assembly", "Quality Check", "Packing"]:
        if frappe.db.exists("Operation", op):
            frappe.delete_doc("Operation", op, force=1, ignore_permissions=True)

def cancel_and_delete(doctype, name):
    if not frappe.db.exists(doctype, name):
        return

    try:
        doc = frappe.get_doc(doctype, name)
        
        # 1. Cancel if submitted
        if doc.docstatus == 1:
            print(f"Cancelling {doctype}: {name}")
            doc.cancel()
            
        # 2. Delete
        print(f"Deleting {doctype}: {name}")
        frappe.delete_doc(doctype, name, force=1, ignore_permissions=True)
        
    except Exception as e:
        print(f"Error handling {doctype} {name}: {e}")
        # Sometimes one link prevents another.
        # We try to proceed.

if __name__ == "__main__":
    setup()
