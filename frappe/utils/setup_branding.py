import frappe

def setup():
    print("Setting up Techxle Branding...")
    try:
        rename_company()
        update_website_settings()
        create_website_theme() # New
        create_bilingual_print_format()
        frappe.db.commit()
        print("Branding Setup Successful!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Branding Setup Failed: {e}")
        import traceback
        traceback.print_exc()

def rename_company():
    new_name = "Techxle CRM"
    companies = frappe.get_all("Company")
    if not companies: return

    old_name = companies[0].name
    if old_name == new_name: return

    print(f"Renaming Company '{old_name}' to '{new_name}'...")
    frappe.rename_doc("Company", old_name, new_name, force=True)

def update_website_settings():
    print("Updating Website & System Settings...")
    logo_path = "/files/techxle_logo.jpg"
    
    # Website Settings
    ws = frappe.get_single("Website Settings")
    ws.app_title = "Techxle CRM"
    ws.app_name = "Techxle CRM"
    ws.app_logo = logo_path
    ws.banner_image = logo_path
    ws.splash_image = logo_path
    ws.save(ignore_permissions=True)
    
    # Navbar Settings (if available in this version/setup)
    try:
        nbs = frappe.get_single("Navbar Settings")
        nbs.app_logo = logo_path
        nbs.save(ignore_permissions=True)
    except:
        print("Navbar Settings not found or not updateable.")

def create_website_theme():
    print("Creating Website Theme 'Techxle Dark'...")
    theme_name = "Techxle Dark"
    if not frappe.db.exists("Website Theme", theme_name):
        doc = frappe.get_doc({
            "doctype": "Website Theme",
            "theme": theme_name,
            "primary": "#003366", # Dark Blue
            "text": "#ffffff",
            "background": "#f0f4f8",
            "custom": 1
        }).insert(ignore_permissions=True)
    else:
        doc = frappe.get_doc("Website Theme", theme_name)
        doc.primary = "#003366"
        doc.save(ignore_permissions=True)
    
    # Set as default theme
    ws = frappe.get_single("Website Settings")
    ws.website_theme = theme_name
    ws.save(ignore_permissions=True)

def create_bilingual_print_format():
    print("Creating Bilingual Print Format...")
    logo_html = '<img src="/files/techxle_logo.jpg" style="max-width: 150px; float: left; margin-right: 20px;">'
    
    html = f"""
<div style="font-family: Arial, sans-serif; direction: ltr;">
    <div style="text-align: center; margin-bottom: 20px; overflow: hidden;">
        {logo_html}
        <div style="display: inline-block;">
            <h2>{{{{ doc.company }}}}</h2>
            <h3>{{{{ doc.doctype }}}} / {{{{ doc.doctype == 'Sales Invoice' and 'فاتورة المبيعات' or 'عرض سعر' }}}}</h3>
        </div>
    </div>

    <table class="table table-bordered table-condensed">
        <thead>
            <tr>
                <th style="width: 5%">Sr<br>م</th>
                <th style="width: 50%">Item / Description<br>الصنف / الوصف</th>
                <th style="width: 15%; text-align: right;">Qty<br>الكمية</th>
                <th style="width: 15%; text-align: right;">Rate<br>السعر</th>
                <th style="width: 15%; text-align: right;">Amount<br>المبلغ</th>
            </tr>
        </thead>
        <tbody>
            {{% for item in doc.items %}}
            <tr>
                <td>{{{{ loop.index }}}}</td>
                <td>
                    <b>{{{{ item.item_code }}}}</b><br>
                    {{{{ item.description }}}}
                </td>
                <td style="text-align: right;">{{{{ item.qty }}}}</td>
                <td style="text-align: right;">{{{{ item.get_formatted("rate") }}}}</td>
                <td style="text-align: right;">{{{{ item.get_formatted("amount") }}}}</td>
            </tr>
            {{% endfor %}}
        </tbody>
        <tfoot>
            <tr>
                <td colspan="4" style="text-align: right;"><b>Total / المجموع</b></td>
                <td style="text-align: right;">{{{{ doc.get_formatted("grand_total") }}}}</td>
            </tr>
             <tr>
                 <td colspan="5">
                    <b>In Words:</b> {{{{ doc.in_words }}}}<br>
                 </td>
            </tr>
        </tfoot>
    </table>
</div>
    """

    pf_name = "Techxle Bilingual"
    if not frappe.db.exists("Print Format", pf_name):
        doc = frappe.get_doc({
            "doctype": "Print Format",
            "name": pf_name,
            "standard": "No",
            "custom_format": 1,
            "print_format_type": "Jinja",
            "doc_type": "Sales Invoice", 
            "html": html
        }).insert(ignore_permissions=True)
        print(f"Created Print Format: {pf_name}")
    else:
        doc = frappe.get_doc("Print Format", pf_name)
        doc.html = html
        doc.save(ignore_permissions=True)
        print(f"Updated Print Format: {pf_name}")

if __name__ == "__main__":
    setup()
