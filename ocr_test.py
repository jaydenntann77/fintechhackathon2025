import cv2
import pytesseract

image_path = "/Users/limyucheng/Downloads/sample_doc2.png"
image = cv2.imread(image_path)

# Preprocessing of image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
_, thresh = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

# Perform OCR
text = pytesseract.image_to_string(thresh)
clean_text = ' '.join(text.split())


print("Extracted Text:")
print(text)
