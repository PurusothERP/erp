import frappe

def setup():
    print("Applying High-Fidelity Print Format...")
    try:
        update_print_format()
        frappe.db.commit()
        print("Print Format Updated Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Print Format Update Failed: {e}")
        import traceback
        traceback.print_exc()

def update_print_format():
    pf_name = "Techxle Bilingual"
    if not frappe.db.exists("Print Format", pf_name):
        print(f"Print Format {pf_name} missing. Run previous setup first.")
        return

    logo_path = "/files/techxle_logo.jpg"
    branding_color = "#003366"

    # HTML Template
    # Using Table layout for reliability in wkhtmltopdf
    html = f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; font-size: 13px;">
        
        <!-- Header Section -->
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
            <tr>
                <!-- Logo Left -->
                <td style="width: 50%; vertical-align: top;">
                    <img src="{logo_path}" style="max-height: 80px; max-width: 200px;">
                </td>
                <!-- Company Info Right -->
                <td style="width: 50%; text-align: right; vertical-align: top;">
                    <h2 style="color: {branding_color}; margin: 0; font-size: 24px;">{{{{ doc.company }}}}</h2>
                    <p style="margin: 5px 0; font-size: 12px; color: #666;">
                        {{{{ frappe.db.get_value("Company", doc.company, "users_address_html") or "" }}}}
                    </p>
                </td>
            </tr>
        </table>

        <!-- Document Title & Details Bar -->
        <div style="background-color: {branding_color}; color: white; padding: 10px; margin-bottom: 20px; border-radius: 4px;">
            <table style="width: 100%;">
                <tr>
                    <td style="font-size: 18px; font-weight: bold;">
                        {{{{ doc.doctype }}}} <span style="font-weight: normal; font-size: 14px; opacity: 0.8;">| {{{{ doc.doctype == 'Sales Invoice' and 'فاتورة المبيعات' or 'عرض سعر' }}}}</span>
                    </td>
                    <td style="text-align: right; font-size: 14px;">
                        <strong># {{{{ doc.name }}}}</strong>
                    </td>
                </tr>
            </table>
        </div>

        <!-- Info Grid -->
        <table style="width: 100%; margin-bottom: 20px;">
            <tr>
                <td style="width: 50%; vertical-align: top; padding-right: 20px;">
                    <strong style="color: {branding_color}; display: block; margin-bottom: 5px; border-bottom: 1px solid #ddd; padding-bottom: 5px;">To / العميل</strong>
                    <h4 style="margin: 5px 0;">{{{{ doc.customer_name }}}}</h4>
                    {{{{ doc.address_display or "" }}}}
                </td>
                <td style="width: 50%; vertical-align: top; padding-left: 20px;">
                    <table style="width: 100%; font-size: 12px;">
                        <tr>
                            <td style="padding: 4px; border-bottom: 1px solid #eee;"><strong>Date / التاريخ</strong></td>
                            <td style="padding: 4px; border-bottom: 1px solid #eee; text-align: right;">{{{{ doc.get_formatted("transaction_date") or doc.get_formatted("date") }}}}</td>
                        </tr>
                        <tr>
                            <td style="padding: 4px; border-bottom: 1px solid #eee;"><strong>Reference / مرجع</strong></td>
                            <td style="padding: 4px; border-bottom: 1px solid #eee; text-align: right;">{{{{ doc.po_no or "-" }}}}</td>
                        </tr>
                        <tr>
                            <td style="padding: 4px; border-bottom: 1px solid #eee;"><strong>Status / الحالة</strong></td>
                            <td style="padding: 4px; border-bottom: 1px solid #eee; text-align: right;">{{{{ doc.status }}}}</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Items Table -->
        <table class="table table-bordered" style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
            <thead>
                <tr style="background-color: {branding_color}; color: white;">
                    <th style="padding: 8px; border: 1px solid {branding_color}; width: 5%;">Sr<br><span style="font-size: 10px; opacity: 0.8;">م</span></th>
                    <th style="padding: 8px; border: 1px solid {branding_color}; width: 45%;">Item & Description<br><span style="font-size: 10px; opacity: 0.8;">الصنف / الوصف</span></th>
                    <th style="padding: 8px; border: 1px solid {branding_color}; width: 10%; text-align: right;">Qty<br><span style="font-size: 10px; opacity: 0.8;">الكمية</span></th>
                    <th style="padding: 8px; border: 1px solid {branding_color}; width: 15%; text-align: right;">Rate<br><span style="font-size: 10px; opacity: 0.8;">السعر</span></th>
                    <th style="padding: 8px; border: 1px solid {branding_color}; width: 15%; text-align: right;">Amount<br><span style="font-size: 10px; opacity: 0.8;">المبلغ</span></th>
                </tr>
            </thead>
            <tbody>
                {{% for item in doc.items %}}
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px; text-align: center; vertical-align: top;">{{{{ loop.index }}}}</td>
                    <td style="padding: 10px; vertical-align: top;">
                        <span style="font-weight: bold; color: {branding_color};">{{{{ item.item_code }}}}</span>
                        <div style="margin-top: 4px; color: #555;">{{{{ item.description }}}}</div>
                    </td>
                    <td style="padding: 10px; text-align: right; vertical-align: top;">{{{{ item.qty }}}}</td>
                    <td style="padding: 10px; text-align: right; vertical-align: top;">{{{{ item.get_formatted("rate") }}}}</td>
                    <td style="padding: 10px; text-align: right; vertical-align: top;">{{{{ item.get_formatted("amount") }}}}</td>
                </tr>
                {{% endfor %}}
            </tbody>
        </table>

        <!-- Totals & Footer -->
        <table style="width: 100%; page-break-inside: avoid;">
            <tr>
                <td style="width: 60%; vertical-align: top;">
                    <p style="font-size: 12px;"><strong>In Words:</strong><br>{{{{ doc.in_words }}}}</p>
                    <!-- T&C Placeholder -->
                    <div style="margin-top: 20px; font-size: 11px; color: #777;">
                        <p><strong>Terms & Conditions:</strong></p>
                        <ol style="padding-left: 15px;">
                            <li>Payment is due within 30 days.</li>
                            <li>Goods once sold cannot be returned.</li>
                        </ol>
                    </div>
                </td>
                <td style="width: 40%; vertical-align: top;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Subtotal</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{{{{ doc.get_formatted("total") }}}}</td>
                        </tr>
                        {{% for tax in doc.taxes %}}
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-size: 12px;">{{{{ tax.description }}}}</td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right; font-size: 12px;">{{{{ tax.get_formatted("tax_amount") }}}}</td>
                        </tr>
                        {{% endfor %}}
                        <tr style="background-color: #f0f4f8;">
                            <td style="padding: 12px; color: {branding_color}; font-size: 16px;"><strong>Grand Total</strong></td>
                            <td style="padding: 12px; color: {branding_color}; font-size: 16px; font-weight: bold; text-align: right;">{{{{ doc.get_formatted("grand_total") }}}}</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        
        <br><br><br>
        
        <!-- Signatures -->
        <table style="width: 100%; margin-top: 40px;">
            <tr>
                <td style="width: 50%;"></td>
                <td style="width: 50%; text-align: center;">
                    <div style="border-bottom: 1px solid #000; width: 80%; margin: 0 auto 10px auto;"></div>
                    <strong>Authorized Signatory</strong><br>
                    <span style="font-size: 12px;">For {{{{ doc.company }}}}</span>
                </td>
            </tr>
        </table>
        
        <!-- Footer Strip -->
        <div style="margin-top: 30px; border-top: 4px solid {branding_color}; padding-top: 10px; text-align: center; color: #999; font-size: 10px;">
            Techxle Consulting Services | CRM
        </div>

    </div>
    """

    doc = frappe.get_doc("Print Format", pf_name)
    doc.html = html
    doc.save()

if __name__ == "__main__":
    setup()
