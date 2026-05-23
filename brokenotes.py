from PyQt5.QtCore import Qt,QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QFileDialog, QScrollArea, QSizePolicy,QDialog, QProgressBar, QTextEdit,
    QGroupBox, QFormLayout, QMessageBox,QFrame)
from PyQt5.QtGui import QColor,QPalette,QPixmap,QFontDatabase,QFont,QIcon
import sys
import os
import json
from webbrowser import open as opensite

developer = "@br0ke.tech"
version = "1.0_BETA"
dir = os.path.dirname(os.path.realpath(__file__))

styleblack = ("QGroupBox { border : none; } QLineEdit { font-size: 20px; border-radius: 8px; padding: 4px; } QPushButton {"
            "background-color: #242424;"
            "color: #ffffff;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}"
        "QPushButton:hover {"
            "background-color: #545454;"
            "color: #ffffff;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}"
        "QLabel {"
            "font-size: 20px;"
            "}"
        "QTextEdit { "
        "border : none; font-size: 10px;"
        "}"
        )

stylewhite = ("QGroupBox { border : none; } QLineEdit { font-size: 20px; border-radius: 8px; padding: 4px; } QPushButton {"
            "background-color: #C3C3C3;"
            "color: #000000;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}"
        "QPushButton:hover {"
            "background-color: #9A9A9A;"
            "color: #000000;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}"
        "QLabel {"
            "font-size: 20px;"
            "}"
        "QTextEdit { "
        "border : none; font-size: 10px;"
        "}"
        )

delbutblack = ("QPushButton {"
            "background-color: #242424;"
            "color: #FF0000;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}"
        "QPushButton:hover {"
            "background-color: #545454;"
            "color: #FF0000;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}")

delbutwhite = ("QPushButton {"
            #"background-color: #C3C3C3"
            "color: #FF0000;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}"
        "QPushButton:hover {"
            "background-color: #9A9A9A;"
            "color: #FF0000;"
            "padding: 5px;"
            "border-radius: 9px;"
            "font-size: 20px;"
            "}")

