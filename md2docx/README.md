# Markdown to Word Document Converter

A powerful Python script that converts Markdown files into professionally formatted Word documents with enhanced styling and features.

## Features

- Converts Markdown to beautifully styled Word documents
- Automatically generates Table of Contents
- Custom heading styles with professional formatting
- Support for multiple heading levels
- List processing with proper indentation
- Custom margin settings
- Professional document styling

## Requirements

```
python-docx
```

## Usage

```python
from md2docx_1 import convert_markdown_to_docx

# Convert a markdown string
markdown_content = """
# Title
## Subtitle
Content here
"""
convert_markdown_to_docx(markdown_content, 'output.docx')

# Or use md2docx_2.py for enhanced features
```

## Supported Markdown Elements

- Headers (# to ######)
- Lists (ordered and unordered)
- Paragraphs
- Basic text formatting
- Code blocks
- Tables

## Document Styling

- Professional fonts (Segoe UI)
- Consistent spacing
- Custom margins
- Enhanced heading formats
- Clean paragraph styling

## Version Information

Two versions available:
- `md2docx_1.py`: Basic conversion with professional styling
- `md2docx_2.py`: Enhanced features and additional formatting options