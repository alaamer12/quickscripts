from docx import Document
import os
from tqdm import tqdm

dir_path = r'D:\Documentations\Recap'

def merge_docx(docx_files, output_file):
    merged_document = Document()
    try:
        for docx_file in tqdm(docx_files, desc='Merging files', unit='files'):
            if not docx_file.endswith('.docx'):
                continue
            abs_docx_file = os.path.join(dir_path, docx_file)
            if not os.path.exists(abs_docx_file):
                continue
            if os.path.isdir(abs_docx_file):
                continue
            # Add a new page with the file name as the title
            doc: Document = Document(abs_docx_file)
            for element in doc.element.body:
                merged_document.element.body.append(element)
            tqdm.write(f"Appended elements from {abs_docx_file} to {output_file}")
        merged_document.save(output_file)
    except Exception as e:
        tqdm.write(f'Error while merging docx files: {e}')

# Example usage
docx_files = [file for file in os.listdir(dir_path) if file.endswith('.docx')]
docx_files.sort()
output_file = 'merged_file.docx'
merge_docx(docx_files, output_file)
