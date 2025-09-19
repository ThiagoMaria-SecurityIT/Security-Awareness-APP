import os
import subprocess
import threading
import fitz  # PyMuPDF
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
COURSES_FOLDER = 'courses'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(COURSES_FOLDER):
    os.makedirs(COURSES_FOLDER)

# --- Hardcoded Path to LibreOffice ---
# This is the direct path to the correct executable for background tasks.
LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

# --- App Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COURSES_FOLDER'] = COURSES_FOLDER
app.secret_key = 'supersecretkey'

# --- Helper Function ---
def allowed_file(filename):
    """Checks if the file's extension is .pptx."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pptx'

# --- Conversion Logic ---
def convert_presentation_to_images(pptx_path, course_name):
    """
    Converts a .pptx file to a series of PNG images with robust error handling.
    """
    print("--- Starting Conversion Process ---")
    print(f"Presentation: {pptx_path}")
    print(f"Using LibreOffice from: {LIBREOFFICE_PATH}")

    output_folder = os.path.join(app.config['COURSES_FOLDER'], course_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Step 1: Convert PPTX to PDF using LibreOffice
    try:
        print("Step 1: Converting PPTX to PDF...")
        command = [
            LIBREOFFICE_PATH,
            "--headless",
            "--convert-to", "pdf",
            pptx_path,
            "--outdir", output_folder
        ]
        result = subprocess.run(
            command,
            check=True,
            timeout=60,
            capture_output=True,
            text=True
        )
        print("PPTX to PDF conversion successful.")

    except FileNotFoundError:
        print("\n--- FATAL ERROR ---")
        print(f"The command '{LIBREOFFICE_PATH}' was not found.")
        print("Please ensure the path is correct and LibreOffice is installed.")
        print("-------------------\n")
        return
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print("\n--- FATAL ERROR ---")
        print("LibreOffice failed to convert the file.")
        if hasattr(e, 'stderr'):
            print(f"Error Output (stderr): {e.stderr}")
        print("-------------------\n")
        return
    except Exception as e:
        print(f"\n--- UNEXPECTED ERROR during LibreOffice conversion ---\n{e}\n-------------------\n")
        return

    # Step 2: Convert PDF to PNG images
    pdf_filename = os.path.splitext(os.path.basename(pptx_path))[0] + '.pdf'
    pdf_path = os.path.join(output_folder, pdf_filename)

    if not os.path.exists(pdf_path):
        print("\n--- FATAL ERROR ---")
        print("LibreOffice reported success, but the PDF file was not found.")
        print(f"Expected at: {pdf_path}")
        print("-------------------\n")
        return

    try:
        print("\nStep 2: Converting PDF to PNGs...")
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            output_image_path = os.path.join(output_folder, f"slide_{page_num + 1}.png")
            pix.save(output_image_path)
        doc.close()
        print(f"Successfully converted {len(doc)} slides to PNG.")
    except Exception as e:
        print(f"\n--- UNEXPECTED ERROR during PDF to PNG conversion ---\n{e}\n-------------------\n")
    finally:
        # Step 3: Clean up the intermediate PDF file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"Cleaned up temporary file: {pdf_path}")
    
    print("--- Conversion Process Finished ---\n")

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part in the request.'); return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file.'); return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            pptx_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pptx_path)
            flash(f"'{filename}' uploaded! Conversion starting in the background.")
            course_name = os.path.splitext(filename)[0]
            thread = threading.Thread(target=convert_presentation_to_images, args=(pptx_path, course_name))
            thread.start()
            return redirect(url_for('upload_page'))
        else:
            flash('Invalid file type. Please upload a .pptx file.'); return redirect(request.url)
    
    courses_dir = app.config['COURSES_FOLDER']
    courses_exist = any(os.path.isdir(os.path.join(courses_dir, d)) for d in os.listdir(courses_dir))
    return render_template('upload.html', courses_exist=courses_exist)

@app.route('/courses')
def list_courses():
    courses_dir = app.config['COURSES_FOLDER']
    available_courses = sorted([d for d in os.listdir(courses_dir) if os.path.isdir(os.path.join(courses_dir, d))])
    return render_template('course_list.html', courses=available_courses)

@app.route('/courses/<course_name>')
def view_course(course_name):
    course_path = os.path.join(app.config['COURSES_FOLDER'], course_name)
    if not os.path.isdir(course_path):
        flash("Course not found.")
        return redirect(url_for('list_courses'))
    try:
        slides = [f for f in os.listdir(course_path) if f.startswith('slide_') and f.endswith('.png')]
        slides.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    except (ValueError, IndexError):
        slides = []
    slide_urls = [url_for('get_slide_image', course_name=course_name, filename=s) for s in slides]
    return render_template('course_viewer.html', course_name=course_name, slide_urls=slide_urls)

@app.route('/courses/<course_name>/<filename>')
def get_slide_image(course_name, filename):
    return send_from_directory(os.path.join(app.config['COURSES_FOLDER'], course_name), filename)

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)
