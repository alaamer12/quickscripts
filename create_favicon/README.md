# Favicon Generator

A Python utility to create favicons from images for web applications.

## Features

- Converts images to favicon format (.ico)
- Supports multiple input image formats (PNG, JPG, etc.)
- Creates favicons in multiple sizes
- Maintains image quality
- Simple command-line interface

## Requirements

```
Pillow
```

## Usage

```bash
python __init__.py input_image.png output_favicon.ico
```

## Supported Input Formats

- PNG
- JPEG/JPG
- BMP
- Other formats supported by Pillow

## Output Specifications

- Format: ICO
- Multiple sizes included:
  - 16x16
  - 32x32
  - 48x48
  - 64x64

## Error Handling

- Input file validation
- Format compatibility checking
- Size validation
- Output path verification