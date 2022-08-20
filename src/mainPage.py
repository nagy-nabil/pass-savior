from sre_compile import isstring
from PyQt5.QtWidgets import QMainWindow , QApplication, QLineEdit , QPushButton, QRadioButton, QScrollArea, QLabel,QWidget,QGridLayout,QFormLayout,QDialog,QWidgetItem,QAction
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5 import uic
from PyQt5.QtCore import QSize
from files import Files
import webbrowser
class UI(QMainWindow):
    
    def __init__(self):
        super(UI,self).__init__()
        self.__data={}
        self.__dataWidgets={}        
        #load ui file [the path must be relative to the working dir not the py file]
        uic.loadUi("src/UI/main.ui",self)
        #define widgets
        # self.logo=self.findChild(QLabel,"logo")
        self.search=self.findChild(QLineEdit,"search")
        self.saved=self.findChild(QScrollArea,"saved")
        self.editBtn=self.findChild(QPushButton,"editBtn")
        self.searchBtn=self.findChild(QPushButton,"searchBtn")
        self.savedData=self.findChild(QWidget,"savedData")
        self.savedGrid=self.findChild(QGridLayout,"savedGrid")
        self.app_name=self.findChild(QLabel,"app_name")
        self.values=self.findChild(QScrollArea,"values")
        self.values_form=self.findChild(QFormLayout,"values_form")
        self.deleteBtn=self.findChild(QPushButton,"deleteBtn")
        # self.mainPageGIF=self.findChild(QLabel,"mainPageGIF")
        self.actionAddApp=self.findChild(QAction,"actionAddApp")
        self.actionHome=self.findChild(QAction,"actionHome")
        self.actionCLOSE=self.findChild(QAction,"actionCLOSE")
        self.actionAbout=self.findChild(QAction,"actionAbout")
        # self.save=self.findChild(QPushButton,"save")
        # self.add_field=self.findChild(QPushButton,"add_field")
        self.editBtn.clicked.connect(lambda :self.editLogic())
        self.searchBtn.clicked.connect(lambda:self.__searchLogic())
        self.deleteBtn.clicked.connect(self.__deleteLogic)
        self.searchBtn.setShortcut(QKeySequence('Return'))
        self.actionAddApp.triggered.connect(self.createApp)
        self.actionHome.triggered.connect(self.__MainPageSetup)
        self.actionCLOSE.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.open_link)
        # self.search.setFocus(True)
        # self.save.clicked.connect(lambda:self.__saveData())
        # self.add_field.clicked.connect(self.new_field)
        self.setupUI()
        # for i in range(10):
        #     self.create_check_gui("kj")
        # #init
        # self.logo_image=QPixmap("Hnet.com-image.png")
        # self.logo.setPixmap(self.logo_image)
        #show the app
        self.show()
    def addApp(self,name):
        name=name.title()
        # print(self.savedGrid.rowCount())
        self.newApp=QRadioButton(self.savedData)
        self.newApp.setStyleSheet('''QRadioButton::indicator {width: 0px;height: 0px;}
        ''')
        self.newApp.setText(f"{name}")
        self.newApp.clicked.connect(lambda: self.addData(name.lower()))
        self.savedGrid.addWidget(self.newApp,self.savedGrid.rowCount(),0,1,2)
        if(name in "Facebook" ):
            self.icon=QIcon("src/icons/facebook-logo.png")
        elif(name in 'Twitter' ):
            self.icon=QIcon("src/icons/twitter-logo.png")
        elif(name in 'Gmail' or name in "Google"):
            self.icon=QIcon("src/icons/Gmail_icon.png")
        elif(name in "Riot Games" or name in "Valorant" or name == "Lol" or name =="League Of Leagends"):
            self.icon=QIcon("src/icons/Riot-Games-logo.png")
        else:
            self.icon=QIcon("src/icons/locked.ico")
        self.newApp.setIcon(self.icon)
        self.newApp.setIconSize(QSize(50,50))
    
    def createApp(self):
        self.newAppName=QLineEdit(self.savedData)
        self.newAppName.setObjectName("newAppName")
        self.newAppName.setFrame(False)
        self.newAppName.setFocus(True)
        self.newAppName.setPlaceholderText("type new app name")
        self.saveIcon=QPushButton(self.values)
        self.saveIcon.setObjectName("saveIcon")
        self.saveIcon.setFlat(True)
        self.icon=QIcon("src/icons/add.png")
        self.saveIcon.setIcon(self.icon)
        self.saveIcon.setIconSize(QSize(50,50))
        self.savedGrid.addWidget(self.newAppName,self.savedGrid.rowCount(),0,1,1)
        self.savedGrid.addWidget(self.saveIcon,self.savedGrid.rowCount()-1,1,1,1)
        self.saveIcon.clicked.connect(self.saveNewApp)
        self.createAppLogic()

    def createAppLogic(self):
        self.__clearForm()
        self.app_name.setText("NEW APP")
        self.editBtn.setEnabled(False)
        self.deleteBtn.setEnabled(False)
        # self.editLogic()
        # self.add_field()
    def saveNewApp(self):
        if(self.newAppName.text().strip()):
            self.__data[self.newAppName.text().strip().lower()]={}
            self.addApp(self.newAppName.text().strip())
            self.app_name.setText(self.newAppName.text().strip().title())
            self.newAppName.deleteLater()
            self.saveIcon.deleteLater()
            self.editLogic()
            self.__new_field()
    def __clearForm(self):
        count=self.values_form.rowCount()
        for i in range(0,count):
            self.values_form.removeRow(0)
        self.__dataWidgets.clear()
    #take dict and create field value ui pair of it
    def addData(self,appName):
        # self.deleteBtn.clicked.connect(lambda:self.__deleteFromSavedUI(row))
        # print(self.__data[appName])
        self.app_name.setText(appName.title())
        self.__clearForm()
        self.deleteBtn.setEnabled(True)
        self.editBtn.setEnabled(True)
        self.__dataWidgets.clear()
        for (k,v) in self.__data[appName].items():
            self.field=QLabel(self.values)
            self.field.setObjectName("field")
            self.field.setText(f"{k}")
            self.values_form.addWidget(self.field)
            self.value=QLineEdit(self.values)
            self.value.setObjectName("value")
            self.value.setText(f"{v}")
            self.value.setReadOnly(True)
            # self.value.setClearButtonEnabled(True)
            self.value.setFrame(False)
            self.values_form.addRow(self.field,self.value)
            self.__dataWidgets[k]=self.value
        # print(self.__dataWidgets)
    
    def __MainPageSetup(self):
        self.app_name.setText("HEY BOSS.")
        self.__clearForm()
        self.deleteBtn.setEnabled(False)
        self.editBtn.setEnabled(False)
        # self.GIF=QMovie("icons/better-call-saul-loop.gif")
        # self.GIF.setObjectName("GIF")
        # # self.GIF.setScaledSize(QSize(self.values.width(),self.values.height()))
        # # self.GIF.setSize(self.)
        # self.mainPageGIF.setMovie(self.GIF)
        # self.GIF.start()
    #load the data when the app start and add the data to the ui
    def setupUI(self):
        self.__MainPageSetup()
        self.__clearSaved()
        self.__data=Files.load()#dict
        # print(self.__data)
        if(self.__data):
            for itm in self.__data:
                self.addApp(itm)
    # pos=2
    def __clearSaved(self):
        # print(self.savedGrid.getItemPosition(1))
        # print(self.savedGrid.rowCount())
        # rows=self.savedGrid.rowCount()-1
        # for i in range(rows,0,-1):
        #     self.__deleteFromSavedUI(i)
        # print(self.savedGrid.rowCount())
        # pos=self.savedGrid.getItemPosition(0)[0]
        rCount=self.savedGrid.rowCount()
        # widget=self.savedGrid.itemAtPosition(0,0)
        # while(isinstance(widget,QWidgetItem)):
        #     widget=widget.widget()
        #     widget.deleteLater()
        #     pos+=1
        #     widget=self.savedGrid.itemAtPosition(pos,0)
        for i in range(0,rCount):
            widget=self.savedGrid.itemAtPosition(i,0)
            if(isinstance(widget,QWidgetItem)):
                widget=widget.widget()
                widget.deleteLater()


    def editLogic(self):
        self.editBtn.setEnabled(False)
        for itm in self.__dataWidgets.values():
            itm.setClearButtonEnabled(True)
            itm.setReadOnly(False)
        #create save and  add field buttons
        self.save=QPushButton(self.values)
        self.save.setObjectName("save")
        self.icon=QIcon("src/icons/save.png")
        self.save.setIcon(self.icon)
        self.save.setIconSize(QSize(50,50))
        self.add_field=QPushButton(self.values)
        self.add_field.setObjectName("add_field")
        self.icon=QIcon("src/icons/add.png")
        self.add_field.setIcon(self.icon)
        self.add_field.setIconSize(QSize(50,50))
        self.save.setShortcut(QKeySequence('Ctrl+s'))
        self.add_field.setShortcut(QKeySequence('Ctrl+a'))
        self.save.clicked.connect(self.__saveData)
        self.add_field.clicked.connect(self.__new_field)
        self.values_form.addRow(self.save, self.add_field)
    def __new_field(self):
        self.fld=QLineEdit(self.values)
        self.fld.setObjectName("field")
        self.fld.setFrame(False)
        self.vlu=QLineEdit(self.values)
        self.vlu.setObjectName("value")
        self.vlu.setFrame(False)
        # self.vlu.setStyleSheet("QLineEdit{border-bottom: 6px solid red;}")
        # self.values_form.insertRow(self.values_form.rowCount(),self.fld)
        # self.values_form.insertRow(self.values_form.rowCount(),self.vlu)
        
        #add those new fields to the same dict but the key will be lineEdit and that will be our condition to how to get the data from the dict
        self.__dataWidgets[self.fld]=self.vlu
        self.values_form.insertRow(self.values_form.rowCount()-1,self.fld,self.vlu)
        # print(self.__dataWidgets)
    def __saveData(self):
        appName=self.app_name.text().lower()
        for k,v in self.__dataWidgets.items():
            if(isstring(k)):
                self.__data[appName][k]=v.text().strip()
            else:
                if(k.text().strip() and v.text().strip()):
                    self.__data[appName][k.text().strip()]=v.text().strip()
        # print(self.__data)
        Files.store(self.__data)
        self.editBtn.setEnabled(True)
        #just for the ui 
        self.addData(appName)
    
    def __deleteFromSavedUI(self,row):
        # print(self.savedGrid.itemAtPosition(2,0).widget())
        self.savedGrid.itemAtPosition(row,0).widget().deleteLater()
    def __deleteLogic(self):
        # print(self.app_name.lower())
        del self.__data[self.app_name.text().lower()]
        Files.store(self.__data)
        self.setupUI()
    
    def __searchLogic(self):
        text=self.search.text().strip().lower()
        # print(text)
        if text:
            if(self.__data and text in self.__data):
                self.addData(text)
            else:
                self.__MainPageSetup()
                self.app_name.setText('NOT FOUND.')
                # self.values_form.addWidget(QLabel(self.values,text="NOT FOUND!"))
    @staticmethod
    def open_link():
        url=r"https://github.com/nagy-nabil/pass-savior"
        webbrowser.open(url)
if __name__ == "__main__":    
    import sys
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())