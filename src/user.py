from files import Files
import sys
from PyQt5.QtWidgets import QMainWindow , QApplication, QLineEdit , QPushButton,  QLabel
from PyQt5 import uic
from mainPage import UI
class USERPAGE(QMainWindow):
    
    def __init__(self):
        super(USERPAGE,self).__init__()
        #load ui file [the path must be relative to the working dir not the py file]
        uic.loadUi("src/UI/login.ui",self)
        #define widgets
        self.header:QLabel=self.findChild(QLabel,"header")
        self.logBtn:QPushButton=self.findChild(QPushButton,"logBtn")
        self.username:QLineEdit=self.findChild(QLineEdit,"username")
        self.password:QLineEdit=self.findChild(QLineEdit,"password")
        self.badData:QLabel=self.findChild(QLabel,"baddata")
        #init state
        self.badData.hide()
        if(not Files.userExists()):
            self.header.setText("SINGUP")
            self.logBtn.setText("Sign Up")
            self.logBtn.clicked.connect(self.__signup)
        else:
            self.logBtn.clicked.connect(self.__signin)
        #show the app
        self.show()
    def __isDataComplete(self):
        username=self.username.text().strip()
        password=self.password.text().strip()
        if(not username or not password):
            self.setStyleSheet('''QLineEdit#username, QLineEdit#password{
                border-style: inset;
                border-width: 2px;
                border-color: red;
                }
            ''')
            self.badData.show()
            return None
        else:
            return (username,password)
    def __signup(self):
        data=self.__isDataComplete()
        if(data != None):
            Files.store_user(*data)
            self.close()
            USERPAGE.openMain()
        return False
    def __signin(self):
        data=self.__isDataComplete()
        if(data != None):
            flag=Files.isUserRight(*data)
            if(flag):
                self.close()
                USERPAGE.openMain()
            else:
                self.badData.show()
                # print("not out")
                return False;
    @staticmethod
    def openMain():
        ui = UI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = USERPAGE()
    sys.exit(app.exec_())