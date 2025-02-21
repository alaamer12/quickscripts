# PDF Image Extractor

A Python utility to extract all images from PDF files while maintaining their quality.

## Features

- Extracts images from PDF documents
- Preserves original image quality
- Supports multiple image formats
- Maintains original image metadata
- Organizes extracted images by page
- Progress tracking with rich console output

## Requirements

PyMuPDF
Pillow
rich

## Usage

```bash
python __init__.py input.pdf output_directory
```

## Supported Image Formats

Extracts images in their original format:
- JPEG/JPG
- PNG
- TIFF
- BMP
- Other embedded formats

## Output Organization

- Creates organized output directory
- Images named with page numbers
- Optional metadata preservation
- Maintains original format

## Error Handling

- PDF file validation
- Image extraction verification
- Output directory management
- Format compatibility checking

## Additional Features

- Progress bar during extraction
- Summary report of extracted images
- Option to filter by image size
- Image quality verification