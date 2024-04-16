import os
import PyPDF2
import pprint
PATH = r"F:\ebooks"

def get_pdfs(path):
    pdfs = []
    i = 0
    for root, dirs, files in os.walk(path):
        # print(f"({i + 1}) {root}")
        i += 1
        for file in files:
            if file.endswith(".pdf"):
                pdfs.append(os.path.join(root, file))
    # pprint.pprint(pdfs)
    return pdfs


def merge(pdfs: list, path: str = PATH):
    pdf_writer = PyPDF2.PdfWriter()

    for pdf in pdfs:
        try:
            with open(pdf, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)
        except Exception as e:
            print(e)
            pass

    with open(os.path.join(path, "merged_output.pdf"), "wb") as out:
        print(f"Output file: {os.path.join(path, 'merged_output.pdf')}")
        pdf_writer.write(out)

if __name__ == "__main__":
    # merge(get_pdfs(PATH))
    # reader = PyPDF2.PdfReader(os.path.join(PATH, "merged_output.pdf"))
    # lender = (len(reader.pages))
    # print(lender // 80)
    print([os.path.basename(base) for base in get_pdfs(PATH)])
    print(len(get_pdfs(PATH)))
    pass