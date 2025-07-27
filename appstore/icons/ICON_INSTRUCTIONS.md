# App Icon Generation Instructions

## Generated Files:
- app_icon.svg: Scalable vector icon for all sizes

## To create PNG icons for App Store submission:

### Method 1: Using online converter
1. Upload app_icon.svg to https://convertio.co/svg-png/
2. Convert to PNG at these sizes:
   - 1024x1024 (App Store)
   - 180x180 (iPhone @3x)
   - 120x120 (iPhone @2x)
   - 60x60 (iPhone @1x)
   - 87x87 (Spotlight @3x)
   - 80x80 (Spotlight @2x)
   - 58x58 (Settings @2x)
   - 40x40 (Spotlight @1x)
   - 29x29 (Settings @1x)
   - 20x20 (Notification @1x)

### Method 2: Using macOS Preview
1. Open app_icon.svg in Preview
2. File → Export As → PNG
3. Set custom size for each required dimension

### Method 3: Using ImageMagick (if installed)
```bash
# Install ImageMagick
brew install imagemagick

# Convert to all sizes
for size in 1024 180 120 87 80 60 58 40 29 20; do
  convert app_icon.svg -resize ${size}x${size} app_icon_${size}x${size}.png
done
```

## App Store Requirements:
- All icons must be PNG format
- No transparency allowed
- Square aspect ratio
- Minimum 1024x1024 for App Store Connect
