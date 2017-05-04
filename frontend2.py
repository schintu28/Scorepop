"""Scorepop"""
#
# Created by: Vijayalakshmi Narayan S

from PyQt4 import QtCore, QtGui
from bs4 import BeautifulSoup
import requests
import time
import sys, os
import subprocess as SE
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import *
import logging
from config import Config
import pyttsx

file_con = file('data.cfg')       # Opens the config file
cfg = Config(file_con)            # Initializing the config as cfg
URL_info = cfg.URL_rss            # Reads the URL data
Print_one = cfg.print_one         # Prints the data
Print_two = cfg.Page_Header       # Page Header
retry_ini = cfg.Retry_ini         # Settinf initial value
time_period = cfg.POPup_period    # Pop-up Period
Print_three = cfg.Page_Title      # Page Title
image = cfg.Back_grd              # Background Image

logging.basicConfig(datefmt='%a, %d %b %Y %H:%M:%S',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    filename="Log_file.log", level=logging.DEBUG)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Scorepop(object):
    '''Class initializing.'''
    global choice

#######################################################################################################

    def setupUi(self, Scorepop):
        '''Creating a function which would create a pyqt window.'''
        Scorepop.setObjectName(_fromUtf8("Scorepop"))
        Scorepop.setFixedSize(1284, 850)                                 # Size of the PYQT Window
        Scorepop.setMouseTracking(True)                            # Setting mouse tracking function
        Scorepop.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMinMaxButtonsHint)
        self.label = QtGui.QLabel(Scorepop)
        self.label.setGeometry(QtCore.QRect(250, 120, 961, 61))   
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(True)                                       # Font name
        font.setWeight(75)
        self.label.setFont(font)                                   # Setting Font for Header and Title
        self.label.setWordWrap(False)                              
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(Scorepop)
        self.pushButton.setGeometry(QtCore.QRect(1120, 20, 141, 41))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.setStyleSheet("background-color: darkGray")
        self.pushButton.clicked.connect(self.refresh)

        self.exit = QtGui.QPushButton(Scorepop)
        self.exit.setGeometry(QtCore.QRect(20, 20, 141, 41))       # For exit
        self.exit.setObjectName(_fromUtf8("pushButton_2"))
        self.exit.setStyleSheet("background-color: darkGray")
        self.exit.clicked.connect(self.exit_button)

        self.pushButton_2 = QtGui.QPushButton(Scorepop)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 260, 591, 91))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.label_2 = QtGui.QLabel(Scorepop)
        self.label_2.setGeometry(QtCore.QRect(560, 60, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.pushButton_3 = QtGui.QPushButton(Scorepop)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 260, 591, 91))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_3.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.pushButton_4 = QtGui.QPushButton(Scorepop)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 410, 591, 91))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.pushButton_5 = QtGui.QPushButton(Scorepop)
        self.pushButton_5.setGeometry(QtCore.QRect(660, 410, 591, 91))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.pushButton_6 = QtGui.QPushButton(Scorepop)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 560, 591, 91))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.pushButton_7 = QtGui.QPushButton(Scorepop)
        self.pushButton_7.setGeometry(QtCore.QRect(660, 560, 591, 91))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_7.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.pushButton_8 = QtGui.QPushButton(Scorepop)
        self.pushButton_8.setGeometry(QtCore.QRect(20, 700, 591, 91))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_8.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.pushButton_9 = QtGui.QPushButton(Scorepop)
        self.pushButton_9.setGeometry(QtCore.QRect(660, 700, 591, 91))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.pushButton_9.setStyleSheet("background-color: cyan")
        # Creating button along with colour

        self.retranslateUi(Scorepop)
        QtCore.QMetaObject.connectSlotsByName(Scorepop)

###########################################################################################################
   
    def getURLtext(self,url1):
       '''Checking internet connection along with parsing.'''
       retryCount = retry_ini
       r = requests.get(url1)
       while r.status_code is not 200:               # To check whether the status code is 200 or not.
           if retryCount == 0:
               print Print_one                       # Displays system is not connected to internet..
               sys.exit(1)
       data = r.text
       soup = BeautifulSoup(data)
       return soup                                   # Returns the soup value to getscore function

