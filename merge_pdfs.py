import sys
import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem

from PyPDF2 import PdfReader, PdfWriter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF merge Program')
        self.setGeometry(100, 100, 400, 500)

        # QWidget을 생성합니다.
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # QVBoxLayout을 생성합니다.
        layout_v = QVBoxLayout(widget)

        # QListWidget 위젯을 생성하고, QVBoxLayout에 추가합니다.
        self.listwidget = MyListWidget()
        layout_v.addWidget(self.listwidget)

        # 새로운 QHBoxLayout을 생성합니다.
        layout_h1 = QHBoxLayout()

        # QLabel 위젯을 생성하고, QHBoxLayout에 추가합니다.
        label = QLabel("New Filename:")
        layout_h1.addWidget(label)

        # QLineEdit 위젯을 생성하고, QHBoxLayout에 추가합니다.
        self.line_edit = QLineEdit()
        layout_h1.addWidget(self.line_edit)

        # QPushButton 위젯을 생성하고, QHBoxLayout에 추가합니다.
        new_button = QPushButton("폴더")
        layout_h1.addWidget(new_button)

        # 새로운 QHBoxLayout을 QVBoxLayout에 추가합니다.
        layout_v.addLayout(layout_h1)

         # QHBoxLayout을 생성합니다.
        layout_h2 = QHBoxLayout()

        # QPushButton 위젯을 생성하고, QHBoxLayout에 추가합니다.
        button = QPushButton('merge PDF')
        layout_h2.addWidget(button)

        # 새로운 QPushButton 위젯을 생성하고, QHBoxLayout에 추가합니다.
        button2 = QPushButton('Clear')
        layout_h2.addWidget(button2)
        
        # QHBoxLayout을 QVBoxLayout에 추가합니다.
        layout_v.addLayout(layout_h2)
        
        # 버튼 클릭 이벤트를 처리할 메서드를 연결합니다.
        new_button.clicked.connect(self.set_output_filename)
        button.clicked.connect(self.merge_pdfs)
        button2.clicked.connect(self.clear_list)        

        self.show()
        
    def set_output_filename(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)")

        if file_name:
            if not file_name.endswith(".pdf"):
                file_name += ".pdf"

            self.line_edit.setText(file_name)
        
    def merge_pdfs(self):
        # listwidget이 비어 있는지 확인하고, 비어 있다면 "파일 없음" 메시지를 출력하고 메서드를 종료합니다.
        if self.listwidget.count() == 0:
            QMessageBox.warning(self, "안내", "통합할 파일이 없습니다.!!!")
            return        
        
        current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        default_output_name = f"merged_output_{current_time}.pdf"
        
        # default_output_name = "merged_output.pdf"
        user_output_name = self.line_edit.text()
        
        # 사용자가 입력한 텍스트가 있으면 해당 이름으로 저장하고, 없으면 기본 이름으로 저장합니다.
        output_path = user_output_name if user_output_name else default_output_name
        pdf_writer = PdfWriter()

        for index in range(self.listwidget.count()):
            input_path = self.listwidget.item(index).text()
            pdf_reader = PdfReader(input_path)

            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)
            
        QMessageBox.information(self, "성공", f"성공했습니다: {output_path}")
        
        
    def clear_list(self):
        self.listwidget.clear()
        self.line_edit.clear()


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
