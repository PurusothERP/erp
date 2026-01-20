import frappe

def verify():
    print("Verifying Manufacturing Setup...")
    
    # Check Warehouses
    whs = ["Stores - RM", "Stores - WIP", "Stores - FG", "Stores - Scrap"]
    all_wh_ok = True
    company = frappe.get_all("Company")[0].name
    
    for w in whs:
        # Search by warehouse name and company
        exists = frappe.db.exists("Warehouse", {"warehouse_name": w, "company": company})
        status = "OK" if exists else "MISSING"
        print(f"Warehouse '{w}': {status}")
        if not exists: all_wh_ok = False

    # Check Items
    items = ["RM-001", "FG-001"]
    all_items_ok = True
    for i in items:
        exists = frappe.db.exists("Item", i)
        status = "OK" if exists else "MISSING"
        print(f"Item '{i}': {status}")
        if not exists: all_items_ok = False

    # Check BOM
    bom = frappe.db.get_value("BOM", {"item": "FG-001"}, "name")
    print(f"BOM for FG-001: {bom if bom else 'MISSING'}")

    # Check QC Template
    qc = frappe.db.exists("Quality Inspection Template", "Visual Check")
    print(f"QC Template 'Visual Check': {'OK' if qc else 'MISSING'}")
    
    if all_wh_ok and all_items_ok and bom and qc:
        print("VERIFICATION SUCCESSFUL")
    else:
        print("VERIFICATION FAILED")
