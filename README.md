# PDF Converter Pro

A modern web-based PDF converter built with Flask. Convert images to PDF, split PDFs into individual pages, and merge multiple PDFs.

## Features

- 🖼️ **Image to PDF Conversion** - Convert JPG/PNG images to PDF format
- ✂️ **PDF Splitting** - Split multi-page PDFs into individual pages
- 🔗 **PDF Merging** - Merge two PDF files into one
- 📱 **Responsive Design** - Works on desktop and mobile devices
- ✨ **Modern UI** - Premium interface with smooth animations

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Convert Image to PDF
1. Click on the "Convert to PDF" tab
2. Upload a JPG or PNG image
3. Click "Convert to PDF"
4. Download your converted PDF file

### Split PDF
1. Click on the "Split PDF" tab
2. Upload a multi-page PDF file
3. Click "Split PDF"
4. Download the ZIP file containing all individual pages

### Merge PDFs
1. Click on the "Merge PDFs" tab
2. Upload the first PDF file
3. Upload the second PDF file
4. Click "Merge PDFs"
5. Download your merged PDF file

## Technical Stack

- **Backend**: Flask (Python)
- **PDF Processing**: PyPDF2, img2pdf
- **Image Processing**: Pillow
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with gradients and animations

## File Structure

```
sample/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # CSS styling
│   └── script.js         # JavaScript functionality
├── uploads/              # Temporary upload folder (auto-created)
└── outputs/              # Processed files folder (auto-created)
```

## Notes

- Maximum file size: 50MB
- Uploaded and processed files are automatically cleaned up after 1 hour
- Supported image formats: PNG, JPG, JPEG
- Supported PDF operations: Convert, Split, Merge

## Version

PDF Converter Pro v2.0 - Flask Edition
