import random
import argparse
import os
from PIL import Image, ImageFilter, ImageEnhance

# --- CONFIGURATION ---
PAGE_WIDTH, PAGE_HEIGHT = 1240, 1754  # A4 @ 150 DPI
MARGINS = {'top': 150, 'bottom': 150, 'left': 120, 'right': 120}
BASE_CHAR_SIZE = 40
LINE_HEIGHT = 45         # <--- Reduced from 80 for tighter rows
WORD_SPACING = 20
CHAR_SPACING_BASE = -29

# Sprite Sheet Info
CHARACTERS = list("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,:?!+-=/'()\"")
SAMPLES_PER_CHAR = 10
CELL_SIZE = 128

def load_spritesheet(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sprite sheet not found: {path}")
    
    sheet = Image.open(path).convert("RGBA")
    
    # Process transparency: Convert white to transparent
    data = sheet.getdata()
    # Using a threshold of 230 to catch off-white "paper" pixels in the sprites
    new_data = [(255, 255, 255, 0) if (item[0] > 230 and item[1] > 230 and item[2] > 230) else item for item in data]
    sheet.putdata(new_data)

    sprites = {}
    for row, char in enumerate(CHARACTERS):
        sprites[char] = [
            sheet.crop((col * CELL_SIZE, row * CELL_SIZE, (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE))
            for col in range(SAMPLES_PER_CHAR)
        ]
    return sprites

def create_new_page():
    return Image.new("RGBA", (PAGE_WIDTH, PAGE_HEIGHT), (255, 255, 255, 255))

def process_text(text, sprites, output_dir, output_prefix):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    pages = []
    current_page = create_new_page()
    x, y = MARGINS['left'], MARGINS['top']

    lines = text.splitlines()

    for line in lines:
        # Handle empty lines (extra enters)
        if not line.strip():
            y += LINE_HEIGHT
            continue

        words = line.split(' ')
        for word in words:
            # Word wrapping check
            est_word_w = len(word) * (BASE_CHAR_SIZE + CHAR_SPACING_BASE)
            if x + est_word_w > PAGE_WIDTH - MARGINS['right']:
                x = MARGINS['left']
                y += LINE_HEIGHT

            # Page splitting check
            if y > PAGE_HEIGHT - MARGINS['bottom']:
                pages.append(current_page)
                current_page = create_new_page()
                x, y = MARGINS['left'], MARGINS['top']

            for char in word:
                if char not in sprites: continue
                
                char_img = random.choice(sprites[char]).copy()
                
                # Realism Transforms
                scale = random.gauss(1.0, 0.02)
                new_size = int(BASE_CHAR_SIZE * scale)
                char_img = char_img.resize((new_size, new_size), Image.Resampling.LANCZOS)
                char_img = char_img.rotate(random.uniform(-3, 3), resample=Image.Resampling.BICUBIC, expand=True)
                
                # Paste
                paste_x = int(x + random.gauss(0, 0.5))
                # Vertical alignment centering
                paste_y = int(y + random.gauss(0, 1.0) + (BASE_CHAR_SIZE - char_img.height) // 2)
                current_page.paste(char_img, (paste_x, paste_y), char_img)
                
                x += new_size + CHAR_SPACING_BASE + random.gauss(0, 1.0)

            x += WORD_SPACING + random.gauss(0, 2.0)
        
        # Reset X and move to next line
        x = MARGINS['left']
        y += LINE_HEIGHT

    pages.append(current_page)
    
    for i, page in enumerate(pages):
        out_name = f"{output_prefix}_{i+1}.png"
        full_path = os.path.join(output_dir, out_name)
        page.convert("RGB").save(full_path)
        print(f"-> Saved: {full_path}")

def main():
    parser = argparse.ArgumentParser(description="Handwriting Document Generator")
    parser.add_argument("input", help="Path to the .txt file")
    parser.add_argument("--sheet", default="handwriting_spritesheet00.png", help="Path to sprite sheet")
    parser.add_argument("--out_dir", default="output", help="Directory to save images")
    parser.add_argument("--prefix", default="page", help="Prefix for filenames")
    
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sprites = load_spritesheet(args.sheet)
        process_text(content, sprites, args.out_dir, args.prefix)
        print("\nSuccess! Check your output folder.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
