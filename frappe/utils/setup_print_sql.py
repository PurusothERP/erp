import frappe

def run():
    # MATCHING USER SCREENSHOT EXACTLY (Dark Banner Design)
    
    html_raw = """
    <div class="print-format-gutter" style="font-family: 'Inter', sans-serif; color: #1f2937; padding: 20px;">
        
        <!-- 1. Top Section: Logo & Company Name -->
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 20px;">
            <div style="width: 50%;">
                <img src="/files/techxle_login_logo_final.png" style="max-height: 70px; width: auto;" alt="Techxle">
            </div>
            <div style="width: 50%; text-align: right;">
                <h2 style="font-size: 18px; font-weight: 700; color: #1e3a8a; margin: 0;">Techxl consulting services</h2>
                <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">
                    {{ doc.company_address_display or '' }}
                </div>
            </div>
        </div>

        <!-- 2. Dark Blue Banner (Signature Look) -->
        <div style="background-color: #0c2b5e; color: white; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-radius: 2px;">
            <div>
                <h1 style="font-size: 20px; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 1px;">
                    {{ doc.doctype }}
                </h1>
            </div>
            <div style="text-align: right; font-size: 13px;">
                <span style="opacity: 0.9;">Date: </span>
                <span style="font-weight: 600;">{{ doc.get_formatted("transaction_date") or doc.get_formatted("date") }}</span>
                <span style="opacity: 0.6; margin: 0 8px;">|</span>
                <span style="opacity: 0.9;"># </span>
                <span style="font-weight: 600;">{{ doc.name }}</span>
            </div>
        </div>

        <!-- 3. Customer & Reference Details -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 40px;">
            
            <!-- Left: Customer -->
            <div style="width: 45%;">
                <div style="font-size: 11px; font-weight: 700; color: #1e3a8a; text-transform: uppercase; margin-bottom: 5px;">
                    TO / CUSTOMER
                </div>
                <div style="font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 5px;">
                    {{ doc.customer_name or doc.supplier_name or doc.party_name or doc.payee_name }}
                </div>
                <div style="font-size: 13px; color: #4b5563; line-height: 1.5;">
                    {{ doc.address_display or '' }}
                </div>
            </div>

            <!-- Right: Metadata -->
            <div style="width: 45%;">
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                    <tr style="border-bottom: 1px solid #f3f4f6;">
                        <td style="padding: 6px 0; color: #6b7280;">Reference</td>
                        <td style="padding: 6px 0; text-align: right; font-weight: 600; color: #111827;">
                             {{ doc.po_no or doc.supplier_quotation or "-" }}
                        </td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f3f4f6;">
                        <td style="padding: 6px 0; color: #6b7280;">Payment Terms</td>
                        <td style="padding: 6px 0; text-align: right; font-weight: 600; color: #111827;">
                            {{ doc.payment_terms_template or "Standard" }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 6px 0; color: #6b7280;">Valid Until / Due</td>
                        <td style="padding: 6px 0; text-align: right; font-weight: 600; color: #111827;">
                             {{ doc.get_formatted("valid_till") or doc.get_formatted("due_date") or "-" }}
                        </td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- 4. Items Table -->
        {% if doc.items %}
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 13px;">
            <thead>
                <tr style="background-color: #f8fafc; border-top: 1px solid #e5e7eb; border-bottom: 1px solid #e5e7eb; color: #4b5563;">
                    <th style="padding: 10px; text-align: left; font-weight: 600;">Sr</th>
                    <th style="padding: 10px; text-align: left; font-weight: 600; width: 50%;">Description</th>
                    <th style="padding: 10px; text-align: right; font-weight: 600;">Qty</th>
                    <th style="padding: 10px; text-align: right; font-weight: 600;">Rate</th>
                    <th style="padding: 10px; text-align: right; font-weight: 600;">Amount</th>
                </tr>
            </thead>
            <tbody>
                {% for item in doc.items %}
                <tr style="border-bottom: 1px solid #f3f4f6;">
                    <td style="padding: 10px; color: #6b7280;">{{ loop.index }}</td>
                    <td style="padding: 10px; color: #111827; font-weight: 500;">
                        {{ item.item_name }}
                        {% if item.description != item.item_name %}
                            <br><span style="font-size: 11px; color: #9ca3af;">{{ item.description }}</span>
                        {% endif %}
                    </td>
                    <td style="padding: 10px; text-align: right; color: #374151;">{{ item.get_formatted("qty") }}</td>
                    <td style="padding: 10px; text-align: right; color: #374151;">{{ item.get_formatted("rate") }}</td>
                    <td style="padding: 10px; text-align: right; font-weight: 600; color: #111827;">{{ item.get_formatted("amount") }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        <!-- 5. Totals & Terms -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 40px;">
            <div style="width: 50%;">
                <div style="font-size: 11px; font-weight: 700; color: #111827; margin-bottom: 5px;">Amount in Words:</div>
                <div style="font-size: 13px; color: #4b5563; font-style: italic;">{{ doc.in_words }}</div>
                
                {% if doc.terms %}
                <div style="margin-top: 20px;">
                    <div style="font-size: 11px; font-weight: 700; color: #111827; margin-bottom: 5px;">Terms & Conditions:</div>
                    <div style="font-size: 11px; color: #6b7280; white-space: pre-wrap;">{{ doc.terms }}</div>
                </div>
                {% endif %}
            </div>

            <div style="width: 40%;">
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                    {% if doc.taxes %}
                        {% for tax in doc.taxes %}
                        {% if not tax.included_in_print_rate %}
                        <tr>
                            <td style="padding: 6px 0; text-align: right; color: #6b7280;">{{ tax.description }}</td>
                            <td style="padding: 6px 0; text-align: right; font-weight: 600; color: #374151; width: 120px;">{{ tax.get_formatted("tax_amount") }}</td>
                        </tr>
                        {% endif %}
                        {% endfor %}
                    {% endif %}
                    
                    <!-- Blue Total Bar -->
                    <tr style="background-color: #0c2b5e; color: white;">
                        <td style="padding: 10px 15px; text-align: right; font-weight: 600;">Grand Total</td>
                        <td style="padding: 10px 15px; text-align: right; font-weight: 700;">{{ doc.get_formatted("grand_total") }}</td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- 6. Footer -->
        <div style="text-align: right; margin-top: 60px;">
            <p style="font-size: 12px; font-weight: 700; color: #111827; margin-bottom: 0;">Authorized Signatory</p>
            <p style="font-size: 11px; color: #6b7280; margin-top: 5px;">Techxl consulting services</p>
        </div>

    </div>
    """

    targets = [
        "Quotation", "Sales Order", "Delivery Note", "Sales Invoice", 
        "Purchase Order", "Purchase Receipt", "Purchase Invoice", "Payment Entry", "Material Request"
    ]
    
    for doctype in targets:
        fmt_name = f"Techxle {doctype} Format"

        # 1. DELETE ANY OLD "Techxle" FORMATS (Fixing %% syntax)
        # We delete anything starting with 'Techxle' that is NOT our target name.
        frappe.db.sql("DELETE FROM `tabPrint Format` WHERE doc_type=%s AND name LIKE 'Techxle%%' AND name != %s", (doctype, fmt_name))

        # 2. Ensure Correct Format Exists
        if not frappe.db.exists("Print Format", fmt_name):
             frappe.get_doc({
                "doctype": "Print Format",
                "name": fmt_name,
                "doc_type": doctype,
                "standard": "No",
                "custom_format": 1,
                "print_format_type": "Jinja",
                "html": "TEMP"
            }).insert()

        # 3. Apply HTML
        frappe.db.sql("""
            UPDATE `tabPrint Format` 
            SET html=%s, custom_format=1, print_format_type='Jinja', disabled=0
            WHERE name=%s
        """, (html_raw, fmt_name))
        
        print(f"Applied: {fmt_name}")

    frappe.db.commit()
    frappe.clear_cache()
    print("SUCCESS: Dark Banner Design Applied. Duplicates Removed.")

if __name__ == "__main__":
    run()
