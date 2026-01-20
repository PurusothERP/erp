import frappe

def setup():
    print("Injecting custom Login Styles V5 (Logo Inside, No Overlay)...")
    try:
        inject_login_css()
        frappe.db.commit()
        frappe.clear_cache()
        print("Login Styles V5 Injected Successfully!")
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
    /* Techxle Login Customization V5 */
    
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
        display: none !important; /* Remove blue tint */
    }}
    
    html, body{{
         background: transparent !important;
    }}
    
    /* 2. Login Card */
    .page-card {{
        background: rgba(255, 255, 255, 1) !important; /* Solid white or slight opacity? User said pop up box. Assuming solid. */
        border-radius: 16px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3) !important;
        padding: 40px !important;
        max-width: 450px !important;
        margin: 0 auto;
        border: none !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    
    /* 3. Hide Default Logo Area (outside card) */
    .page-card-head {{
        display: none !important;
    }}
    
    /* 4. Custom Internal Logo Wrapper (injected via JS) */
    .custom-auth-logo {{
        max-width: 250px;
        height: auto;
        margin-bottom: 10px;
    }}
    
    .custom-login-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        font-size: 24px;
        font-weight: 700;
        color: {branding_color};
        margin-bottom: 30px;
        text-align: center;
    }}
    
    /* Form Enhancements */
    .form-control {{
        background: #fdfdfd !important;
        border: 1px solid #e2e2e2 !important;
        padding: 12px !important;
        height: auto !important;
    }}
    
    .btn-login {{
        margin-top: 10px;
    }}

    </style>
    
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        const cardBody = document.querySelector(".login-content");
        
        // Only run if we haven't already injected (check for our custom title)
        if(cardBody && !document.querySelector(".custom-login-title")) {{
            
            // 1. Create Login Title
            const title = document.createElement("div");
            title.className = "custom-login-title";
            title.innerText = "Login";
            
            // 2. Create Logo Image
            const logo = document.createElement("img");
            logo.src = "{logo_image}";
            logo.className = "custom-auth-logo";
            
            // 3. Prepend to card body: Logo first, then Title
            // cardBody.prepend(title); 
            // cardBody.prepend(logo); // Prepending in reverse order of desired appearance
            
            // Actually, let's look at the structure. .login-content contains .form-group usually.
            // We want it at the very top of .page-card, inside it.
            
            const pageCard = document.querySelector(".page-card");
            if(pageCard) {{
                // Insert at the beginning of the card
                pageCard.insertBefore(title, pageCard.firstChild);
                pageCard.insertBefore(logo, pageCard.firstChild);
            }}
        }}
    }});
    </script>
    """
    
    settings = frappe.get_single("Website Settings")
    
    # Clean previous scripts
    import re
    if settings.head_html:
        pattern = re.compile(r'<style>\s*/\* Techxle Login Customization.*?</script>', re.DOTALL)
        settings.head_html = re.sub(pattern, "", settings.head_html) 
    
    settings.head_html = (settings.head_html or "") + "\n" + custom_css
    settings.save(ignore_permissions=True)
    print("Injected V5 CSS/JS (Logo Inside, No Overlay)")

if __name__ == "__main__":
    setup()
