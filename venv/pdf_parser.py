import easyocr
from pdf2image import convert_from_path
from PIL import Image
import pytesseract


def get_list_of_pdfs():
    pass


def mass_pdf2img_convert():
    #get list of pdf from path -> convert each to img
    pass


def get_list_of_imgs():
    pass


def mass_img2txt_convert():
    #get list of imgs -> convert each to raw txt
    pass


def convert_pdf2img(file='f1.pdf'):
    images = convert_from_path(file, 350, poppler_path=r'C:\FILES_C\progs\election\poppler-23.07.0\Library\bin')
    for i, image in enumerate(images):
        fname = 'image' + str(i) + '.png'
        image.save(fname, "PNG")


def parse_from_img(filepath='image5.png'):
     reader = easyocr.Reader(['en'])
     result1 = reader.readtext(filepath, detail=0, paragraph=True)
    #result = pytesseract.image_to_string(Image.open(filepath))
     return result1


if __name__ == '__main__':
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(parse_from_img())
