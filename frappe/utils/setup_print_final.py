import frappe

def run():
    # WE ARE NOT USING f-strings HERE.
    # This ensures {{ }} are treated literally as text, not python placeholders.
    html_content = """
    <div class="print-format-gutter" style="font-family: 'Inter', sans-serif; color: #1f2937;">
        
        <!-- Header: Logo, Company Name, Address -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; border-bottom: 2px solid #1e3a8a; padding-bottom: 20px;">
            <div style="width: 40%;">
                <img src="/files/logo.jpg" style="max-width: 180px; height: auto;" alt="Techxle Logo">
            </div>
            <div style="width: 60%; text-align: right;">
                <h1 style="font-size: 24px; font-weight: 700; color: #1e3a8a; margin: 0; text-transform: uppercase;">Techxle Consultation Service</h1>
                <p style="font-size: 12px; color: #6b7280; margin-top: 5px; line-height: 1.4;">
                    {{ doc.company_address_display or '' }}
                </p>
            </div>
        </div>

        <!-- Document Title & Date Strip -->
        <div style="background-color: #0f172a; color: white; padding: 12px 20px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
            <h2 style="font-size: 18px; font-weight: 600; margin: 0; letter-spacing: 1px;">
                {{ doc.doctype.upper() }}
            </h2>
            <div style="text-align: right; font-size: 13px;">
                <span style="opacity: 0.8;">Date:</span> 
                <span style="font-weight: 600; margin-left: 5px;">
                    {{ doc.get_formatted("transaction_date") or doc.get_formatted("date") }}
                </span>
                <br>
                <span style="opacity: 0.8;">#</span> 
                <span style="font-weight: 600; margin-left: 5px;">{{ doc.name }}</span>
            </div>
        </div>

        <!-- Two Column Details: To/Customer vs Reference -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 40px;">
            
            <!-- Left: To / Customer -->
            <div style="width: 48%;">
                <h4 style="font-size: 11px; text-transform: uppercase; color: #1e3a8a; margin-bottom: 8px; font-weight: 700;">To / Customer</h4>
                <p style="font-size: 14px; font-weight: 600; margin: 0 0 5px 0; color: #111827;">
                    {{ doc.customer_name or doc.supplier_name or doc.party_name or doc.payee_name }}
                </p>
                <p style="font-size: 13px; color: #4b5563; line-height: 1.5; margin: 0;">
                    {{ doc.address_display or '' }}
                </p>
            </div>

            <!-- Right: Metadata Table -->
            <div style="width: 45%;">
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0; color: #6b7280;">Reference</td>
                        <td style="padding: 8px 0; text-align: right; font-weight: 600; color: #111827;">
                            {{ doc.po_no or doc.supplier_quotation or "-" }}
                        </td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0; color: #6b7280;">Payment Terms</td>
                        <td style="padding: 8px 0; text-align: right; font-weight: 600; color: #111827;">
                            {{ doc.payment_terms_template or "Standard" }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #6b7280;">Valid Until / Due</td>
                        <td style="padding: 8px 0; text-align: right; font-weight: 600; color: #111827;">
                            {{ doc.get_formatted("valid_till") or doc.get_formatted("due_date") or "-" }}
                        </td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- Check for Items Table -->
        {% if doc.items %}
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 13px;">
            <thead>
                <tr style="background-color: #f3f4f6; color: #374151;">
                    <th style="padding: 12px; text-align: left; border-radius: 4px 0 0 4px;">Sr</th>
                    <th style="padding: 12px; text-align: left;">Description</th>
                    <th style="padding: 12px; text-align: right;">Qty</th>
                    <th style="padding: 12px; text-align: right;">Rate</th>
                    <th style="padding: 12px; text-align: right; border-radius: 0 4px 4px 0;">Amount</th>
                </tr>
            </thead>
            <tbody>
                {% for item in doc.items %}
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 12px; color: #6b7280;">{{ loop.index }}</td>
                    <td style="padding: 12px; font-weight: 500; color: #111827;">
                        {{ item.item_name }}
                        {% if item.item_code != item.item_name %}
                        <br><span style="font-size: 11px; color: #9ca3af;">{{ item.item_code }}</span>
                        {% endif %}
                    </td>
                    <td style="padding: 12px; text-align: right; color: #374151;">{{ item.get_formatted("qty") }}</td>
                    <td style="padding: 12px; text-align: right; color: #374151;">{{ item.get_formatted("rate") }}</td>
                    <td style="padding: 12px; text-align: right; font-weight: 600; color: #111827;">{{ item.get_formatted("amount") }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        <!-- Totals Section -->
        <div style="display: flex; justify-content: flex-end; margin-bottom: 40px;">
            <div style="width: 50%;">
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                    
                    <!-- Taxes -->
                    {% if doc.taxes %}
                    {% for tax in doc.taxes %}
                    {% if not tax.included_in_print_rate %}
                    <tr>
                        <td style="padding: 6px 0; color: #6b7280; text-align: right;">
                            {{ tax.description }}
                            <span style="font-size: 11px;">@ {{ tax.rate }}%</span>
                        </td>
                        <td style="padding: 6px 0; text-align: right; font-weight: 500; color: #374151; width: 120px;">
                            {{ tax.get_formatted("tax_amount") }}
                        </td>
                    </tr>
                    {% endif %}
                    {% endfor %}
                    {% endif %}

                    <!-- Grand Total -->
                    <tr style="background-color: #1e3a8a; color: white;">
                        <td style="padding: 10px 15px; text-align: right; font-weight: 600; border-radius: 4px 0 0 4px;">Grand Total</td>
                        <td style="padding: 10px 15px; text-align: right; font-weight: 700; border-radius: 0 4px 4px 0;">
                            {{ doc.get_formatted("grand_total") }}
                        </td>
                    </tr>

                    <!-- In Words -->
                    <tr>
                        <td colspan="2" style="padding-top: 10px; text-align: right; font-size: 11px; color: #6b7280; font-style: italic;">
                            {{ doc.in_words }}
                        </td>
                    </tr>
                </table>
            </div>
        </div>

        <!-- Footer / Terms -->
        {% if doc.terms %}
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
            <h5 style="font-size: 12px; font-weight: 700; color: #111827; margin: 0 0 5px 0;">Terms & Conditions:</h5>
            <div style="font-size: 11px; color: #6b7280; line-height: 1.5;">
                {{ doc.terms }}
            </div>
        </div>
        {% endif %}

        <!-- Signatory -->
        <div style="margin-top: 60px; text-align: right;">
            <p style="font-size: 12px; font-weight: 700; color: #111827; margin-bottom: 40px;">Authorized Signatory</p>
            <p style="font-size: 11px; color: #9ca3af;">Techxle Consultation Service</p>
        </div>

    </div>
    """

    # Apply to comprehensive list of modules
    targets = [
        "Quotation", 
        "Sales Order", 
        "Delivery Note", 
        "Sales Invoice", 
        "Purchase Order", 
        "Purchase Receipt",
        "Purchase Invoice",
        "Payment Entry"
    ]
    
    for doctype in targets:
        fmt_name = f"Techxle {doctype} Format"
        
        # Force Create or Update
        if frappe.db.exists("Print Format", fmt_name):
            doc = frappe.get_doc("Print Format", fmt_name)
        else:
            doc = frappe.new_doc("Print Format")
            doc.name = fmt_name
            doc.doc_type = doctype
            doc.standard = "No"
            doc.custom_format = 1
            doc.print_format_type = "Jinja"
        
        doc.html = html_content 
        doc.save()
        print(f"Fixed: {fmt_name}")

    frappe.db.commit()
    print("SUCCESS: All Print Formats overwritten with Clean RAW HTML.")

if __name__ == "__main__":
    run()
