import frappe

def run():
    pf_name = "Techxle Sales Invoice Format"
    if frappe.db.exists("Print Format", pf_name):
        content = frappe.db.get_value("Print Format", pf_name, "html")
        with open("debug_print.txt", "w") as f:
            f.write(content)
        print(f"Dumped content of {pf_name} to debug_print.txt")
    else:
        print(f"{pf_name} not found")

if __name__ == "__main__":
    run()
