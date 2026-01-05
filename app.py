from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import img2pdf
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import tempfile
import shutil
from datetime import datetime
import zipfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_IMAGES = {'png', 'jpg', 'jpeg'}
ALLOWED_PDF = {'pdf'}


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def cleanup_old_files():
    """Clean up files older than 1 hour"""
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                if os.path.getmtime(filepath) < datetime.now().timestamp() - 3600:
                    os.remove(filepath)


@app.route('/')
def index():
    cleanup_old_files()
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_image_to_pdf():
    """Convert image to PDF"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_IMAGES):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
        
        # Save uploaded image
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(image_path)
        
        # Convert to PDF
        pdf_filename = f"{os.path.splitext(unique_filename)[0]}.pdf"
        pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
        
        image = Image.open(image_path)
        pdf_bytes = img2pdf.convert(image.filename)
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        image.close()
        
        return jsonify({
            'success': True,
            'message': 'Image converted to PDF successfully',
            'download_url': f'/download/{pdf_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/split', methods=['POST'])
def split_pdf():
    """Split PDF into individual pages"""
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file provided'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_PDF):
            return jsonify({'error': 'Invalid file type. Only PDF allowed'}), 400
        
        # Save uploaded PDF
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(pdf_path)
        
        # Create output directory for split pages
        base_name = os.path.splitext(unique_filename)[0]
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], base_name)
        os.makedirs(output_dir, exist_ok=True)
        
        # Split PDF
        input_pdf = PdfFileReader(open(pdf_path, "rb"))
        num_pages = input_pdf.numPages
        
        for i in range(num_pages):
            output = PdfFileWriter()
            output.addPage(input_pdf.getPage(i))
            output_filename = f"page_{i+1}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, "wb") as output_stream:
                output.write(output_stream)
        
        # Create ZIP file of all pages
        zip_filename = f"{base_name}_split.zip"
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i in range(num_pages):
                page_file = os.path.join(output_dir, f"page_{i+1}.pdf")
                zipf.write(page_file, f"page_{i+1}.pdf")
        
        return jsonify({
            'success': True,
            'message': f'PDF split into {num_pages} pages successfully',
            'pages': num_pages,
            'download_url': f'/download/{zip_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/merge', methods=['POST'])
def merge_pdfs():
    """Merge two PDF files"""
    try:
        if 'pdf1' not in request.files or 'pdf2' not in request.files:
            return jsonify({'error': 'Two PDF files required'}), 400
        
        file1 = request.files['pdf1']
        file2 = request.files['pdf2']
        
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Both files must be selected'}), 400
        
        if not (allowed_file(file1.filename, ALLOWED_PDF) and allowed_file(file2.filename, ALLOWED_PDF)):
            return jsonify({'error': 'Invalid file type. Only PDF allowed'}), 400
        
        # Save uploaded PDFs
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        
        pdf1_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_1_{filename1}")
        pdf2_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_2_{filename2}")
        
        file1.save(pdf1_path)
        file2.save(pdf2_path)
        
        # Merge PDFs
        merger = PdfFileMerger()
        merger.append(pdf1_path)
        merger.append(pdf2_path)
        
        merged_filename = f"{timestamp}_merged.pdf"
        merged_path = os.path.join(app.config['OUTPUT_FOLDER'], merged_filename)
        
        with open(merged_path, 'wb') as f:
            merger.write(f)
        merger.close()
        
        return jsonify({
            'success': True,
            'message': 'PDFs merged successfully',
            'download_url': f'/download/{merged_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download processed file"""
    try:
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
