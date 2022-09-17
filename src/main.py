from user import USERPAGE
from sys import exit , argv
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(argv)
    ui = USERPAGE()
    ui2=USERPAGE()
    exit(app.exec_())
