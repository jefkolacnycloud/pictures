from pathlib import Path
from PIL import Image


# Supported input formats
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

# Output variants
VARIANTS = {
    "low": {
        "max_size": 480,
        "quality": 60,
    },
    "medium": {
        "max_size": 1200,
        "quality": 75,
    },
    "max": {
        "max_size": None,  # Keep original resolution
        "quality": 90,
    },
}


def resize_image(image: Image.Image, max_size: int | None) -> Image.Image:
    """
    Resize image while keeping aspect ratio.
    If max_size is None, the original resolution is kept.
    """
    if max_size is None:
        return image.copy()

    resized = image.copy()
    resized.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return resized


def convert_images_to_webp(folder_path: str) -> None:
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a folder: {folder}")

    images = [
        file for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not images:
        print("No PNG, JPG, or JPEG images found.")
        return

    for image_path in images:
        try:
            with Image.open(image_path) as img:
                # Convert to RGB to avoid issues with PNG transparency or palette modes
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
                    background.alpha_composite(img)
                    img = background.convert("RGB")
                else:
                    img = img.convert("RGB")

                for variant_name, settings in VARIANTS.items():
                    output_image = resize_image(img, settings["max_size"])

                    output_filename = f"{image_path.stem}_{variant_name}.webp"
                    output_path = folder / output_filename

                    output_image.save(
                        output_path,
                        "WEBP",
                        quality=settings["quality"],
                        method=6
                    )

                    print(f"Saved: {output_path}")

        except Exception as error:
            print(f"Failed to convert {image_path.name}: {error}")


if __name__ == "__main__":
    folder_input = input("Enter the folder path containing your images: ").strip()
    convert_images_to_webp(folder_input)