import frappe

def setup():
    print("Starting Total GL Wipe (Deleting ALL GL Entries)...")
    try:
        wipe_all_gl()
        frappe.db.commit()
        print("Total GL Wipe Complete!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Cleanup Failed: {e}")
        import traceback
        traceback.print_exc()

def wipe_all_gl():
    # 1. Delete ALL GL Entries
    # Fetching all IDs
    gl_entries = frappe.get_all("GL Entry", pluck="name")
    print(f"Found {len(gl_entries)} GL Entries. Deleting...")
    
    # We use frappe.delete_doc for safety hooks, but loop might be slow if thousands.
    # Given the screenshot shows ~12, loop is fine.
    
    for gl in gl_entries:
        try:
            frappe.delete_doc("GL Entry", gl, force=1, ignore_permissions=True)
            print(f" - Deleted GL: {gl}")
        except Exception as e:
            print(f" ! Failed to delete GL {gl}: {e}")

    # 2. Delete ALL Stock Ledger Entries
    # Often related to GL
    sles = frappe.get_all("Stock Ledger Entry", pluck="name")
    if sles:
        print(f"Found {len(sles)} Stock Ledger Entries. Deleting...")
        for sle in sles:
            try:
                frappe.delete_doc("Stock Ledger Entry", sle, force=1, ignore_permissions=True)
                print(f" - Deleted SLE: {sle}")
            except Exception as e:
                print(f" ! Failed to delete SLE {sle}: {e}")

if __name__ == "__main__":
    setup()
