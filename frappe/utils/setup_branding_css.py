import frappe

def setup():
    print("Applying CSS Overrides for Branding...")
    try:
        inject_custom_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("CSS Overrides Applied!")
    except Exception as e:
        frappe.db.rollback()
        print(f"CSS Override Failed: {e}")
        import traceback
        traceback.print_exc()

def inject_custom_css():
    # We will inject CSS into the 'Website Theme' or 'Navbar Settings' if possible.
    # But for the DESK (internal), best place is 'Navbar Settings' -> 'style' doesn't exist.
    # Use 'Client Script' for Style is one way, but let's use the 'build_event' logic or simply
    # update the 'Brand HTML' to contain a <style> block which is validated but often allowed in settings.
    
    brand_text = "Techxle Consulting"
    logo_url = "/files/techxle_logo.jpg"
    
    # 1. REDEFINE Brand HTML with embedded Style to force layout
    # We use ::after pseudo-element to replace text if it's "ERPNext"
    
    css_hack = f"""
    <style>
    /* Hide the text if it says ERPNext (hard to target text content with CSS, but we can hide the span and show our own) */
    .navbar-brand .hidden-xs, .navbar-brand .hidden-sm {{
        display: none !important;
    }}
    
    /* Re-inject our text using pseudo element on the link anchor */
    .navbar-brand::after {{
        content: "{brand_text}";
        display: block;
        font-size: 10px;
        font-weight: bold;
        color: #fff; /* Assuming dark navbar */
        line-height: normal;
        margin-top: 2px;
    }}
    
    /* Ensure Logo is nice */
    .navbar-brand img {{
        max-height: 24px !important;
        width: auto !important;
        display: block !important;
        margin: 0 auto !important;
    }}
    
    /* Stack Layout */
    .navbar-brand {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 5px 15px !important;
        height: auto !important;
    }}
    </style>
    
    <!-- The Actual Content -->
    <div style="text-align: center;">
        <img src="{logo_url}" style="height: 24px;">
    </div>
    """
    
    # Apply to Website Settings (Global)
    ws = frappe.get_single("Website Settings")
    ws.brand_html = css_hack
    ws.save(ignore_permissions=True)
    
    print("Injected CSS Hack into Website Settings Brand HTML.")

if __name__ == "__main__":
    setup()
