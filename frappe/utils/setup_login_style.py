import frappe

def setup():
    print("Injecting Custom Login Styles...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles Injected!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Login Styling Failed: {e}")
        import traceback
        traceback.print_exc()

def inject_login_css():
    # Images (Assumed deployed)
    hero_image = "/files/techxle_login_hero.jpg"
    logo_image = "/files/techxle_login_logo.jpg"
    branding_color = "#003366" # Techxle Blue
    
    # We will append this to Website Settings -> head_html
    # This ensures it loads on the Login Page (which is a website page).
    
    custom_css = f"""
    <style>
    /* Techxle Login Customization */
    
    body.frappe-login-page {{
        background-color: {branding_color} !important;
        /* Hero Image as Full Background Overlay */
        background-image: url('{hero_image}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
    }}
    
    /* Darken background for readability if needed */
    body.frappe-login-page::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 51, 102, 0.4); /* Blue Tint */
        z-index: -1;
    }}

    /* Card Styling */
    .login-content-page {{
        background: transparent !important;
        box-shadow: none !important;
    }}
    
    .page-card, .login-content {{
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        max-width: 450px !important;
        padding: 40px !important;
        margin: 0 auto;
    }}
    
    /* Logo Area Customization */
    .page-card-head img, .login-content .app-logo {{
        max-height: 45px !important;
        width: auto !important;
        margin-bottom: 10px !important;
    }}
    
    /* Add "Techxl" visual next to logo using CSS ::after on container */
    /* This depends on exact DOM structure, but let's try targeting the parent of the image */
    .page-card-head, .login-header {{
        display: flex !important;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    
    /* Hide default "Login to..." text if redundant or style it */
    .page-card-head h4, .login-header h4 {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: {branding_color} !important;
        font-weight: 700 !important;
        margin-top: 10px !important;
    }}
    
    /* Inject "Techxl" text if we want it strictly NEXT to logo image */
    /* We'll wrap the logo in a flex container via JS or just fake it with ::after on the IMAGE container if possible. 
       Actually, standard ERPNext logo is just an img tag. 
       Let's use a nice trick: 
       We will inject some JS to validly restructure the header if CSS isn't enough. 
       But CSS is safer for pure styles. 
       Let's stick to styling the H4 (Title) to look like the brand name if the user set App Name to "Techxl".
    */

    /* Input Fields */
    .form-control {{
        background-color: #f7f9fc !important;
        border: 1px solid #e0e6ed !important;
        color: #333 !important;
        font-size: 14px !important;
        border-radius: 6px !important;
    }}
    
    .form-control:focus {{
        border-color: {branding_color} !important;
        box-shadow: 0 0 0 2px rgba(0, 51, 102, 0.1) !important;
    }}

    /* Buttons */
    .btn-primary {{
        background-color: {branding_color} !important;
        border-color: {branding_color} !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
    }}
    
    .btn-primary:hover {{
        background-color: #002244 !important; /* Darker Blue */
        transform: translateY(-1px);
    }}
    
    /* Footer/Copyright */
    .frappe-copyright {{
        display: none !important;
    }}
    
    </style>
    
    <script>
    // JS to force "Techxl" text next to logo if structure prevents CSS
    document.addEventListener("DOMContentLoaded", function() {
        if(document.querySelector(".frappe-login-page")) {{
            const logo = document.querySelector(".page-card-head img") || document.querySelector(".app-logo");
            if(logo && !logo.parentNode.querySelector(".tech-brand-text")) {{
                // Create text element
                const span = document.createElement("span");
                span.innerText = "Techxl";
                span.className = "tech-brand-text";
                span.style.fontSize = "24px";
                span.style.fontWeight = "bold";
                span.style.color = "{branding_color}";
                span.style.marginLeft = "12px";
                span.style.verticalAlign = "middle";
                span.style.display = "inline-block";
                
                // Wrap in container
                const container = document.createElement("div");
                container.style.display = "flex";
                container.style.alignItems = "center";
                container.style.justifyContent = "center";
                container.style.marginBottom = "20px";
                
                logo.parentNode.insertBefore(container, logo);
                container.appendChild(logo);
                container.appendChild(span);
            }}
        }}
    });
    </script>
    """
    
    settings = frappe.get_single("Website Settings")
    # Append to existing head_html or create new
    # We want to be careful not to duplicate endlessly if run multiple times.
    # Simple check:
    if settings.head_html and "Techxle Login Customization" in settings.head_html:
        # Replace existing block
        import re
        pattern = re.compile(r'<style>\s*/\* Techxle Login Customization \*/.*?</script>', re.DOTALL)
        settings.head_html = re.sub(pattern, custom_css.strip(), settings.head_html)
    else:
        settings.head_html = (settings.head_html or "") + "\n" + custom_css

    settings.save(ignore_permissions=True)
    print("Injected CSS/JS into Website Settings Head HTML")

if __name__ == "__main__":
    setup()
