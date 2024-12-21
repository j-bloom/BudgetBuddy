import pytesseract
from PIL import Image
from PyQt5.QtWidgets import QMessageBox
import controllers.functions

def import_screenshot_image(parent_widget, file_path, current_month):
    # Set the path to the Tesseract OCR engine
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust if needed

    try:
        # Open the selected image
        img = Image.open(file_path)
        
        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(img)

        # Process the extracted text and insert into the database
        controllers.functions.process_ocr_and_insert(extracted_text, current_month)

        # Notify user of success
        QMessageBox.information(parent_widget, "OCR Import Successful", "Data has been successfully imported from the screenshot.")
    except Exception as e:
        # Handle exceptions (e.g., Tesseract not working, image issues)
        QMessageBox.critical(parent_widget, "OCR Import Failed", f"An error occurred while processing the image: {e}")
