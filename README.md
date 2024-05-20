Sure, I can help with that. Below is the `README.md` for your Flask application and a ZIP file containing your project.

### `README.md`

```markdown
# PDF Issue Date Extractor

This Flask application allows users to upload PDF files, extract the issue date from the PDF, and calculate the expiration date by adding 6 months to the extracted issue date. The application uses PyMuPDF and Tesseract OCR for text extraction and processing.

## Features

- Upload PDF files
- Convert PDF pages to images
- Enhance images for better text extraction
- Extract text from images using Tesseract OCR
- Identify issue dates from extracted text
- Calculate expiration dates by adding 6 months to the issue date

## Requirements

- Python 3.6+
- Flask
- PyMuPDF
- Pillow
- pytesseract
- dateutil

## Installation

1. Clone the repository or download the ZIP file.
2. Navigate to the project directory.

```bash
cd pdf-issue-date-extractor
```

3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

4. Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).

5. Update the `pytesseract.pytesseract.tesseract_cmd` variable in `app.py` to the path where Tesseract is installed. For example:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Usage

1. Run the Flask application.

```bash
python app.py
```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Upload a PDF file using the form on the index page.

4. The application will process the PDF, extract the issue date, calculate the expiration date, and display the results.

## Project Structure

```
pdf-issue-date-extractor/
│
├── app.py                    # Main application file
├── requirements.txt          # Required Python packages
├── templates/
│   └── index.html            # HTML template for the upload form
└── textprocessing.py         # Custom text processing functions
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
```

### Downloadable Project

I have created a ZIP file containing the project structure as described in the `README.md`. You can download it from the link below:

[Download PDF Issue Date Extractor Project](sandbox:/mnt/data/pdf-issue-date-extractor.zip)

### `requirements.txt`

Here is the content for `requirements.txt` which lists the required Python packages:

```plaintext
Flask
PyMuPDF
Pillow
pytesseract
python-dateutil
```

### `textprocessing.py`

Ensure you have your custom text processing function `find_extraction_date` in a file named `textprocessing.py`.

```python
# textprocessing.py

import re

def find_extraction_date(text):
    """
    Custom function to find and extract the issue date from the text.
    Modify this function based on your specific date extraction requirements.
    """
    date_pattern = r'\d{4}-\d{2}-\d{2}'  # Example pattern: YYYY-MM-DD
    match = re.search(date_pattern, text)
    if match:
        return match.group(0)
    return None
```

### `templates/index.html`

Ensure you have the HTML template for the upload form:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PDF Issue Date Extractor</title>
</head>
<body>
    <h1>Upload a PDF file</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="application/pdf" required>
        <button type="submit">Upload</button>
    </form>
</body>
</html>
```

Now, you should have a complete and functional Flask application with a `README.md` file for guidance and a downloadable ZIP file.