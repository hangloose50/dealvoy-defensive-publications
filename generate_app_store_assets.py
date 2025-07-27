#!/usr/bin/env python3
"""
App Icon Generator for iOS App Store
Creates all required app icon sizes for Dealvoy mobile app
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_dealvoy_app_icon():
    """Create Dealvoy app icon in all required sizes"""
    
    # Define required icon sizes for iOS
    icon_sizes = [
        1024,  # App Store
        180,   # iPhone App iOS 7-13 60pt@3x
        120,   # iPhone App iOS 7-13 60pt@2x
        87,    # iPhone Spotlight iOS 7-13 29pt@3x
        80,    # iPhone Spotlight iOS 7-13 40pt@2x
        60,    # iPhone Spotlight iOS 7-13 20pt@3x
        58,    # iPhone Settings iOS 7-13 29pt@2x
        40,    # iPhone Settings iOS 7-13 20pt@2x
        29,    # iPhone Settings iOS 7-13 29pt@1x
        20,    # iPhone Settings iOS 7-13 20pt@1x
        167,   # iPad Pro App iOS 9-13 83.5pt@2x
        152,   # iPad App iOS 7-13 76pt@2x
        144,   # iPad App iOS 7-13 72pt@2x (Legacy)
        76,    # iPad App iOS 7-13 76pt@1x
        72,    # iPad App iOS 7-13 72pt@1x (Legacy)
    ]
    
    # Create icons directory
    icons_dir = Path("/Users/dusti1/OneDrive/Documents/AmazonScraperToolkit/appstore/icons")
    icons_dir.mkdir(exist_ok=True)
    
    # Create base 1024x1024 icon
    base_size = 1024
    img = Image.new('RGB', (base_size, base_size), color='#2563eb')
    draw = ImageDraw.Draw(img)
    
    # Draw circular background with gradient effect
    # Create a circle with rounded edges
    margin = 60
    circle_size = base_size - (margin * 2)
    circle_pos = margin
    
    # Draw main circle
    draw.ellipse([circle_pos, circle_pos, circle_pos + circle_size, circle_pos + circle_size], 
                fill='#1d4ed8', outline='#1e40af', width=8)
    
    # Add "D" letter in center
    try:
        # Try to use a system font
        font_size = int(base_size * 0.4)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text = "D"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (base_size - text_width) // 2
    text_y = (base_size - text_height) // 2 - 20  # Slight adjustment
    
    # Draw the "D" with shadow effect
    shadow_offset = 4
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, 
              font=font, fill='#1e3a8a')  # Shadow
    draw.text((text_x, text_y), text, font=font, fill='#ffffff')  # Main text
    
    # Add small "DEALVOY" text at bottom
    subtitle_font_size = int(base_size * 0.08)
    try:
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", subtitle_font_size)
    except:
        subtitle_font = ImageFont.load_default()
    
    subtitle_text = "DEALVOY"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (base_size - subtitle_width) // 2
    subtitle_y = base_size - 150
    
    draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill='#ffffff')
    
    # Save all required sizes
    for size in icon_sizes:
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        filename = f"app_icon_{size}x{size}.png"
        filepath = icons_dir / filename
        resized_img.save(filepath, "PNG", quality=100)
        print(f"✅ Created {filename}")
    
    # Also save as AppIcon.png for general use
    img.save(icons_dir / "AppIcon.png", "PNG", quality=100)
    print(f"✅ Created AppIcon.png (1024x1024)")
    
    print(f"\n📱 All app icons saved to: {icons_dir}")
    return str(icons_dir)

def create_app_store_screenshots():
    """Create placeholder screenshots for App Store submission"""
    
    screenshots_dir = Path("/Users/dusti1/OneDrive/Documents/AmazonScraperToolkit/appstore/screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    # Define screenshot dimensions for different devices
    screenshot_specs = {
        "iPhone_6.7": (1290, 2796),  # iPhone 14 Pro Max
        "iPhone_6.5": (1242, 2688),  # iPhone XS Max
        "iPhone_5.5": (1242, 2208),  # iPhone 8 Plus
        "iPad_Pro_12.9": (2048, 2732),  # iPad Pro 12.9"
        "iPad_Pro_11": (1668, 2388),    # iPad Pro 11"
    }
    
    for device, (width, height) in screenshot_specs.items():
        # Create screenshot image
        img = Image.new('RGB', (width, height), color='#f9fafb')
        draw = ImageDraw.Draw(img)
        
        # Draw header
        header_height = 120
        draw.rectangle([0, 0, width, header_height], fill='#2563eb')
        
        # Add title
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        except:
            title_font = ImageFont.load_default()
        
        title_text = "Dealvoy Dashboard"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        title_y = (header_height - (title_bbox[3] - title_bbox[1])) // 2
        
        draw.text((title_x, title_y), title_text, font=title_font, fill='#ffffff')
        
        # Draw content cards
        card_margin = 40
        card_height = 200
        card_y = header_height + 60
        
        for i in range(3):
            card_top = card_y + (i * (card_height + 30))
            draw.rectangle([card_margin, card_top, width - card_margin, card_top + card_height], 
                         fill='#ffffff', outline='#e5e7eb', width=2)
            
            # Add card content
            try:
                card_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            except:
                card_font = ImageFont.load_default()
            
            card_texts = ["AI Deal Analysis", "Profit Forecasting", "Market Trends"]
            card_text = card_texts[i]
            
            text_x = card_margin + 30
            text_y = card_top + 30
            draw.text((text_x, text_y), card_text, font=card_font, fill='#1f2937')
            
            # Add metrics
            metrics_y = text_y + 60
            draw.text((text_x, metrics_y), "ROI: 75.4% | Profit: $6,996", 
                     font=card_font, fill='#10b981')
        
        # Save screenshot
        filename = f"{device}_screenshot.png"
        filepath = screenshots_dir / filename
        img.save(filepath, "PNG", quality=100)
        print(f"📱 Created {filename} ({width}x{height})")
    
    print(f"\n📱 All screenshots saved to: {screenshots_dir}")
    return str(screenshots_dir)

def main():
    print("🎨 Generating Dealvoy App Icons and Screenshots...")
    print("=" * 60)
    
    # Create app icons
    icons_path = create_dealvoy_app_icon()
    
    print("\n" + "=" * 60)
    
    # Create screenshots
    screenshots_path = create_app_store_screenshots()
    
    print("\n" + "=" * 60)
    print("✅ APP STORE ASSETS GENERATION COMPLETE")
    print(f"📁 Icons: {icons_path}")
    print(f"📁 Screenshots: {screenshots_path}")
    print("\n🚀 Ready for App Store Connect submission!")

if __name__ == "__main__":
    main()
