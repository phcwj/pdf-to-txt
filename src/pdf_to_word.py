import os
import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Specify the path to your PDF file
pdf_path = './2012_測試驅動的嵌入式 C 語言開發.pdf'

# Create a directory to store the extracted images
images_dir = 'extracted_images'
txt_dir = 'extracted_txt'
tw_dir = 'tw_txt'
os.makedirs(images_dir, exist_ok=True)
os.makedirs(txt_dir, exist_ok=True)
os.makedirs(tw_dir, exist_ok=True)

b_PDF2Image = False
b_Image2Txt = False
b_ch2tw     = True

if b_PDF2Image:
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)

        # Iterate through each page
        for page_num in range(num_pages):
            print(page_num)
            # Extract the page
            page = pdf_reader.pages[page_num]

            # Extract the text from the page
            text = page.extract_text()

            # Save the extracted text to a file
            with open(f'{txt_dir}/page_{page_num+1}.txt', 'w', encoding='utf-8') as text_file:
                text_file.write(text)

            # Convert the PDF page to images
            images = convert_from_path(
                pdf_path,
                first_page=page_num+1,
                last_page=page_num+1,
                poppler_path='./poppler-25.12.0/Library/bin'
            )

            # Save the images to the extracted_images directory
            for i, image in enumerate(images):
                image_path = os.path.join(images_dir, f'page_{page_num+1}_image_{i+1:03d}.png')
                image.save(image_path)

if b_Image2Txt:
    # Perform OCR on the extracted images
    for image_file in os.listdir(images_dir):
        print(image_file)
        image_path = os.path.join(images_dir, image_file)
        image = Image.open(image_path)
        ocr_text = pytesseract.image_to_string(image, lang="chi_sim+eng")   # chi_tra_vert=直書的繁體中文

        # Save the OCR text to a file
        with open(f'{txt_dir}/ocr_{image_file.split('.')[0]}.txt', 'a', encoding='utf-8') as ocr_file:
            ocr_file.write(ocr_text)

if b_ch2tw:
    from opencc import OpenCC

    cc = OpenCC('s2t')  # s2t=簡體到繁體, s2tw=簡體到台灣繁體, s2twp=簡體到台灣繁體，並轉換為台灣常用詞匯
    for ch_txt_file in os.listdir(txt_dir):
        with open(f'{txt_dir}/{ch_txt_file}', 'r', encoding='utf-8') as ch_file:
            txt = ch_file.read()
        with open(f'{tw_dir}/{ch_txt_file}', 'w', encoding='utf-8') as tw_file:
            txt = cc.convert(txt)
            tw_file.write(txt)