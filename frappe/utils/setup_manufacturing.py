import frappe
from frappe.utils import flt

def setup():
    print("Setting up Manufacturing ERP...")

    try:
        setup_domains()
        setup_global_defaults()
        company = get_company()
        setup_warehouses(company)
        setup_item_groups()
        setup_taxes(company)
        setup_contacts()
        setup_manufacturing_data(company)
        setup_quality_control()
        
        frappe.db.commit()
        print("Setup completed successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()

def get_company():
    companies = frappe.get_all("Company")
    if not companies:
        doc = frappe.get_doc({
            "doctype": "Company",
            "company_name": "My Manufacturing Company",
            "abbr": "MMC",
            "default_currency": "INR",
            "country": "India"
        }).insert(ignore_permissions=True)
        return doc.name
    return companies[0].name

def setup_domains():
    print("Enabling Domains...")
    domain_settings = frappe.get_single("Domain Settings")
    
    # Get standard available domains from DB
    valid_domains = [d.name for d in frappe.get_all("Domain")]
    print(f"Valid Domains in DB: {valid_domains}")
    
    target_domains = ["Manufacturing", "Retail", "Stock", "Buying", "Selling", "Quality", "Accounts", "CRM"]
    domains_to_set = [d for d in target_domains if d in valid_domains]
    
    domain_settings.set("active_domains", [])
    for d in domains_to_set:
        domain_settings.append("active_domains", {"domain": d})
    
    if domains_to_set:
        domain_settings.save(ignore_permissions=True)

def setup_global_defaults():
    print("Setting Global Defaults...")
    sys_settings = frappe.get_single("System Settings")
    sys_settings.setup_complete = 1
    sys_settings.save(ignore_permissions=True)

def setup_warehouses(company):
    print("Creating Warehouses...")
    warehouses = ["Stores - RM", "Stores - WIP", "Stores - FG", "Stores - Scrap"]
    parent_warehouse = frappe.get_value("Warehouse", {"company": company, "is_group": 1}, "name")
    
    if not parent_warehouse:
        abbr = frappe.get_cached_value('Company',  company,  'abbr')
        parent_warehouse_name = f"All Warehouses - {abbr}"
        if not frappe.db.exists("Warehouse", parent_warehouse_name):
             frappe.get_doc({
                 "doctype": "Warehouse",
                 "warehouse_name": "All Warehouses",
                 "is_group": 1,
                 "company": company
             }).insert(ignore_permissions=True)
        parent_warehouse = parent_warehouse_name

    for wh_name in warehouses:
        if not frappe.db.exists("Warehouse", {"warehouse_name": wh_name, "company": company}):
            doc = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh_name,
                "parent_warehouse": parent_warehouse,
                "company": company
            })
            try:
                doc.insert(ignore_permissions=True)
            except Exception as e:
                print(f"Warning: Could not create warehouse {wh_name}: {e}")

def setup_item_groups():
    print("Creating Item Groups...")
    groups = ["Raw Material", "Sub-Assembly", "Finished Goods", "Consumables", "Services"]
    
    if not frappe.db.exists("Item Group", "All Item Groups"):
         frappe.get_doc({"doctype": "Item Group", "item_group_name": "All Item Groups", "is_group": 1}).insert(ignore_permissions=True)

    for group in groups:
        if not frappe.db.exists("Item Group", group):
            frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": group,
                "parent_item_group": "All Item Groups",
                "is_group": 0
            }).insert(ignore_permissions=True)

