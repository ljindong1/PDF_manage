import argparse
import PyPDF2

# 명령행 인자를 받습니다.
parser = argparse.ArgumentParser(description='Merge two PDF files into one.')
parser.add_argument('files', type=str, nargs='+', help='paths to the PDF files to be merged')
parser.add_argument('--output', '-o', type=str, default='merged_file.pdf', help='path to the merged PDF file (default: "merged_file.pdf")')
args = parser.parse_args()

# PDF 파일을 열고 병합할 PDFWriter 객체를 생성합니다.
pdf_writer = PyPDF2.PdfWriter()

# 각 PDF 파일을 순회하면서 병합합니다.
for file in args.files:
    pdf_file = open(file, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # 해당 PDF 파일의 페이지를 추가합니다.
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        pdf_writer.add_page(page_obj)
        

    pdf_file.close()
    
# 새로운 PDF 파일을 만듭니다.
pdf_output_file = open(args.output, 'wb')

# PDFWriter 객체로 병합된 페이지를 새로운 PDF 파일에 작성합니다.
pdf_writer.write(pdf_output_file)

# 파일을 닫습니다.
pdf_output_file.close()

