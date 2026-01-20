import frappe

def setup():
    print("Injecting FINAL Login Styles (Aggressive Background)...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles Final Injected Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Login Styling Failed: {e}")
        import traceback
        traceback.print_exc()

def inject_login_css():
    # Images
    hero_image = "/files/techxle_login_hero_final.jpg" # FINAL Background
    logo_image = "/files/techxle_login_logo_final.png" # V3 Logo
    branding_color = "#003366" 
    
    # 1. Unset splash_image in Website Settings to avoid conflict
    # Sometimes setting this overrides custom CSS or creates split layout
    ws = frappe.get_single("Website Settings")
    ws.splash_image = "" # Clear it to let CSS take over full screen
    ws.app_logo = logo_image
    ws.save(ignore_permissions=True)
    
    # 2. Aggressive CSS
    custom_css = f"""
    <style>
    /* Techxle Login Customization FINAL */
    
    /* Target body and html to ensure full coverage */
    html, body, .frappe-login-page {{
        height: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    body.frappe-login-page {{
        background: url('{hero_image}') no-repeat center center fixed !important;
        background-size: cover !important;
        -webkit-background-size: cover !important;
        -moz-background-size: cover !important;
        -o-background-size: cover !important;
    }}
    
    /* Strong Blue Overlay */
    body.frappe-login-page::before {{
        content: "";
        position: fixed; /* Fixed to cover updated scroll */
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 51, 102, 0.6) !important; /* Slightly darker */
        z-index: 0;
        pointer-events: none;
    }}
    
    /* content styling */
    .login-content-page {{
        position: relative;
        z-index: 1;
        background: transparent !important;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }}
    
    .page-card {{
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.4) !important;
        padding: 40px !important;
        width: 100% !important;
        max-width: 420px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}
    
    /* Ensure no other backgrounds interfere */
    .main-section {{
        background: transparent !important;
    }}
    
    /* Logo sizing */
    .page-card-head img, .login-content .app-logo {{
        max-height: 80px !important; 
        max-width: 250px !important;
        width: auto !important;
        margin-bottom: 25px !important;
    }}
    
    /* Hide unwanted text */
    .page-card-head h4, .login-header h4 {{
        display: none !important;
    }}
    
    .btn-primary {{
        background-color: {branding_color} !important;
        border-color: {branding_color} !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    </style>
    
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        // Force Logo update just in case
        if(document.querySelector(".frappe-login-page")) {{
            const logo = document.querySelector(".page-card-head img") || document.querySelector(".app-logo");
            if(logo) {{
                logo.src = "{logo_image}";
            }}
        }}
    }});
    </script>
    """
    
    settings = frappe.get_single("Website Settings")
    
    # Clean replacement
    import re
    if settings.head_html:
        pattern = re.compile(r'<style>\s*/\* Techxle Login Customization.*?</script>', re.DOTALL)
        settings.head_html = re.sub(pattern, "", settings.head_html) 
    
    settings.head_html = (settings.head_html or "") + "\n" + custom_css
    settings.save(ignore_permissions=True)
    print("Injected Final CSS into Website Settings Head HTML")

if __name__ == "__main__":
    setup()
