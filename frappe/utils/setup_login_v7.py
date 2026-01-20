import frappe

def setup():
    print("Injecting Custom Login Styles V7 (Absolute Center-Right)...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles V7 Injected Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Login Styling Failed: {e}")
        import traceback
        traceback.print_exc()

def inject_login_css():
    # Images
    hero_image = "/files/techxle_login_hero_final.jpg" 
    logo_image = "/files/techxle_login_logo_final.png" 
    branding_color = "#003366" 
    
    custom_css = f"""
    <style>
    /* Techxle Login Customization V7 */
    
    /* 1. Background */
    html::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('{hero_image}') no-repeat center center fixed !important;
        background-size: cover !important;
        z-index: -9999;
    }}
    html::after {{ display: none !important; }}
    html, body {{ background: transparent !important; overflow: hidden; }}
    
    /* 2. Positioning the Card (ABSOLUTE) */
    /* We ignore the flow and place it exactly where we want */
    .page-card {{
        position: fixed !important;
        right: 15% !important; /* Center-Right sweet spot */
        top: 50% !important;
        transform: translateY(-50%) !important;
        left: auto !important;
        margin: 0 !important;
        
        background: rgba(255, 255, 255, 1) !important;
        border-radius: 16px !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.25) !important;
        padding: 45px 40px !important;
        width: 400px !important;
        max-width: 90vw !important;
        z-index: 100 !important;
        
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
    }}
    
    /* Mobile Responsive: Back to Center */
    @media (max-width: 800px) {{
        .page-card {{
            position: relative !important;
            right: auto !important;
            top: auto !important;
            transform: none !important;
            margin: 10vh auto !important;
            width: 90% !important;
            left: 0 !important;
        }}
        .login-content-page {{
             display: flex;
             justify-content: center;
             align-items: center;
        }}
    }}
    
    /* 3. Hide Default Header */
    .page-card-head, .login-header {{ display: none !important; }}
    
    /* 4. Custom Logo & Title styles */
    .custom-auth-logo {{
        max-width: 220px;
        height: auto;
        margin-bottom: 5px;
        display: block;
    }}
    
    .custom-login-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        font-size: 26px;
        font-weight: 700;
        color: {branding_color};
        margin-bottom: 20px;
        text-align: center;
    }}
    
    /* 5. Form Styles */
    .form-group {{ width: 100%; margin-bottom: 15px !important; }}
    .form-control {{
        background: #f8f9fa !important;
        border: 1px solid #dfe3e8 !important;
        padding: 12px 15px !important;
        height: auto !important;
        font-size: 14px;
        border-radius: 8px;
        transition: all 0.2s;
    }}
    .form-control:focus {{
        border-color: {branding_color} !important;
        box-shadow: 0 0 0 3px rgba(0, 51, 102, 0.1) !important;
        background: #fff !important;
    }}
    .btn-login {{
        width: 100%;
        padding: 12px !important;
        font-size: 16px;
        font-weight: 600;
        margin-top: 15px;
        background-color: {branding_color} !important;
        border: none;
        border-radius: 8px;
    }}
    </style>
    
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        const pageCard = document.querySelector(".page-card");
        if(pageCard && !document.querySelector(".custom-login-title")) {{
            // Title
            const title = document.createElement("div");
            title.className = "custom-login-title";
            title.innerText = "Login";
            // Logo
            const logo = document.createElement("img");
            logo.src = "{logo_image}";
            logo.className = "custom-auth-logo";
            // Insert
            pageCard.insertBefore(title, pageCard.firstChild);
            pageCard.insertBefore(logo, pageCard.firstChild);
        }}
    }});
    </script>
    """
    
    settings = frappe.get_single("Website Settings")
    import re
    if settings.head_html:
        pattern = re.compile(r'<style>\s*/\* Techxle Login Customization.*?</script>', re.DOTALL)
        settings.head_html = re.sub(pattern, "", settings.head_html) 
    
    settings.head_html = (settings.head_html or "") + "\n" + custom_css
    settings.save(ignore_permissions=True)
    print("Injected V7 CSS (Absolute Position)")

if __name__ == "__main__":
    setup()
