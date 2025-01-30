import fitz  # PyMuPDF


def extract_bold_text(pdf_path):
    doc = fitz.open(pdf_path)
    bold_text = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    # Check if the font is bold
                    if 'bold' in span["font"].lower():
                        bold_text.append(span["text"])

    return bold_text


# Example usage
pdf_path = r"D:\Posts\Users\Facebook\Business\Tealim\Posts\Encouraging Educational Content.pdf"
bold_text_list = extract_bold_text(pdf_path)

# Print or save the bold text
for text in bold_text_list:
    print(text)

# Save the bold text to a file (optional)
with open("bold_text.txt", "w") as f:
    for text in bold_text_list:
        f.write(text + "\n")
