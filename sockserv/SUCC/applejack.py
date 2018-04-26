from threading import Thread
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QSystemTrayIcon, \
    QStyle, QWidget, QGridLayout
import sys
from applet import Applet


class Applejack(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)

        self.logWin = QMainWindow()
        self.logWin.setMinimumSize(100, 100)
        self.logWin.setWindowTitle('Sign in IPM')
        self.logWin.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        self.cw = QWidget(self.logWin)
        self.logWin.setCentralWidget(self.cw)

        self.gl = QGridLayout(self.logWin)
        self.cw.setLayout(self.gl)

        self.gl.addWidget(QLabel('Login:', self.logWin), 0, 0)
        self.gl.addWidget(QLabel('Password:', self.logWin), 0, 1)

        self.pe = QLineEdit(self.logWin)
        self.gl.addWidget(self.pe, 1, 1)

        self.le = QLineEdit(self.logWin)
        self.gl.addWidget(self.le, 1, 0)

        self.btn = QPushButton('Log in', self.logWin)
        self.gl.addWidget(self.btn, 2, 0)
        self.btn.clicked.connect(self.on_click_login)

        self.tray = QSystemTrayIcon(self.logWin)
        self.tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        self.logWin.show()
        self.tray.show()

    def output(self, cond, str):
        self.tray.showMessage(cond, str, msecs=5000)

    def on_click_login(self):
        if self.le.text() != '' and self.pe.text() != '':
            self.logWin.hide()
            Applet(login=self.le.text(), password=self.pe.text(), fOUT=self.output).start()


if __name__ == '__main__':
    a = Applejack()
    a.exec()
    a.tray.hide()
    sys.exit(12)