def setup_taxes(company):
    print("Creating GST Tax Templates...")
    abbr = frappe.get_cached_value('Company',  company,  'abbr')
    parent_account = frappe.get_value("Account", {"account_name": "Duties and Taxes", "company": company, "is_group": 1}, "name")
    if not parent_account:
        parent_account = frappe.get_value("Account", {"account_type": "Tax", "company": company, "is_group": 1}, "name")

    tax_account_name = f"Output GST 5% - {abbr}"
    if parent_account and not frappe.db.exists("Account", tax_account_name):
        try:
            frappe.get_doc({
                "doctype": "Account",
                "account_name": "Output GST 5%",
                "parent_account": parent_account,
                "company": company,
                "account_type": "Tax",
                "tax_rate": 5
            }).insert(ignore_permissions=True)
        except Exception:
            pass
            
    account_head = frappe.get_value("Account", {"account_name": ["like", "%GST%"], "company": company}, "name")
    if account_head:
        if not frappe.db.exists("Sales Taxes and Charges Template", {"title": "GST 5%", "company": company}):
            frappe.get_doc({
                "doctype": "Sales Taxes and Charges Template",
                "title": "GST 5%",
                "company": company,
                "taxes": [{
                    "charge_type": "On Net Total",
                    "account_head": account_head,
                    "rate": 5,
                    "description": "GST 5%"
                }]
            }).insert(ignore_permissions=True)

        if not frappe.db.exists("Purchase Taxes and Charges Template", {"title": "GST 5%", "company": company}):
            frappe.get_doc({
                "doctype": "Purchase Taxes and Charges Template",
                "title": "GST 5%",
                "company": company,
                "taxes": [{
                    "charge_type": "On Net Total",
                    "account_head": account_head,
                    "rate": 5,
                    "description": "GST 5%"
                }]
            }).insert(ignore_permissions=True)

def setup_contacts():
    print("Creating Customers and Suppliers...")
    if not frappe.db.exists("Customer", "Distributor A"):
        frappe.get_doc({"doctype": "Customer", "customer_name": "Distributor A", "customer_group": "Commercial", "territory": "All Territories"}).insert(ignore_permissions=True)
    if not frappe.db.exists("Supplier", "Vendor X"):
        frappe.get_doc({"doctype": "Supplier", "supplier_name": "Vendor X", "supplier_group": "Local"}).insert(ignore_permissions=True)

def setup_manufacturing_data(company):
    print("Creating Operations and Workstations...")
    ops = ["Assembly", "Quality Check", "Packing"]
    for op in ops:
        if not frappe.db.exists("Operation", op):
            frappe.get_doc({"doctype": "Operation", "name": op}).insert(ignore_permissions=True)

    ws = ["Assembly Station", "Packing Station"]
    for w in ws:
        if not frappe.db.exists("Workstation", w):
            frappe.get_doc({"doctype": "Workstation", "workstation_name": w}).insert(ignore_permissions=True)

    print("Creating Items...")
    if not frappe.db.exists("Item", "RM-001"):
        frappe.get_doc({
            "doctype": "Item",
            "item_code": "RM-001",
            "item_name": "Raw Material 1",
            "item_group": "Raw Material",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "valuation_rate": 100
        }).insert(ignore_permissions=True)
    
    if not frappe.db.exists("Item", "FG-001"):
        def_wh = f"Stores - FG - {frappe.get_cached_value('Company', company, 'abbr')}"
        if not frappe.db.exists("Warehouse", def_wh):
             def_wh = frappe.get_value("Warehouse", {"warehouse_name": "Stores - FG", "company": company}, "name")

        frappe.get_doc({
            "doctype": "Item",
            "item_code": "FG-001",
            "item_name": "Finished Good 1",
            "item_group": "Finished Goods",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "default_warehouse": def_wh
        }).insert(ignore_permissions=True)

    print("Creating BOM...")
    if not frappe.db.exists("BOM", {"item": "FG-001"}):
        frappe.get_doc({
            "doctype": "BOM",
            "item": "FG-001",
            "quantity": 1,
            "with_operations": 1,
            "items": [{"item_code": "RM-001", "qty": 1}],
            "operations": [{"operation": "Assembly", "workstation": "Assembly Station", "time_in_mins": 30}]
        }).insert(ignore_permissions=True)

def setup_quality_control():
    print("Creating Quality Inspection Template...")
    if not frappe.db.exists("Quality Inspection Parameter", "Scratch Test"):
         frappe.get_doc({
             "doctype": "Quality Inspection Parameter",
             "parameter": "Scratch Test",
             "description": "Check for visible scratches"
         }).insert(ignore_permissions=True)

    if not frappe.db.exists("Quality Inspection Template", "Visual Check"):
        frappe.get_doc({
            "doctype": "Quality Inspection Template",
            "quality_inspection_template_name": "Visual Check",
            "item_quality_inspection_parameter": [{"specification": "Scratch Test", "acceptance_formula": "reading == 'Pass'"}]
        }).insert(ignore_permissions=True)
