import argparse
import PyPDF2

# 명령행 인자를 받습니다.
parser = argparse.ArgumentParser(description='Merge two PDF files into one.')
parser.add_argument('file1', type=str, help='path to the first PDF file')
parser.add_argument('file2', type=str, help='path to the second PDF file')
parser.add_argument('--output', '-o', type=str, default='merged_file.pdf', help='path to the merged PDF file (default: "merged_file.pdf")')
args = parser.parse_args()

# PDF 파일을 열고 병합할 PDFWriter 객체를 생성합니다.
pdf_writer = PyPDF2.PdfWriter()

# 첫 번째 PDF 파일을 엽니다.
pdf_file1 = open(args.file1, 'rb')

# 첫 번째 PDF 파일의 페이지를 추가합니다.
pdf_reader1 = PyPDF2.PdfReader(pdf_file1)
for page_num in range(len(pdf_reader1.pages)):
    page_obj = pdf_reader1.pages[page_num]
    pdf_writer.add_page(page_obj)

# 두 번째 PDF 파일을 엽니다.
pdf_file2 = open(args.file2, 'rb')

# 두 번째 PDF 파일의 페이지를 추가합니다.
pdf_reader2 = PyPDF2.PdfReader(pdf_file2)
for page_num in range(len(pdf_reader2.pages)): 
    page_obj = pdf_reader2.pages[page_num]
    pdf_writer.add_page(page_obj)

# 새로운 PDF 파일을 만듭니다.
pdf_output_file = open(args.output, 'wb')

# PDFWriter 객체로 병합된 페이지를 새로운 PDF 파일에 작성합니다.
pdf_writer.write(pdf_output_file)

# 파일을 닫습니다.
pdf_output_file.close()
pdf_file1.close()
pdf_file2.close()
