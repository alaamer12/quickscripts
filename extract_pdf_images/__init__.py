import fitz  # PyMuPDF
from PIL import Image
from fpdf import FPDF
import io
import os


def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)

        for img in image_list:
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            img_ext = base_image["ext"]
            img_name = f"image_{page_num + 1}_{xref}.{img_ext}"

            # Save the extracted image to a bytes buffer
            image_stream = io.BytesIO(image_bytes)
            images.append((img_name, image_stream))

    pdf_document.close()
    return images


def create_pdf_from_images(image_list, output_pdf_path):
    # Ensure the directory exists
    tmp_dir = "E:\\tmp\\"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    pdf = FPDF()

    # A4 page dimensions in millimeters
    pdf_w, pdf_h = 210, 297

    for img_name, img_stream in image_list:
        img = Image.open(img_stream)
        img_width, img_height = img.size

        # Calculate aspect ratio and resizing to fit within A4 dimensions
        aspect_ratio = img_width / img_height

        if aspect_ratio > 1:
            # Landscape or wide image
            w = pdf_w
            h = pdf_w / aspect_ratio
        else:
            # Portrait or tall image
            h = pdf_h
            w = pdf_h * aspect_ratio

        # Ensure the image fits within the PDF page
        if w > pdf_w:
            w = pdf_w
            h = w / aspect_ratio
        if h > pdf_h:
            h = pdf_h
            w = h * aspect_ratio

        pdf.add_page()

        # Center the image on the PDF page
        x_offset = (pdf_w - w) / 2
        y_offset = (pdf_h - h) / 2

        # Save image temporarily to disk and add it to the PDF
        img_path = os.path.join(tmp_dir, img_name)
        img.save(img_path)
        pdf.image(img_path, x=x_offset, y=y_offset, w=w, h=h)

    pdf.output(output_pdf_path)


if __name__ == "__main__":
    input_pdf = r"C:\Users\amrmu\Downloads\Clean Architecture_ A Craftsmans Guide to Software Structure and Design.pdf"
    output_pdf = r"output_images.pdf"

    # Extract images from the input PDF
    images = extract_images_from_pdf(input_pdf)

    # Create a new PDF from extracted images
    create_pdf_from_images(images, output_pdf)
