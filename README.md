# QuickScripts Python Utilities

A collection of powerful Python utilities for file manipulation, document conversion, and automation tasks.

## 🚀 Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Navigate to the desired utility directory
4. Run the script as per individual README instructions

## 📦 Available Utilities

### Document Processing
- **[convert_docx_to_nice_style](./convert_docx_to_nice_style)**: Transform plain Word documents into professionally styled ones
- **[md2docx](./md2docx)**: Convert Markdown files to beautifully formatted Word documents
- **[merge_docx_files.py](./merge_docx_files.py)**: Combine multiple Word documents
- **[pdf_to_docx](./pdf_to_docx)**: Convert PDF files to editable Word format

### PDF Utilities
- **[extract_pdf_images](./extract_pdf_images)**: Extract images from PDF files
- **[merge_pdfs](./merge_pdfs)**: Combine multiple PDF files

### File Management
- **[hard-coded_force_deletion](./hard-coded_force_deletion)**: Forcefully delete stubborn files and directories
- **[hide_dirs_and_files.py](./hide_dirs_and_files.py)**: Hide/unhide files and directories
- **[datatypes_remover.py](./datatypes_remover.py)**: Clean up specific file types

### Excel Tools
- **[enhance_excel_file_styling](./enhance_excel_file_styling)**: Apply professional styling to Excel files

### Web Development
- **[create_favicon](./create_favicon)**: Generate favicons for web applications

### Development Tools
- **[git_commiter_to_repo](./git_commiter_to_repo)**: Automate Git repository operations
- **[fix_indention.py](./fix_indention.py)**: Fix code indentation
- **[to_pascal.py](./to_pascal.py)**: Convert text to PascalCase
- **[pytaskbar_demo](./pytaskbar_demo)**: Windows taskbar progress demonstration

### Other Utilities
- **[generate_profile_cards.py](./generate_profile_cards.py)**: Create profile cards
- **[zib_bomb.py](./zib_bomb.py)**: ZIP file handling utility

## 🛠️ Global Requirements

Main dependencies (see individual READMEs for specific requirements):
```
python-docx
PyPDF2
Pillow
openpyxl
rich
gitpython
pywin32 (Windows only)
```

## 🔧 Installation

1. Ensure Python 3.6+ is installed
2. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📚 Documentation

Each utility has its own README with specific:
- Features and capabilities
- Installation requirements
- Usage instructions
- Error handling
- Additional features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## ⚠️ Important Notes

- Some utilities require Windows-specific dependencies
- Always check individual README files for specific requirements
- Use virtual environment to avoid dependency conflicts
- Test utilities with sample data before using with important files

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details