class UI(QWidget):
    def __init__(self):
        super().__init__()
        with open(os.path.join(dir,"assets","config.json"),"r",encoding="utf-8") as file:
            self.config = json.load(file)
        
        self.fontlist = []
        for i in os.listdir(os.path.join(dir,"assets","fonts")):
            if i.endswith(".ttf"):
                self.fontlist.append(i)

        self.open = "Untitled.txt"
        self.logo = os.path.join(dir,"assets","logo.png")
        self.out = ""

        self.setWindowIcon(QIcon(self.logo))
        self.setWindowOpacity(0.95)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.sizes = ["10","20","30","40","50","60","70","80","90","100"]
        self.logopix = QPixmap(self.logo).scaled(30,30,Qt.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.logol = QLabel()
        self.logol.setPixmap(self.logopix)

        #controls
        self.maing = QGroupBox()
        self.layout.addWidget(self.maing)
        self.main = QVBoxLayout()
        self.maing.setLayout(self.main)
        self.buts = QHBoxLayout()
        self.main.addLayout(self.buts)
        self.titlel = QLabel(f"{os.path.basename(self.open)} ")
        self.setWindowTitle(self.titlel.text()+"- Broke Notes")
        self.buts.addWidget(self.logol)
        self.buts.addWidget(self.titlel)
        self.saveasbut = QPushButton("Save as")
        self.saveasbut.clicked.connect(self.savefileas)
        self.savebut = QPushButton("Save")
        self.savebut.clicked.connect(self.savefile)
        self.loadbut = QPushButton("Load")
        self.loadbut.clicked.connect(self.fileopen)
        self.clearbut = QPushButton("Clear All")
        self.clearbut.clicked.connect(self.cleartext)
        for but in [self.savebut,self.saveasbut,self.loadbut,self.clearbut]: self.buts.addWidget(but)
        self.buts.addStretch()

        #stats
        self.bottoml = QHBoxLayout()
        self.char = QLabel("Characters: 0 Words: 0     ")
        self.bottoml.addWidget(self.char)
        self.bottoml.addStretch()
        self.setbut = QPushButton("Open Settings")
        self.setbut.clicked.connect(self.settings)
        self.bottoml.addWidget(self.setbut)

        self.text = QTextEdit()
        self.text.setAcceptRichText(False)
        self.text.textChanged.connect(self.changetext)
        self.main.addWidget(self.text)
        self.main.addLayout(self.bottoml)

        #Settings
        self.setg = QGroupBox()
        self.setg.hide()
        self.layout.addWidget(self.setg)
        self.setmain = QVBoxLayout()
        
        self.setwidget = QWidget()
        self.setl = QVBoxLayout()
        self.setwidget.setLayout(self.setl)
        self.setscroll = QScrollArea()
        self.setscroll.setWidgetResizable(True)
        self.setscroll.setFrameShape(QFrame.NoFrame)
        self.setscroll.setWidget(self.setwidget)

        self.setmain.addWidget(self.setscroll)
        self.setg.setLayout(self.setmain)
        self.setl.addWidget(QLabel("Settings"),alignment=Qt.AlignHCenter)

        self.setl.addWidget(QLabel("\nDISPLAY"),alignment=Qt.AlignHCenter)
        self.sizel = QHBoxLayout()
        self.setl.addLayout(self.sizel)
        self.sizecombo = QComboBox()
        self.sizecombo.addItems(self.sizes)
        self.sizecombo.currentTextChanged.connect(self.changesize)
        self.sizel.addWidget(QLabel("Change size: "))
        self.sizel.addWidget(self.sizecombo)
        self.sizedesc = QLabel(f"This option allows you to set how big you want your editor's characters. Defaults to 60 on launch.\n")
        self.sizedesc.setWordWrap(True)
        self.setsize(self.sizedesc,15)
        self.setl.addWidget(self.sizedesc)

        self.displayl = QHBoxLayout()
        self.setl.addLayout(self.displayl)
        self.displaycombo = QComboBox()
        self.displaycombo.addItems(["black","white"])
        self.displaycombo.setCurrentText(self.config["mode"])
        self.displaycombo.currentTextChanged.connect(self.changemode)
        self.displayl.addWidget(QLabel("Display mode: "))
        self.displayl.addWidget(self.displaycombo)
        self.displaydesc = QLabel(f"The display mode setting allows you to switch between dark and light themes based on your preference. The dark mode provides a more comfortable viewing experience in low-light environments, while the light mode offers a cleaner look for daytime use.\n")
        self.displaydesc.setWordWrap(True)
        self.setsize(self.displaydesc,15)
        self.setl.addWidget(self.displaydesc)

        self.fontl = QHBoxLayout()
        self.setl.addLayout(self.fontl)
        self.fontcombo = QComboBox()
        self.fontcombo.addItems(self.fontlist)
        self.fontcombo.setCurrentText(self.config["font"])
        self.fontcombo.currentTextChanged.connect(self.changefont)
        self.fontl.addWidget(QLabel("Default font: "))
        self.fontl.addWidget(self.fontcombo)
        self.fontdesc = QLabel(f"With this option you can set what size is used by the UI elements. You can add your own sizes (.ttf) by copying them to /assets/sizes\n")
        self.fontdesc.setWordWrap(True)
        self.setsize(self.fontdesc,15)
        self.setl.addWidget(self.fontdesc)

        self.setl.addStretch()
        self.tiktokbut = QPushButton("My TikTok")
        self.setl.addWidget(self.tiktokbut)
        self.tiktokbut.clicked.connect(lambda:opensite("tiktok.com/@br0ke.tech"))
        self.githubbut = QPushButton("My Github")
        self.setl.addWidget(self.githubbut)
        self.githubbut.clicked.connect(lambda:opensite("github.com/broke-tech"))

        self.versionl = QHBoxLayout()
        self.setl.addLayout(self.versionl)
        self.versionl.addWidget(QLabel(f"with love\nby {developer}"))
        self.versionl.addWidget(QLabel(f"broke notes\nversion {version}",alignment=Qt.AlignRight),alignment=Qt.AlignRight)

        self.setg.setMaximumWidth(self.setg.width()-200)
        self.setscroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        #msg
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Message")
        self.msg.setWindowIcon(QIcon(self.logo))

        #dialog
        self.dialogbox = QDialog()
        self.dialogbox.setWindowIcon(QIcon(self.logo))
        self.butts = QHBoxLayout()
        self.accepted = QPushButton("")
        self.rejected = QPushButton("")
        self.accepted.clicked.connect(lambda: self.stated(True))
        self.rejected.clicked.connect(lambda: self.stated(False))
        self.butts.addStretch()
        self.butts.addWidget(self.accepted)
        self.butts.addWidget(self.rejected)
        self.dlayout = QVBoxLayout()
        self.dmessage = QLabel("")
        self.dlayout.addWidget(self.dmessage)
        self.dlayout.addLayout(self.butts)
        self.dialogbox.setLayout(self.dlayout)

        self.findbox = QGroupBox()
        self.findl = QHBoxLayout()
        self.findl.addStretch()
        self.findbox.setLayout(self.findl)
        self.query = QLineEdit()
        self.query.setPlaceholderText("What are you looking for?")
        self.query.setMaximumWidth(400)
        self.findl.addWidget(self.query)
        self.findbut = QPushButton("Find")
        self.findbut.clicked.connect(self.findtext)
        self.findl.addWidget(self.findbut)
        self.buts.addWidget(self.findbox)

        #styling
        self.appstyle()
        self.sizecombo.setCurrentIndex(5)

    def changesize(self):
        self.text.setStyleSheet(f"border:none;font-size:{self.sizecombo.currentText()}px;")
    
    def changemode(self):
        self.config["mode"] = self.displaycombo.currentText()
        with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
            json.dump(self.config,file)
        self.appstyle()

    def refresh_ui(self): #By chatGPT
        app.processEvents()
        for widget in app.allWidgets():
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

    def changefont(self):
        self.config["font"] = self.fontcombo.currentText()
        with open(os.path.join(dir,"assets","config.json"),"w",encoding="utf-8") as file:
            json.dump(self.config,file)
        self.appstyle()
        
    def changetext(self):
        text = self.text.toPlainText()
        self.char.setText(f"Characters: {len(text)} Words: {len(text.split())}       ")
        if text != self.out:
            self.titlel.setText(f"{os.path.basename(self.open)}* ")
            self.setWindowTitle(self.titlel.text()+"- Broke Notes")
        else:
            self.titlel.setText(f"{os.path.basename(self.open)} ")
            self.setWindowTitle(self.titlel.text()+"- Broke Notes")

    def settings(self):
        if self.setbut.text() == "Open Settings":
            self.setg.show()
            self.setbut.setText("Hide Settings")
        elif self.setbut.text() == "Hide Settings":
            self.setg.hide()
            self.setbut.setText("Open Settings")


    def cleartext(self):
        self.dialog("Are you sure?","Unsaved work will be lost!\nClear all?","yes unc","no")
        if self.yesno:
            self.titlel.setText(f"{os.path.basename(self.open)}* ")
            self.setWindowTitle(self.titlel.text()+"- Broke Notes")
            self.text.setText("")
            
    def stated(self,s):
        self.yesno = s
        self.dialogbox.hide()

    def dialog(self,title,command,yestext,notext):
        self.dialogbox.setWindowTitle(title)
        self.dmessage.setText(command)
        self.accepted.setText(yestext)
        self.rejected.setText(notext)
        self.yesno = False
        self.dialogbox.exec()

    def fileopen(self):
        filework = QFileDialog.getOpenFileName(self,"Select a text file","","All files (*.*)")
        if filework[0] != "":
            try:
                with open(filework[0],"r",encoding="utf-8") as file:
                    self.out = file.read()
                self.text.setText(self.out)
                self.open = filework[0]
                self.titlel.setText(f"{os.path.basename(self.open)} ")
                self.setWindowTitle(self.titlel.text()+"- Broke Notes")
            except:
                self.messagebox("Oops! Seems like Broke Notes couldn't open this file! Please try opening another one")
        
    def filestart(self,fileopen):
        try:
            with open(fileopen,"r",encoding="utf-8") as file:
                self.out = file.read()
            self.text.setText(self.out)
            self.open = fileopen
            self.titlel.setText(f"{os.path.basename(self.open)} ")
            self.setWindowTitle(self.titlel.text()+"- Broke Notes")
        except:
            self.messagebox("Oops! Seems like Broke Notes couldn't open this file! Please try opening another one")
    
    def savefileas(self):
        saveas = QFileDialog.getSaveFileName(self,"Save as...","","Text files (*.txt)","Text files (*.txt)")
        if saveas[0] != "":
            with open(saveas[0],"w",encoding="utf-8") as file:
                file.write(self.text.toPlainText())
            self.out = self.text.toPlainText()
            self.open = saveas[0]
            self.titlel.setText(f"{os.path.basename(self.open)} ")
            self.setWindowTitle(self.titlel.text()+"- Broke Notes")
            self.messagebox("File saved")

    def savefile(self):
        if self.open != "Untitled.txt":
            try:
                with open(self.open,"w",encoding="utf-8") as file:
                    file.write(self.text.toPlainText())
                self.out = self.text.toPlainText()
                self.titlel.setText(f"{os.path.basename(self.open)} ")
                self.setWindowTitle(self.titlel.text()+"- Broke Notes")
                self.messagebox("File saved")
            except:
                self.messagebox("Something went wrong :(")
    
    def findtext(self):
        findings = self.text.toPlainText().split(self.query.text())
        self.messagebox(f'We found "{self.query.text()}" {len(findings)-1} times.')

    def messagebox(self,message):
        self.msg.setText(message)
        self.msg.exec()

    def appstyle(self):
        for i in [self,app,self.msg,self.dialogbox]:
            i.setStyleSheet("")
        if self.config["mode"] == "black":
            self.clearbut.setStyleSheet(delbutblack)
            self.setmodeblack()
            for i in [self,app,self.msg,self.dialogbox]:
                i.setStyleSheet(styleblack)
        elif self.config["mode"] == "white":
            self.clearbut.setStyleSheet(delbutwhite)
            self.setmodewhite()
            for i in [self,app,self.msg,self.dialogbox]:
                i.setStyleSheet(stylewhite)
        self.setfont()

    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
    
    def setfont(self):
        font_path = os.path.join(dir,"assets","fonts",self.config["font"])
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app.setFont(QFont(font_family,11))
        else:
            self.messagebox("Font not found.")
        self.refresh_ui()

    def setmodeblack(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.black)
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, Qt.black)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#242424"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        app.setPalette(palette)

    def setmodewhite(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.white)
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor("#959595"))
        palette.setColor(QPalette.ButtonText, Qt.black)
        app.setPalette(palette)

    def setsize(self,widget,size):
        widget.setStyleSheet(f"font-size: {size}px;")

    def semititle(self,title,layout):
        label = QLabel(title)
        label.setStyleSheet("color: #ffffff; font-size: 30px;")    
        layout.addWidget(QLabel())
        layout.addWidget(label,alignment=Qt.AlignLeft)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = UI()
    ui.show()
    try:
        if os.path.exists(sys.argv[1]):
            ui.filestart(sys.argv[1])
    except:
        pass
    sys.exit(app.exec_())