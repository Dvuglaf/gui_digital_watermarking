import sys
import os
import subprocess
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QVBoxLayout, QWidget, QHBoxLayout, \
    QLabel, QCheckBox, QPushButton, QTextEdit, QProgressBar, QTabWidget
from PyQt5.QtWidgets import QFileDialog


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("CNN Digital Watermarking")
        self.setGeometry(600, 200, 600, 400)  # Первые две координаты смешение окна, последние две-размеры окна.
        self.setFixedSize(600, 450)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.main_lay = QVBoxLayout(self)

        self.panel = ControlPanel()
        self.main_lay.addWidget(self.panel)

        self.tab1.setLayout(self.main_lay)

        # Add tabs
        self.tabs.addTab(self.tab1, "Embedding")
        self.tabs.addTab(self.tab2, "Extracting")

        self.setCentralWidget(self.tabs)
        self.show()


class ControlPanel(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QVBoxLayout(self)

        self.path_coverimage_layout = QHBoxLayout(self)
        self.label_coverimage_path = QLabel('Choose coverimage path', self)
        self.layout.addWidget(self.label_coverimage_path)

        self.search_coverimage_button = QPushButton('...', self)
        self.path_coverimage_field = QTextEdit()
        self.path_coverimage_field.setPlaceholderText("PATH to coverimage")
        self.path_coverimage_field.setReadOnly(True)
        self.path_coverimage_field.setMaximumSize(450, 28)
        self.path_coverimage_field.setMinimumSize(450, 28)
        self.path_coverimage_layout.addWidget(self.path_coverimage_field)
        self.path_coverimage_layout.addWidget(self.search_coverimage_button)
        self.layout.addLayout(self.path_coverimage_layout)
        self.browser1 = WinBrowser()

        self.path_watermark_layout = QHBoxLayout(self)
        self.label_watermark_path = QLabel('Choose watermark path', self)
        self.layout.addWidget(self.label_watermark_path)

        self.search_watermark_button = QPushButton('...', self)
        self.path_watermark_field = QTextEdit()
        self.path_watermark_field.setPlaceholderText("PATH to watermark")
        self.path_watermark_field.setReadOnly(True)
        self.path_watermark_field.setMaximumSize(450, 28)
        self.path_watermark_field.setMinimumSize(450, 28)
        self.path_watermark_layout.addWidget(self.path_watermark_field)
        self.path_watermark_layout.addWidget(self.search_watermark_button)
        self.layout.addLayout(self.path_watermark_layout)
        self.browser2 = WinBrowser()

        self.search_coverimage_button.clicked.connect(self.browser1.search_files)
        self.search_coverimage_button.clicked.connect(self.print_path)

        self.search_watermark_button.clicked.connect(self.browser2.search_files)
        self.search_watermark_button.clicked.connect(self.print_path)

        self.text_label = QLabel('or', self)
        self.layout.addWidget(self.text_label)

        self.string_watermark_layout = QHBoxLayout(self)

        self.string_watermark_field = QTextEdit()
        self.string_watermark_field.setPlaceholderText("Enter a text watermark")
        self.string_watermark_field.setReadOnly(False)
        self.string_watermark_field.setMaximumSize(450, 28)
        self.string_watermark_field.setMinimumSize(450, 28)
        self.layout.addWidget(self.string_watermark_field)
        self.layout.addLayout(self.string_watermark_layout)

        #.void_label = QLabel('\n', self)
        #self.layout.addWidget(self.void_label)

        self.start_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMaximumSize(450, 23)
        self.progress_bar.setMinimumSize(450, 23)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.start_layout.addWidget(self.progress_bar)
        self.start_button = QPushButton('Start', self)
        self.start_layout.addWidget(self.start_button)
        self.layout.addLayout(self.start_layout)

        self.start_button.clicked.connect(self.start)

        self.result_layout = QFormLayout()
        self.result_label_1 = QLabel('...')
        self.result_label_2 = QLabel('...')
        self.result_label_3 = QLabel('...')
        self.result_layout.addRow(QLabel('Metric'), QLabel('Value'))
        self.result_layout.setHorizontalSpacing(50)
        self.result_layout.setVerticalSpacing(20)
        self.result_layout.addRow(QLabel('PSNR : '), self.result_label_1)
        self.result_layout.addRow(QLabel('SSIM : '), self.result_label_2)
        self.result_layout.addRow(QLabel('MSE : '), self.result_label_3)
        self.layout.addSpacing(30)
        self.layout.addLayout(self.result_layout)
        self.layout.addStretch(5)
        self.layout.addSpacing(40)

        self.setLayout(self.layout)

    def print_path(self):
        self.path_field.setText(self.browser.filename)

    def start(self):
        if self.path_watermark_field.toPlainText() == '' and self.string_watermark_field.toPlainText():
            self.path_watermark_field.setPlaceholderText("Please, choose watermark path")
            return
        if self.path_coverimage_field.toPlainText() == '':
            self.path_coverimage_field.setPlaceholderText("Please, choose coverimage path")
            return

        if self.path_watermark_field.toPlainText() == '':  # Watermark as text
            pass
        else:  # Watermark as image
            pass

    def reset_progress_bar(self):
        self.progress_bar.setValue(0)


class WinBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = ''

    def search_files(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\',
                                                'Images (*.jpg)')
        self.filename = file_name[0]


def start_app():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()



