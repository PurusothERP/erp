import frappe

def setup():
    print("Injecting NUCLEAR Login Styles (Force Background)...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles Nuclear Injected Successfully!")
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
    
    # Ensuring standard settings are clean
    ws = frappe.get_single("Website Settings")
    ws.splash_image = "" 
    ws.app_logo = logo_image
    ws.save(ignore_permissions=True)
    
    # NUCLEAR OPTION CSS
    # We use a FIXED position div created via pseudo-element on HTML
    # This sits behind everything.
    # Then we force body and main containers to be transparent.
    
    custom_css = f"""
    <style>
    /* Techxle Login Customization NUCLEAR */
    
    /* 1. Root layer background */
    html::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('{hero_image}') no-repeat center center fixed !important;
        background-size: cover !important;
        z-index: -9999;
    }}
    
    /* 2. Overlay layer */
    html::after {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 51, 102, 0.6) !important;
        z-index: -9998;
    }}
    
    /* 3. Make structural layers transparent so background shows */
    html, body, .frappe-login-page, .main-section, .content {{
        background: transparent !important;
        background-color: transparent !important;
    }}
    
    /* 4. Restore card background */
    .page-card {{
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important;
        padding: 40px !important;
        max-width: 400px !important;
        margin: 0 auto;
        border: 1px solid rgba(255,255,255,0.3) !important;
        position: relative; 
        z-index: 10; /* Above background */
    }}
    
    /* Center the card vertically if needed */
    .login-content-page {{
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }}
    
    /* Logo styling */
    .page-card-head img, .login-content .app-logo {{
        max-height: 80px !important; 
        max-width: 250px !important;
        width: auto !important;
        margin-bottom: 20px !important;
    }}
    
    /* Hide unwanted text */
    .page-card-head h4, .login-header h4 {{
        display: none !important;
    }}
    
    /* Inputs & Buttons */
    .form-control {{
        background: #f4f7fa !important;
        border: 1px solid #d1d8e0 !important;
    }}
    
    .btn-primary {{
        background-color: {branding_color} !important;
        border-color: {branding_color} !important;
    }}
    </style>
    
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        console.log("Techxle Branding: Nuclear Script Loaded");
        
        // Force Logo update just in case
        if(document.querySelector(".frappe-login-page")) {{
            const logo = document.querySelector(".page-card-head img") || document.querySelector(".app-logo");
            if(logo) {{
                logo.src = "{logo_image}";
            }}
            
            // Debugging: Force body background via JS if CSS fails
            document.body.style.backgroundImage = "url('{hero_image}')";
            document.body.style.backgroundSize = "cover";
        }}
    }});
    </script>
    """
    
    settings = frappe.get_single("Website Settings")
    
    # Wipe old custom CSS to prevent conflicts (keep it clean)
    if settings.head_html:
        import re
        pattern = re.compile(r'<style>\s*/\* Techxle Login Customization.*?</script>', re.DOTALL)
        settings.head_html = re.sub(pattern, "", settings.head_html) 
    
    settings.head_html = (settings.head_html or "") + "\n" + custom_css
    settings.save(ignore_permissions=True)
    print("Injected Nuclear CSS into Website Settings Head HTML")

if __name__ == "__main__":
    setup()
