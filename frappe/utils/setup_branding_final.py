import frappe
import json
import os

def setup():
    print("Applying Brute Force Branding (JS Injection & Config)...")
    try:
        inject_client_script()
        update_site_config()
        frappe.db.commit()
        frappe.clear_cache()
        print("Branding INJECTED & CONFIG UPDATED! Please Hard Refresh.")
    except Exception as e:
        frappe.db.rollback()
        print(f"Injection Failed: {e}")
        import traceback
        traceback.print_exc()

def inject_client_script():
    # We will create a Client Script that runs on 'List' or specific pages if possible.
    # But for global Desk branding, 'frappe.hooks' is better but we can't edit code easily without restart.
    # So we use a "Client Script" that monkey patches the navbar render if possible.
    # Note: Client Scripts usually run on Form/List load. 
    # We will target 'User' doctype as a proxy for something loaded, or just rely on 'app_name' config.
    
    # Actually, let's aggressively update the `Navbar Settings` -> `items` if needed? No, too complex.
    
    # Re-verify Website Settings brand_html ONE MORE TIME with !important css
    ws = frappe.get_single("Website Settings")
    logo_url = "/files/techxle_logo.jpg"
    brand_text = "Techxle Consulting"
    
    # We add a script tag into the brand_html itself? No, sanitized.
    # We use style tag in brand_html.
    
    stacked_html = f"""
    <div class="techxle-brand" style="display: flex !important; flex-direction: column !important; justify-content: center !important; align-items: start !important; line-height: 1.1 !important;">
        <img src="{logo_url}" style="max-height: 25px !important; width: auto !important; margin-bottom: 2px !important; display: block !important;">
        <span style="font-size: 10px !important; font-weight: bold !important; color: inherit !important; display: block !important;">{brand_text}</span>
    </div>
    <script>
        // Brute force JS injection via HTML if not sanitized (often stripped but worth a shot in some versions)
        // If this runs, it cleans up any "ERPNext" text remaining.
        setTimeout(function() {{
            $('.navbar-brand .hidden-xs').text('{brand_text}'); 
        }}, 1000);
    </script>
    """
    
    ws.brand_html = stacked_html
    ws.save(ignore_permissions=True)
    print("Injected Aggressive HTML/CSS into Website Settings.")

def update_site_config():
    # Update site_config.json
    site_path = frappe.get_site_path()
    config_path = os.path.join(site_path, "site_config.json")
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
        
        data["app_name"] = "Techxle Consulting"
        data["app_title"] = "Techxle Consultancy Services"
        
        with open(config_path, "w") as f:
            json.dump(data, f, indent=1)
            
        print("Updated site_config.json with app_name.")
    else:
        print("site_config.json not found.")

if __name__ == "__main__":
    setup()
