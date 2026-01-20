import frappe
import base64
import os

def setup():
    print("Applying V4 Print Polish & Company Rename...")
    try:
        rename_company()
        create_all_formats()
        frappe.db.commit()
        print("V4 Polish Applied Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"V4 Update Failed: {e}")
        import traceback
        traceback.print_exc()

def rename_company():
    target_name = "Techxle Consultancy Private Limited"
    # Search for any company that contains 'Techxle' to find the current one
    current_companies = frappe.get_all("Company", filters={"name": ["like", "Techxle%"]})
    
    if current_companies:
        current_name = current_companies[0].name
        if current_name == target_name:
            print(f"Company already named '{target_name}'")
        else:
            print(f"Renaming '{current_name}' to '{target_name}'...")
            frappe.rename_doc("Company", current_name, target_name, force=True)
            # Update Setup Values if needed (e.g. Website Settings)
            frappe.db.set_value("Website Settings", None, "app_title", "Techxle Consultancy")
    else:
        print("No 'Techxle' company found to rename.")

def create_all_formats():
    # 1. Get Base64 Logo
    logo_path = "/Users/purusothaman/Desktop/erpnext/erpnext-bench/sites/site1.local/public/files/techxle_logo.jpg"
    img_src = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
            img_src = f"data:image/jpeg;base64,{base64_string}"

    branding_color = "#003366"

    # 2. Compact HTML Template
    html_template = f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #444; font-size: 11px; line-height: 1.3;">
        
        <!-- Header: Compact Side-by-Side -->
        <table style="width: 100%; border-bottom: 2px solid {branding_color}; padding-bottom: 5px; margin-bottom: 10px;">
            <tr>
                <td style="width: 40%; vertical-align: middle;">
                    <img src="{img_src}" style="max-height: 60px; width: auto;">
                </td>
                <td style="width: 60%; text-align: right; vertical-align: middle;">
                    <h2 style="color: {branding_color}; margin: 0; font-size: 18px;">Techxle Consultancy Private Limited</h2>
                    <p style="margin: 2px 0; font-size: 10px; color: #666;">
                        {{{{ doc.company_address_display or "" }}}}
                    </p>
                </td>
            </tr>
        </table>

        <!-- Document Title Bar: Very specific and colorful -->
        <div style="background-color: {branding_color}; color: white; padding: 5px 10px; margin-bottom: 15px; border-radius: 3px;">
            <table style="width: 100%;">
                <tr>
                    <td style="font-size: 14px; font-weight: bold;">
                        {{{{ doc.doctype.upper() }}}}
                    </td>
                    <td style="text-align: right; font-size: 12px;">
                        <strong>Date:</strong> {{{{ doc.get_formatted("transaction_date") or doc.get_formatted("date") }}}} &nbsp;|&nbsp; <strong># {{{{ doc.name }}}}</strong>
                    </td>
                </tr>
            </table>
        </div>

        <!-- Info Grid: Minimized whitespace -->
        <table style="width: 100%; margin-bottom: 15px;">
            <tr>
                <td style="width: 50%; vertical-align: top; border-right: 1px dotted #ccc; padding-right: 10px;">
                    <span style="color: {branding_color}; font-weight: bold; font-size: 10px; text-transform: uppercase;">To / Customer</span>
                    <h4 style="margin: 2px 0; font-size: 12px;">{{{{ doc.customer_name or doc.supplier_name }}}}</h4>
                    <!-- Clean Address Display: Truncate if too long -->
                    <div style="font-size: 10px;">{{{{ doc.address_display or "" }}}}</div>
                </td>
                <td style="width: 50%; vertical-align: top; padding-left: 10px;">
                    <table style="width: 100%; font-size: 10px;">
                         <tr>
                            <td style="width: 40%; color: #666;">Reference</td>
                            <td style="font-weight: bold;">{{{{ doc.po_no or doc.supplier_quotation or "-" }}}}</td>
                        </tr>
                        <tr>
                            <td style="color: #666;">Payment Terms</td>
                            <td>{{{{ doc.payment_terms_template or "Standard" }}}}</td>
                        </tr>
                        <tr>
                            <td style="color: #666;">Status</td>
                            <td>{{{{ doc.status }}}}</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Items Table: Compact Padding -->
        <table class="table table-bordered" style="width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 10px;">
            <thead>
                <tr style="background-color: #f0f4f8; color: {branding_color};">
                    <th style="padding: 4px; border: 1px solid #ddd; width: 5%;">Sr</th>
                    <th style="padding: 4px; border: 1px solid #ddd; width: 50%;">Description (الصنف)</th>
                    <th style="padding: 4px; border: 1px solid #ddd; width: 10%; text-align: right;">Qty</th>
                    <th style="padding: 4px; border: 1px solid #ddd; width: 15%; text-align: right;">Rate</th>
                    <th style="padding: 4px; border: 1px solid #ddd; width: 20%; text-align: right;">Amount</th>
                </tr>
            </thead>
            <tbody>
                {{% for item in doc.items %}}
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 4px; text-align: center;">{{{{ loop.index }}}}</td>
                    <td style="padding: 4px;">
                        <strong style="color: #333;">{{{{ item.item_code }}}}</strong>
                        <div style="color: #666;">{{{{ item.description }}}}</div>
                    </td>
                    <td style="padding: 4px; text-align: right;">{{{{ item.qty }}}}</td>
                    <td style="padding: 4px; text-align: right;">{{{{ item.get_formatted("rate") }}}}</td>
                    <td style="padding: 4px; text-align: right;">{{{{ item.get_formatted("amount") }}}}</td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>

        <!-- Totals & Footer -->
        <table style="width: 100%; page-break-inside: avoid; font-size: 10px;">
            <tr>
                <td style="width: 60%; vertical-align: top; padding-right: 20px;">
                    <strong>Amount in Words:</strong><br>
                    <span style="color: #666; font-style: italic;">{{{{ doc.in_words }}}}</span>
                </td>
                <td style="width: 40%; vertical-align: top;">
                    <table style="width: 100%; border-collapse: collapse;">
                        {{% for tax in doc.taxes %}}
                        <tr>
                            <td style="padding: 3px; text-align: right; color: #666;">{{{{ tax.description }}}}</td>
                            <td style="padding: 3px; text-align: right; border-bottom: 1px solid #eee;">{{{{ tax.get_formatted("tax_amount") }}}}</td>
                        </tr>
                        {{% endfor %}}
                        <tr style="background-color: {branding_color}; color: white;">
                            <td style="padding: 6px; text-align: right; font-weight: bold;">Grand Total</td>
                            <td style="padding: 6px; text-align: right; font-weight: bold;">{{{{ doc.get_formatted("grand_total") }}}}</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        
        <div style="margin-top: 30px; text-align: center;">
             <strong>Authorized Signatory</strong><br>
             <span style="font-size: 9px; color: #999;">Techxle Consultancy Private Limited</span>
        </div>

    </div>
    """

    # 3. Create/Update Formats for each Type
    doctypes = ["Sales Invoice", "Sales Order", "Purchase Order"]
    
    for dt in doctypes:
        format_name = f"Techxle {dt.replace(' ', '')}"
        
        if not frappe.db.exists("Print Format", format_name):
            frappe.get_doc({
                "doctype": "Print Format",
                "name": format_name,
                "standard": "No",
                "custom_format": 1,
                "print_format_type": "Jinja",
                "doc_type": dt,
                "html": html_template
            }).insert(ignore_permissions=True)
            print(f"Created Format: {format_name}")
        else:
            doc = frappe.get_doc("Print Format", format_name)
            doc.html = html_template
            doc.save(ignore_permissions=True)
            print(f"Updated Format: {format_name}")

if __name__ == "__main__":
    setup()
