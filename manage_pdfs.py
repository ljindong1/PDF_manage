import sys
import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem

from PyPDF2 import PdfReader, PdfWriter


def parse_range(range_str):
    parts = range_str.split(',')
    result = []
    for part in parts:
        if not part.replace('-', '').isdigit():
            raise ValueError("잘못된 입력입니다: {}".format(part))
        if '-' in part:
            start, end = part.split('-')
            start = int(start.strip())
            end = int(end.strip())
            result.extend(range(start, end + 1))
        else:
            result.append(int(part.strip()))
    return result


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Manage Program')
        self.setGeometry(100, 100, 400, 500)

        # QWidget을 생성합니다.
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # QVBoxLayout을 생성합니다.
        layout_v = QVBoxLayout(widget)

        # QListWidget 위젯을 생성하고, QVBoxLayout에 추가합니다.
        self.listwidget = MyListWidget()
        layout_v.addWidget(self.listwidget)

         # QHBoxLayout을 생성합니다.
        layout_h1 = QHBoxLayout()
        layout_h2 = QHBoxLayout()

        # merge와 clear 위젯을 생성하고, layout_h1(QHBoxLayout)에 추가합니다.
        button = QPushButton('merge PDF')
        button2 = QPushButton('Clear')
        layout_h1.addWidget(button)      
        layout_h1.addWidget(button2)
        
        # select page 버튼과 Edit를 생성하고,layout_h2에 추가합니다. 
        pBtn_select = QPushButton('extracting Pages')
        self.lEdit_page = QLineEdit() 
        self.lEdit_page.setPlaceholderText('입력 방법: 1,2,5-7')
        
        layout_h2.addWidget(pBtn_select)
        layout_h2.addWidget(self.lEdit_page)      
       
        # QHBoxLayout을 QVBoxLayout에 추가합니다.
        layout_v.addLayout(layout_h1)
        layout_v.addLayout(layout_h2)
        
        # 버튼 클릭 이벤트를 처리할 메서드를 연결합니다.
        # new_button.clicked.connect(self.set_output_filename)
        button.clicked.connect(self.merge_pdfs)
        button2.clicked.connect(self.clear_list) 
        pBtn_select.clicked.connect(self.select_Page)  

        self.show()
        
    def merge_pdfs(self):
        # listwidget이 비어 있는지 확인하고, 비어 있다면 "파일 없음" 메시지를 출력하고 메서드를 종료합니다.
        if self.listwidget.count() == 0:
            QMessageBox.warning(self, "안내", "통합할 파일이 없습니다.!!!")
            return        
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)")

        if file_name:
            if not file_name.endswith(".pdf"):
                file_name += ".pdf"
        else:           
            return

        # 사용자가 입력한 텍스트가 있으면 해당 이름으로 저장하고, 없으면 기본 이름으로 저장합니다.
        pdf_writer = PdfWriter()

        for index in range(self.listwidget.count()):
            input_path = self.listwidget.item(index).text()
            pdf_reader = PdfReader(input_path)

            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])

        with open(file_name, "wb") as output_file:
            pdf_writer.write(output_file)
            
        self.clear_list()            
        QMessageBox.information(self, "성공", f"성공했습니다: {file_name}")
        
    def clear_list(self):
        self.listwidget.clear()
        self.lEdit_page.clear()
        
    def select_Page(self):
        current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        default_output_name = f"merged_output_{current_time}.pdf"
        
        # listwidget이 비어 있는지 확인하고, 비어 있다면 "파일 없음" 메시지를 출력하고 메서드를 종료합니다.
        if self.listwidget.count() == 0:
            QMessageBox.warning(self, "안내", "추출할 PDF 파일을 가져오세요.!!!")
            return        
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)")

        if file_name:
            if not file_name.endswith(".pdf"):
                file_name += ".pdf"
        else: 
            file_name =  default_output_name     
        
        try:    
            selected_page = parse_range(self.lEdit_page.text())
        except ValueError as e:
            QMessageBox.information(self, "입력 에러", "에러 발생: {}".format(e))
            # self.lEdit_page.setText("")
            
        pdf_writer = PdfWriter()    
        
        input_path = self.listwidget.item(0).text()
        pdf_reader = PdfReader(input_path)
        
        total_page = len(pdf_reader.pages)
        
        # new_page_number = 0
        for page in selected_page:  
            if page <= total_page:     
                pdf_writer.add_page(pdf_reader.pages[page-1])        

        
        with open(file_name, "wb") as output_file:
            pdf_writer.write(output_file)
            
        self.clear_list()            
        QMessageBox.information(self, "성공", f"성공했습니다: {file_name}")
          
        
class MyListWidget(QListWidget):

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.CopyAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and all(url.toLocalFile().endswith('.pdf') for url in event.mimeData().urls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls() and all(url.toLocalFile().endswith('.pdf') for url in event.mimeData().urls()):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = [url.toLocalFile() for url in event.mimeData().urls()]
            for url in urls:
                if url.endswith('.pdf'):
                    item = QListWidgetItem()
                    item.setText(url)
                    self.addItem(item)

            if event.source() is not self:
                event.setDropAction(Qt.CopyAction)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
