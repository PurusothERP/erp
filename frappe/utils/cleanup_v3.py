import frappe

def setup():
    print("Starting Aggressive Data Cleanup V3...")
    try:
        cleanup_recursive()
        frappe.db.commit()
        print("Aggressive Cleanup V3 Complete!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Cleanup Failed: {e}")
        import traceback
        traceback.print_exc()

def cleanup_recursive():
    # 1. Clear Material Requests first (Downstream of SO)
    # They don't always have 'customer' field easily indexable in listview without join, 
    # so we search by item or get all if test data.
    # To be safe, we'll brute force check MRs linked to our items.
    test_items = ["RM-001", "FG-001", "Sub-Assembly-001"]
    for item in test_items:
        clean_docs_by_item("Material Request", item)
        clean_docs_by_item("Stock Entry", item)
        clean_docs_by_item("Work Order", item)
        
    # 2. Customers
    customers = ["Distributor A"]
    for cust in customers:
        process_customer_transactions(cust)
        
    # 3. Suppliers
    suppliers = ["Raw Material Supplier"]
    for supp in suppliers:
        process_supplier_transactions(supp)
        
    # 4. Master Data (Last)
    delete_masters(customers, suppliers, test_items)

def clean_docs_by_item(doctype, item_code):
    # Find docs where item is present in child table
    child_table = f"tab{doctype} Item" # Standard convention
    if doctype == "Stock Entry": child_table = "tabStock Entry Detail"
    
    try:
        # SQL to find parents
        parents = frappe.db.sql(f"""
            SELECT DISTINCT parent FROM `{child_table}` WHERE item_code = %s
        """, (item_code,), as_dict=True)
        
        for p in parents:
            cancel_and_delete(doctype, p.parent)
    except Exception:
        pass

def process_customer_transactions(customer):
    # Order: Payment -> Invoice -> Delivery -> Order -> Quote
    
    # 1. Payment Entry
    ps = frappe.get_all("Payment Entry", filters={"party_type": "Customer", "party": customer}, pluck="name")
    for p in ps: cancel_and_delete("Payment Entry", p)
    
    # 2. Sales Invoice
    sis = frappe.get_all("Sales Invoice", filters={"customer": customer}, pluck="name")
    for si in sis: cancel_and_delete("Sales Invoice", si)
    
    # 3. Delivery Note
    dns = frappe.get_all("Delivery Note", filters={"customer": customer}, pluck="name")
    for dn in dns: cancel_and_delete("Delivery Note", dn)
    
    # 4. Sales Order
    sos = frappe.get_all("Sales Order", filters={"customer": customer}, pluck="name")
    for so in sos: cancel_and_delete("Sales Order", so)
    
    # 5. Quotation (Uses party_name)
    qs = frappe.get_all("Quotation", filters={"party_name": customer}, pluck="name")
    for q in qs: cancel_and_delete("Quotation", q)

def process_supplier_transactions(supplier):
    # 1. Payment Entry
    ps = frappe.get_all("Payment Entry", filters={"party_type": "Supplier", "party": supplier}, pluck="name")
    for p in ps: cancel_and_delete("Payment Entry", p)
    
    # 2. Purchase Invoice
    pis = frappe.get_all("Purchase Invoice", filters={"supplier": supplier}, pluck="name")
    for pi in pis: cancel_and_delete("Purchase Invoice", pi)
    
    # 3. Purchase Receipt
    prs = frappe.get_all("Purchase Receipt", filters={"supplier": supplier}, pluck="name")
    for pr in prs: cancel_and_delete("Purchase Receipt", pr)
    
    # 4. Purchase Order
    pos = frappe.get_all("Purchase Order", filters={"supplier": supplier}, pluck="name")
    for po in pos: cancel_and_delete("Purchase Order", po)
    
    # 5. Supplier Quotation
    sqs = frappe.get_all("Supplier Quotation", filters={"supplier": supplier}, pluck="name")
    for sq in sqs: cancel_and_delete("Supplier Quotation", sq)

def delete_masters(customers, suppliers, items):
    # Pricing Rules
    pr_list = frappe.get_all("Pricing Rule", filters={"title": "Distributor Discount"}, pluck="name")
    for pr in pr_list:
        frappe.delete_doc("Pricing Rule", pr, force=1, ignore_permissions=True)

    # Items & BOMs
    for item in items:
        # Check Linked BOMs again
        boms = frappe.get_all("BOM", filters={"item": item}, pluck="name")
        for bom in boms: cancel_and_delete("BOM", bom)
        
        if frappe.db.exists("Item", item):
            frappe.delete_doc("Item", item, force=1, ignore_permissions=True)
            print(f"Deleted Item: {item}")

    # Customers
    for cust in customers:
        if frappe.db.exists("Customer", cust):
            frappe.delete_doc("Customer", cust, force=1, ignore_permissions=True)
            print(f"Deleted Customer: {cust}")

    # Suppliers
    for supp in suppliers:
        if frappe.db.exists("Supplier", supp):
            frappe.delete_doc("Supplier", supp, force=1, ignore_permissions=True)
            print(f"Deleted Supplier: {supp}")

    # Clean Workstations/Ops
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
