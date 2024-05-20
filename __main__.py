from flask import Flask, request, render_template, jsonify
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageOps
import io
import pytesseract
from textprocessing import find_extraction_date
import tempfile
import shutil

app = Flask(__name__)
# todo: update textract path over here, its installed in some servers already
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def crop_image(image, left=0, top=0, right=1, bottom=1):
    width, height = image.size
    left = int(left * width)
    top = int(top * height)
    right = int(right * width)
    bottom = int(bottom * height)
    return image.crop((left, top, right, bottom))

def enhance_image(image):
    image = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(2)

def pdf_to_images(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        zoom_x, zoom_y = 3.0, 3.0
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes(output="png")

        image = Image.open(io.BytesIO(img_data))
        cropped_image = crop_image(image, left=0.5, top=0.5, right=1.0, bottom=1.0)
        enhanced_image = enhance_image(cropped_image)

        cropped_image_path = os.path.join(output_folder, f"page_{page_number + 1}_cropped.png")
        enhanced_image.save(cropped_image_path)
        # print(f"Saved cropped and enhanced image: {cropped_image_path}")

def pdf_to_text(pdf_path, output_folder):
    pdf_to_images(pdf_path, output_folder)
    text = ""
    for image_filename in sorted(os.listdir(output_folder)):
        if image_filename.endswith("_cropped.png"):
            image_path = os.path.join(output_folder, image_filename)
            # print(f"Processing image for text extraction: {image_path}")
            page_text = pytesseract.image_to_string(Image.open(image_path))
            text += page_text
    return text

def extract_pdf_text(pdf_path, output_folder):
    document = fitz.open(pdf_path)
    all_text = "".join([page.get_text() for page in document])
    pytesseract_extracted = pdf_to_text(pdf_path, output_folder)
    return all_text + "\n" + pytesseract_extracted

def extract_issue_date_custom(pdf_path, output_folder):
    text = extract_pdf_text(pdf_path, output_folder)
    return find_extraction_date(text)

def calculate_expiration_date(issue_date_str):
    issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d")
    expiration_date = issue_date + relativedelta(months=6)
    return expiration_date.strftime("%Y-%m-%d")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    with tempfile.TemporaryDirectory() as upload_folder:
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        issue_date = extract_issue_date_custom(filepath, upload_folder)
        if issue_date:
            expiration_date = calculate_expiration_date(issue_date)
            return jsonify({"issue_date": issue_date, "expiration_date": expiration_date})
        else:
            return jsonify({"error": "Issue date not found"})

if __name__ == "__main__":
    app.run(debug=True)
