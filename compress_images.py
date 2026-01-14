import os
from PIL import Image

# ===== CONFIG =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "input_images")  # Folder next to script
DEST_DIR = os.path.join(BASE_DIR, "tiny_output")     # Output folder
os.makedirs(DEST_DIR, exist_ok=True)

IMAGE_EXT = (".jpg", ".jpeg", ".png")  # Supported formats
QUALITY = 85                          # JPG quality
WEBP = False                            # Convert to WebP for better compression

# ===== FUNCTION =====
def compress_image(src_path, dest_path):
    with Image.open(src_path) as img:

        # Convert transparent images safely
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Decide output format
        if WEBP:
            base_name = os.path.splitext(os.path.basename(src_path))[0] + ".webp"
            dest_path = os.path.join(DEST_DIR, base_name)
            img.save(dest_path, "WEBP", quality=QUALITY, method=6)
        else:
            if src_path.lower().endswith((".jpg", ".jpeg")):
                img.save(dest_path, optimize=True, quality=QUALITY, progressive=True)
            elif src_path.lower().endswith(".png"):
                img.save(dest_path, optimize=True)

    return os.path.getsize(src_path), os.path.getsize(dest_path)


# ===== MAIN =====
def main():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Create folder: {SOURCE_DIR}")
        return

    total_before = 0
    total_after = 0
    count = 0

    for file in os.listdir(SOURCE_DIR):
        if file.lower().endswith(IMAGE_EXT):
            src = os.path.join(SOURCE_DIR, file)
            dst = os.path.join(DEST_DIR, file)

            try:
                before, after = compress_image(src, dst)
                total_before += before
                total_after += after
                count += 1
                print(f"[OK] {file} {before//1024}KB → {after//1024}KB")
            except Exception as e:
                print(f"[ERROR] {file} -> {e}")

    if total_before > 0:
        saved = 100 - (total_after / total_before * 100)
        print(f"\n🔥 Compressed {count} images, saved {saved:.2f}% of space.")


if __name__ == "__main__":
    main()
