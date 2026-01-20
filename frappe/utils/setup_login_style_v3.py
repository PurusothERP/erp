import frappe

def setup():
    print("Injecting Custom Login Styles (V3 - Final Logo)...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles V3 Injected Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Login Styling Failed: {e}")
        import traceback
        traceback.print_exc()

def inject_login_css():
    # Images
    hero_image = "/files/techxle_login_hero.jpg"
    logo_image = "/files/techxle_login_logo_final.png" # Using New Final Logo
    branding_color = "#003366" 
    
    # Update Website Settings to point to the new logo
    ws = frappe.get_single("Website Settings")
    ws.app_logo = logo_image
    ws.save(ignore_permissions=True)
    
    # Custom CSS/JS
    # Note: We REMOVE the JS text injection because the new logo has the text.
    
    custom_css = f"""
    <style>
    /* Techxle Login Customization V3 */
    
    body.frappe-login-page {{
        background-color: {branding_color} !important;
        background-image: url('{hero_image}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
    }}
    
    /* Overlay */
    body.frappe-login-page::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 51, 102, 0.5); 
        z-index: -1;
    }}
    
    .page-card, .login-content {{
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 16px !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}
    
    /* Logo sizing - Increased for the full logo+text image */
    .page-card-head img, .login-content .app-logo, .tech-brand-container img {{
        max-height: 80px !important; 
        max-width: 250px !important;
        width: auto !important;
        margin-bottom: 20px !important;
    }}
    
    /* Hide previous V2 text if it lingers or standard titles */
    .tech-brand-text, .page-card-head h4, .login-header h4 {{
        display: none !important;
    }}
    
    .btn-primary {{
        background-color: {branding_color} !important;
        border-color: {branding_color} !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .form-control:focus {{
        border-color: {branding_color} !important;
        box-shadow: 0 0 0 3px rgba(0, 51, 102, 0.15) !important;
    }}
    </style>
    
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        // Reset DOM if V2 Script ran previously on this page load context (unlikely on reload but good hygiene)
        // Ensure Logo is correct src
        if(document.querySelector(".frappe-login-page")) {{
            const logo = document.querySelector(".page-card-head img") || document.querySelector(".app-logo");
            if(logo) {{
                logo.src = "{logo_image}";
                // If wrapped in our V2 container, we can leave it or unwrap, 
                // but CSS above hides the text anyway.
            }}
        }}
    }});
    </script>
    """
    
    settings = frappe.get_single("Website Settings")
    
    # Replace old block if exists
    import re
    if settings.head_html and "Techxle Login Customization" in settings.head_html:
         # Regex replacement to wipe previous versions
        pattern = re.compile(r'<style>\s*/\* Techxle Login Customization.*?</script>', re.DOTALL)
        settings.head_html = re.sub(pattern, custom_css.strip(), settings.head_html)
    else:
        settings.head_html = (settings.head_html or "") + "\n" + custom_css

    settings.save(ignore_permissions=True)
    print("Injected V3 CSS/JS into Website Settings Head HTML")

if __name__ == "__main__":
    setup()
