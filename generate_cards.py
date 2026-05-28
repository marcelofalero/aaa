import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# Setup paths
out_dir = "roll20_charsheet/initiative_cards"
os.makedirs(out_dir, exist_ok=True)

# Download sharp geometric font (Montserrat-Bold has a very pointy, clean A and M)
font_path = "Montserrat-Bold.ttf"
if not os.path.exists(font_path):
    print("Downloading Montserrat-Bold font...")
    font_url = "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf"
    try:
        urllib.request.urlretrieve(font_url, font_path)
    except Exception as e:
        print(f"Failed to download Montserrat-Bold: {e}. Falling back to default.")
        font_path = None

def get_font(size):
    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_sci_fi_card(phase_name, priority, color_hex):
    # Colors
    bg_color = (11, 14, 20) # #0b0e14
    accent_color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    accent_dim = tuple(max(0, int(c * 0.3)) for c in accent_color)
    white = (255, 255, 255)
    gray = (120, 130, 150)
    
    # Create image
    w, h = 350, 500
    img = Image.new("RGBA", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw background grid lines (subtle)
    for x in range(25, w, 25):
        draw.line([(x, 0), (x, h)], fill=(20, 25, 35), width=1)
    for y in range(25, h, 25):
        draw.line([(0, y), (w, y)], fill=(20, 25, 35), width=1)
        
    # Draw outer chamfered border
    # Points for a 15px chamfer on corners
    border_pts = [
        (25, 10), (w-25, 10), (w-10, 25), (w-10, h-25),
        (w-25, h-10), (25, h-10), (10, h-25), (10, 25)
    ]
    draw.polygon(border_pts, outline=accent_color, width=3)
    
    # Inner tech border (thin, offset)
    inner_pts = [
        (30, 18), (w-30, 18), (w-18, 30), (w-18, h-30),
        (w-30, h-18), (30, h-18), (18, h-30), (18, 30)
    ]
    draw.polygon(inner_pts, outline=accent_dim, width=1)
    
    # Corner tech brackets
    # Top-Left
    draw.line([(10, 45), (10, 25), (25, 10), (45, 10)], fill=accent_color, width=4)
    # Top-Right
    draw.line([(w-10, 45), (w-10, 25), (w-25, 10), (w-45, 10)], fill=accent_color, width=4)
    # Bottom-Left
    draw.line([(10, h-45), (10, h-25), (25, h-10), (45, h-10)], fill=accent_color, width=4)
    # Bottom-Right
    draw.line([(w-10, h-45), (w-10, h-25), (w-25, h-10), (w-45, h-10)], fill=accent_color, width=4)
    
    # Huge Central Letter (A, G, O, M) - Pointy and Massive!
    central_letter = phase_name[0].upper()
    font_large_letter = get_font(220)
    # Adjusting vertical center slightly for perfect visual balance with the larger size
    draw.text((w/2, h/2 - 45), central_letter, fill=accent_color, font=font_large_letter, anchor="mm")
    
    # Full Phase Name below letter
    font_phase = get_font(28)
    draw.text((w/2, h/2 + 85), phase_name.upper(), fill=white, font=font_phase, anchor="mm")
    
    # Subtitle with tech priority
    font_desc = get_font(12)
    desc_text = f"PRIORITY RANK {priority}"
    draw.text((w/2, h/2 + 125), desc_text, fill=gray, font=font_desc, anchor="mm")
    
    # Tech lines at bottom
    draw.line([(60, h-55), (w-60, h-55)], fill=accent_dim, width=1)
    
    # Footer "ACTION CHECK INITIATIVE"
    font_foot = get_font(11)
    draw.text((w/2, h-40), "ACTION CHECK INITIATIVE", fill=gray, font=font_foot, anchor="mm")
    
    # Save card
    filepath = os.path.join(out_dir, f"{phase_name.lower()}.png")
    img.save(filepath, "PNG")
    print(f"Generated {filepath}")

def draw_card_back():
    bg_color = (8, 10, 15)
    accent_color = (99, 102, 241) # Sleek Indigo #6366f1
    accent_dim = (45, 48, 85)
    gray = (100, 110, 130)
    
    w, h = 350, 500
    img = Image.new("RGBA", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Background grid
    for x in range(25, w, 25):
        draw.line([(x, 0), (x, h)], fill=(16, 20, 30), width=1)
    for y in range(25, h, 25):
        draw.line([(0, y), (w, y)], fill=(16, 20, 30), width=1)
        
    # Outer chamfered border
    border_pts = [
        (25, 10), (w-25, 10), (w-10, 25), (w-10, h-25),
        (w-25, h-10), (25, h-10), (10, h-25), (10, 25)
    ]
    draw.polygon(border_pts, outline=accent_color, width=3)
    
    # Outer brackets
    draw.line([(10, 45), (10, 25), (25, 10), (45, 10)], fill=accent_color, width=4)
    draw.line([(w-10, 45), (w-10, 25), (w-25, 10), (w-45, 10)], fill=accent_color, width=4)
    draw.line([(10, h-45), (10, h-25), (25, h-10), (45, h-10)], fill=accent_color, width=4)
    draw.line([(w-10, h-45), (w-10, h-25), (w-25, h-10), (w-45, h-10)], fill=accent_color, width=4)
    
    # Sleek geometric starburst pattern in center
    cx, cy = w/2, h/2
    draw.ellipse([(cx-60, cy-60), (cx+60, cy+60)], outline=accent_dim, width=2)
    draw.ellipse([(cx-40, cy-40), (cx+40, cy+40)], outline=accent_color, width=1)
    
    # Center logo text
    font_logo = get_font(32)
    draw.text((cx, cy), "AAA", fill=(255, 255, 255), font=font_logo, anchor="mm")
    
    # Subtle geometric tech lines radiating
    draw.line([(cx-120, cy), (cx-70, cy)], fill=accent_dim, width=2)
    draw.line([(cx+70, cy), (cx+120, cy)], fill=accent_dim, width=2)
    draw.line([(cx, cy-120), (cx, cy-70)], fill=accent_dim, width=2)
    draw.line([(cx, cy+70), (cx, cy+120)], fill=accent_dim, width=2)
    
    # Top and bottom labels
    font_alt = get_font(12)
    draw.text((w/2, 40), "ALTERNITY SCI-FI VTT", fill=gray, font=font_alt, anchor="mm")
    draw.text((w/2, h-40), "TACTICAL INITIATIVE CARD", fill=gray, font=font_alt, anchor="mm")
    
    filepath = os.path.join(out_dir, "card_back.png")
    img.save(filepath, "PNG")
    print(f"Generated {filepath}")

if __name__ == "__main__":
    print("Generating cards...")
    # Amazing: Gold, Good: Green, Ordinary: Blue, Marginal: Grey
    draw_sci_fi_card("Amazing", 4, "#ffcc00")
    draw_sci_fi_card("Good", 3, "#10b981")
    draw_sci_fi_card("Ordinary", 2, "#3b82f6")
    draw_sci_fi_card("Marginal", 1, "#9ca3af")
    draw_card_back()
    print("All card graphics generated successfully!")
