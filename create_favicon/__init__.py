from PIL import Image
import cairosvg
import io
import os


def svg_to_png(svg_path, size):
    png_data = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
    return Image.open(io.BytesIO(png_data))


def create_favicon(svg_path, ico_path):
    # Create images of different sizes
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = svg_to_png(svg_path, size)
        images.append(img)

    # Save as ICO file with multiple sizes
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(size, size) for size in sizes],
        append_images=images[1:]
    )


if __name__ == '__main__':
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Input and output paths
    svg_path = os.path.join(script_dir, 'logo_final.svg')
    ico_path = os.path.join(script_dir, 'favicon.ico')

    create_favicon(svg_path, ico_path)
    print(f"Favicon created at: {ico_path}")
