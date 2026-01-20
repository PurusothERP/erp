import frappe

def setup():
    print("Injecting Custom Login Styles (V2)...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles Injected Successfully!")
    except Exception as e:
        frappe.db.rollback()
        print(f"Login Styling Failed: {e}")
        import traceback
        traceback.print_exc()

def inject_login_css():
    # Images
    hero_image = "/files/techxle_login_hero.jpg"
    logo_image = "/files/techxle_login_logo_custom.png" # Using New Logo (PNG)
    branding_color = "#003366" 
    
    # Update Website Settings to point to the new logo first
    ws = frappe.get_single("Website Settings")
    ws.app_logo = logo_image
    ws.save(ignore_permissions=True)
    
    # Custom CSS/JS with proper escaping for Python f-strings
    # Double curly braces {{ }} are needed for literal braces in f-strings.
    
    custom_css = f"""
    <style>
    /* Techxle Login Customization V2 */
    
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
    
    /* Logo sizing */
    .page-card-head img, .login-content .app-logo, .tech-brand-container img {{
        max-height: 50px !important; 
        width: auto !important;
    }}
    
    /* Hide default logo to use our custom container if needed, 
       but standard behavior replaces existing logo. 
       We will suppress the default logo if our script runs, 
       OR we just style the default one. 
       Use JS to ensure structure. */
       
    .tech-brand-text {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
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
        if(document.querySelector(".frappe-login-page")) {{
            // Find the logo
            const logo = document.querySelector(".page-card-head img") || document.querySelector(".app-logo");
            
            // If logo exists and we haven't modified it yet
            if(logo && !logo.parentNode.classList.contains("tech-brand-container")) {{
                
                // create container
                const container = document.createElement("div");
                container.className = "tech-brand-container";
                container.style.display = "flex";
                container.style.alignItems = "center";
                container.style.justifyContent = "center";
                container.style.marginBottom = "20px";
                
                // Ensure logo src is correct (client side override just in case)
                logo.src = "{logo_image}";
                logo.style.marginRight = "15px";
                logo.style.marginBottom = "0px"; // Reset
                
                // Create text
                const span = document.createElement("span");
                span.innerText = "Techxl";
                span.className = "tech-brand-text";
                span.style.fontSize = "28px";
                span.style.fontWeight = "bold";
                span.style.color = "{branding_color}";
                span.style.lineHeight = "1";
                span.style.letterSpacing = "-0.5px";
                
                // Insert container before logo
                logo.parentNode.insertBefore(container, logo);
                
                // Move logo into container
                container.appendChild(logo);
                container.appendChild(span);
                
                // Hide any other H4 branding text that might be there
                const existingTitle = document.querySelector(".page-card-head h4");
                if(existingTitle) existingTitle.style.display = "none";
            }}
        }}
    }});
    </script>
    """
    
    settings = frappe.get_single("Website Settings")
    
    # Replace old block if exists
    import re
    if settings.head_html and "Techxle Login Customization" in settings.head_html:
        # Regex to match basic style block - naive but workable
        pattern = re.compile(r'<style>\s*/\* Techxle Login Customization.*?</script>', re.DOTALL)
        settings.head_html = re.sub(pattern, custom_css.strip(), settings.head_html)
    else:
        settings.head_html = (settings.head_html or "") + "\n" + custom_css

    settings.save(ignore_permissions=True)
    print("Injected CSS/JS into Website Settings Head HTML")

if __name__ == "__main__":
    setup()
