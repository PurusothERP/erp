import frappe

def setup():
    print("Injecting Custom Login Styles V6 (Center-Right Layout)...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles V6 Injected Successfully!")
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
    /* Techxle Login Customization V6 */
    
    /* 1. Background - NO OVERLAY */
    html::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('{hero_image}') no-repeat center center fixed !important;
        background-size: cover !important;
        z-index: -9999;
    }}
    
    html::after {{
        display: none !important;
    }}
    
    html, body{{
         background: transparent !important;
         height: 100vh;
         width: 100%;
         overflow: hidden; /* Prevent scroll */
    }}
    
    /* 2. Main Flex Container - Right Aligned */
    .login-content-page {{
        min-height: 100vh;
        display: flex;
        align-items: center; /* Vertical Center */
        justify-content: flex-end !important; /* Push everything to right */
        padding-right: 15vw !important; /* Distance from right edge */
    }}
    
    /* Mobile Responsive adjustment */
    @media (max-width: 768px) {{
        .login-content-page {{
            justify-content: center !important;
            padding-right: 0 !important;
        }}
    }}
    
    /* 3. Login Card */
    .page-card, .login-content {{
        background: rgba(255, 255, 255, 1) !important;
        border-radius: 12px !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2) !important;
        padding: 40px !important;
        width: 100% !important;
        max-width: 420px !important;
        
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px; /* Nice spacing between Logo, Title, Inputs */
    }}
    
    /* 4. Hide Default Logo Area */
    .page-card-head, .login-header {{
        display: none !important;
    }}
    
    /* 5. Custom Elements via JS */
    .custom-auth-logo {{
        max-width: 220px;
        height: auto;
        margin-bottom: 5px;
    }}
    
    .custom-login-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial;
        font-size: 26px;
        font-weight: 700;
        color: {branding_color};
        margin-bottom: 25px;
        text-align: center;
    }}
    
    /* Form Inputs */
    .form-group {{
        width: 100%;
        margin-bottom: 15px !important;
    }}
    
    .form-control {{
        background: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        padding: 12px !important;
        height: auto !important;
        font-size: 14px;
        border-radius: 6px;
    }}
    
    .btn-login {{
        width: 100%;
        padding: 12px !important;
        font-size: 16px;
        font-weight: 600;
        margin-top: 10px;
        background-color: {branding_color} !important;
        border: none;
    }}
    
    /* Make sure password show icon is positioned right */
    .toggle-password {{
        top: 12px !important;
    }}
    
    </style>
    
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        // Logic to inject Logo/Title inside card if not present
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
            
            // Insert at top
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
    print("Injected V6 CSS (Center-Right Layout)")

if __name__ == "__main__":
    setup()
