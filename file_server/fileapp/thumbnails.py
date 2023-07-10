from PIL import Image
from io import BytesIO
import os
import fitz
# import pdf2image
def generate_thumbnail(file_path):
    file_ext = os.path.splitext(file_path)[1]
    if file_ext.lower() == '.pdf':
        img_bytes = pdf_to_image(file_path)
    else:
        img = Image.open(file_path)
        img.thumbnail((500, 500))
        thumb_io = BytesIO()
        img.save(thumb_io, img.format)
        img_bytes = thumb_io.getvalue()
    return img_bytes

def pdf_to_image(pdf_file):
    with fitz.open(pdf_file) as doc:
        # Load the first page of the PDF file as an image
        page = doc.load_page(0)
        pix = page.get_pixmap()
        img_bytes = pix.tobytes()
    return img_bytes

