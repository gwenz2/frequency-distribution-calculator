"""
Convert icon.ico to Android launcher icons
"""
from PIL import Image
import os

# Icon sizes for Android
ICON_SIZES = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192
}

def convert_icon():
    # Load the icon
    icon_path = 'frequency_dist_icon.ico'
    
    if not os.path.exists(icon_path):
        print(f"Error: {icon_path} not found!")
        return
    
    # Open the largest size from ico
    img = Image.open(icon_path)
    
    # Get the largest available size
    if hasattr(img, 'size'):
        print(f"Original icon size: {img.size}")
    
    # Create icons for each density
    base_path = os.path.join(os.path.dirname(__file__), 'android', 'app', 'src', 'main', 'res')
    
    for folder, size in ICON_SIZES.items():
        output_dir = os.path.join(base_path, folder)
        
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Resize and save
        resized = img.resize((size, size), Image.LANCZOS)
        output_path = os.path.join(output_dir, 'ic_launcher.png')
        resized.save(output_path, 'PNG')
        
        # Also create round icon
        output_path_round = os.path.join(output_dir, 'ic_launcher_round.png')
        resized.save(output_path_round, 'PNG')
        
        print(f"Created: {output_path} ({size}x{size})")
    
    print("\n✅ Android launcher icons created successfully!")
    print("Note: The app will use these icons after rebuilding.")

if __name__ == "__main__":
    convert_icon()
