import pytesseract
from PIL import Image

img_file = "lined_final_edited.jpg"

img = Image.open(img_file)

ocr_result = pytesseract.image_to_string(img)
print(ocr_result)
