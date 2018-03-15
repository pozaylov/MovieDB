from PyQt5.QtWidgets import (QWidget, QPushButton, QFileDialog, QApplication, QTextEdit, QGridLayout, QApplication, QLabel, QMessageBox, QLineEdit, QSpacerItem)
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
import sys
from MoviesDatabase import *


class Example(QWidget):
    found_movie = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setStyleSheet("background-color: dimgray;")

        self.add_path = QPushButton('Add Path')
        self.add_path.setStyleSheet("background-color: slategray")

        self.add_path.clicked.connect(self.show_path)

        self.go = QPushButton('GO!')
        self.go.setStyleSheet("background-color: slategray")
        self.go.clicked.connect(lambda: self.gogo(self.excel_p.text()))

        self.textbox = QTextEdit()
        self.textbox.setStyleSheet("background-color: grey")

        self.found_movie.connect(self.textbox.append)

        self.quit = QPushButton('Quit', self)
        self.quit.setStyleSheet("background-color: slategray")
        self.quit.clicked.connect(QCoreApplication.instance().quit)

        self.videofound = QLabel('0 Videos found', self)

        self.text = QLabel('Exccel Path:', self)

        self.excel_p = QLineEdit('', self)
        self.excel_p.setStyleSheet("background-color: gray")

        self.browse = QPushButton('Browse')
        self.browse.clicked.connect(self.browse_excel)
        self.browse.setStyleSheet("background-color: slategray")

        self.rights = QLabel('© Amit Pozner 2018')

        self.space = QLabel('')

        self.open_excel = QPushButton('Open Excel', self)
        self.open_excel.setStyleSheet("background-color: slategray")
        self.open_excel.clicked.connect(lambda: self.open_excel_path(self.excel_p.text()))
        self.open_excel.hide()


        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.add_path, 1, 1, 1, 3)
        grid.addWidget(self.textbox, 2, 1, 1, 2)
        grid.addWidget(self.videofound, 2, 3)
        grid.addWidget(self.text, 3, 1)
        grid.addWidget(self.excel_p, 3, 2)
        grid.addWidget(self.browse, 3, 3)
        grid.addWidget(self.go, 4, 1, 1 ,3)
        grid.addWidget(self.open_excel, 5, 1, 1, 3)
        grid.addWidget(self.quit, 7, 3)
        grid.addWidget(self.space, 6, 1)
        grid.addWidget(self.rights, 7, 1)


        self.setLayout(grid)

        self.setGeometry(300, 300, 550, 300)
        self.setWindowTitle('VideoDB')
        self.show()


    def show_path(self):
        """Fill in textbox with pathes and count video files"""
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select Videos Directory"))
        self.textbox.append(folder_path)  # Update textbox

        paths_list = self.textbox.toPlainText()  # Get text from textbox
        paths_list = paths_list.split('\n')  # split text to list

        self.videofound.setText(self.count_files(paths_list)+ ' Videos found')


    def browse_excel(self):
        excel_path = str(QFileDialog.getExistingDirectory(self, "Select Excel Directory"))
        self.excel_p.setText(excel_path)


    def gogo(self, excel_path):
        """Gather all user paths and call main from MoviesDatabase.py"""
        paths_list = self.textbox.toPlainText()  # Get text from textbox

        if paths_list == '':
            QMessageBox.about(self, "Title", "Please add video paths")
            return
        elif self.excel_p.text() == '':
            QMessageBox.about(self, "Title", "Please select where to save Excel file")
            return

        # excel_path = str(QFileDialog.getExistingDirectory(self, "Select Excel Directory"))
        paths_list = paths_list.split('\n')  # split text to list

        self.movie_worker = MovieWorker(paths_list, excel_path, self.found_movie, parent=self)
        self.movie_worker.start()
        self.movie_worker.finished.connect(lambda: self.textbox.append('\n--- Finished! ---'))
        self.open_excel.show()

    def count_files(self, pathslist):
        """Gets path and return how many videos in it"""
        matches = []
        for l in pathslist:
            for root, dirnames, filenames in os.walk(l):
                for filename in filenames:
                    if filename.endswith(('.mkv', '.mp4', '.avi', '.ts')):
                        matches.append(os.path.join(root, filename))
                for dirname in dirnames:
                    if dirname.endswith('BDMV'):
                        matches.append(os.path.join(root, filename))
            count = str(len(matches))
        return count

    def open_excel_path(self, expath):
        if expath == '':
            QMessageBox.about(self, "Title", "Please add video paths")
        else:
            os.system("open " + expath + os.sep + 'VideoFiles.xls')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