############################################################################################################

    def guinotify(self,message):
        '''Displays Notification.'''
        if os.path.isfile('/etc/lsb-release'):
            SE.Popen(['notify-send', message])       # Used for notifying the score
         

############################################################################################################

    def getscore(self,choice):  
        '''Fetching score'''   
        QtCore.QCoreApplication.processEvents()                                  
        scoreURL = str(allMatches[choice].find_next_sibling().string)
        mainPage = self.getURLtext(scoreURL)
        score = str(mainPage.title.string).split('|')[0]
        inningsreq = mainPage.find("div", {"class" : "innings-requirement"}).string.strip()
        message = score + inningsreq
        self.guinotify(message)   
        engine = pyttsx.init()
        engine.say(inningsreq)
        engine.runAndWait() 

############################################################################################################                             
        
    def clicked_slot1(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(1)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(1)
        

    def clicked_slot2(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(2)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(2)
        

    def clicked_slot3(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(3)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(3)

    def clicked_slot4(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(4)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(4)

    def clicked_slot5(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(5)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(5)

    def clicked_slot6(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(6)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(6)

    def clicked_slot7(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(7)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(7)

    def clicked_slot8(self):
        QtCore.QCoreApplication.processEvents() 
        self.getscore(8)
        while True:
            time.sleep(time_period)                        # To display the notification in a particular time instance
            self.getscore(8)

######################################################################################################### 

    def refresh(self):
        QtCore.QCoreApplication.processEvents()
        self.retranslateUi(Scorepop)

#########################################################################################################


    def retranslateUi(self, Scorepop):
        QtCore.QCoreApplication.processEvents()
        global allMatches,soup
        b = []
        for i in range(0,8):
	    string = 'No Current Matches'
            b.append(string)
                    
        Scorepop.setWindowTitle(_translate("Scorepop", "Scorepop", None))
        self.label.setText(_translate(Print_three, Print_two, None))
        self.exit.setText(_translate("Scorepop", "Exit", None))
        self.pushButton.setText(_translate("Scorepop", "Refresh", None))
        self.label_2.setText(_translate("Scorepop", "SCOREPOP", None))
        
        
        liveMatches = self.getURLtext(URL_info)
        allMatches = liveMatches.find_all('description')
        if len(allMatches) > 1:
            for index, game in enumerate(allMatches[1:9], 1):
                a = '%d.'%index , str(game.string)
                b[index-1] = a
    
        self.pushButton_2.setText(_translate("Scorepop", " ".join(b[0]), None))
        self.pushButton_2.clicked.connect(self.clicked_slot1)
            
        self.pushButton_3.setText(_translate("Scorepop", " ".join(b[1]), None))
        self.pushButton_3.clicked.connect(self.clicked_slot2)
       
        self.pushButton_4.setText(_translate("Scorepop", " ".join(b[2]), None))
        self.pushButton_4.clicked.connect(self.clicked_slot3)

        self.pushButton_5.setText(_translate("Scorepop", " ".join(b[3]), None))
        self.pushButton_5.clicked.connect(self.clicked_slot4)

        self.pushButton_6.setText(_translate("Scorepop", " ".join(b[4]), None))
        self.pushButton_6.clicked.connect(self.clicked_slot5)

        self.pushButton_7.setText(_translate("Scorepop", " ".join(b[5]), None))
        self.pushButton_7.clicked.connect(self.clicked_slot6)

        self.pushButton_8.setText(_translate("Scorepop", " ".join(b[6]), None))
        self.pushButton_8.clicked.connect(self.clicked_slot7)

        self.pushButton_9.setText(_translate("Scorepop", " ".join(b[7]), None))
        self.pushButton_9.clicked.connect(self.clicked_slot8)

#######################################################################################################################

    def exit_button(self):
        QtCore.QCoreApplication.processEvents()
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Scorepop = QtGui.QWidget()
    palette = QtGui.QPalette()
    palette.setBrush(QtGui.QPalette.Background,QBrush(QPixmap(image)))	# TO INSERT BACKGROUND FOR THE SCREEN
    Scorepop.setPalette(palette)
    ui = Ui_Scorepop()
    ui.setupUi(Scorepop)
    Scorepop.show()
    sys.exit(app.exec_())

