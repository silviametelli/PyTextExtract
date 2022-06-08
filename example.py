from PIL import Image
import pytesseract

#### example
path_to_tesseract = r'/usr/local/bin/tesseract'
image_path = r"sample.png"

# Opening the image & storing it in an image object
img = Image.open(image_path)
pytesseract.tesseract_cmd = path_to_tesseract
text = pytesseract.image_to_string(img)

# Displaying the extracted text
print(text[:-1])