
import sys

from datetime import date
from database import *

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QFormLayout
)

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QMessageBox

#### LOAD MODULES ###
from control import *


if not os.path.exists('check_points'):
    os.mkdir('check_points')

if not os.path.isfile("check_points/last_row.json"):
    saveCheckPoint("check_points/last_row.json", {'last_row':0})

class Worker(QtCore.QObject):# BOT OR OBJECT TO BE MANIPULATE

    descargarSignal = QtCore.pyqtSignal(object)
    solveCaptchaSignal = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._i = 0
        self._stop = False
        self.captcha_flag = False
    # ACTION OR PROCCESS TO MANIPULATE START OR STOP
    def activateFunction(self):
        def incAndEmit():
            self._i, self._stop, self.captcha_flag, self.current_row = processControl(self._i, self._stop, self.selected_file, self.export_file_name, self.captcha_flag)            
            if self.captcha_flag:                
                self._stop = True
                self.solveCaptchaSignal.emit(self)
            else:
                self.descargarSignal.emit(self)
        QtCore.QTimer.singleShot(100, incAndEmit)

class WindowMain(QWidget):

    cargarSignal = QtCore.pyqtSignal() # TO CONNECT WITHO OTHER PROCCESS OR OBJEC
    updateFile = QtCore.pyqtSignal() 
    updateExportFile = QtCore.pyqtSignal() 

    def __init__(self):
        super().__init__()
        # INICIALIZACION DE VENTANA ACTUAL
        self.fecha = date.today().strftime("%d/%m/%Y")        
        self.selected_file = ''
        ############### Creacion de botones y elementos asociacion con funciones #################        
        
        # LAUNCH NAVIGATOR
        self.ButtonLaunchNavigator = QtWidgets.QPushButton('Launch Navigator')
        self.ButtonLaunchNavigator.setFixedSize(150, 25)        
        self.ButtonLaunchNavigator.clicked.connect(self.ExecuteLaunchNavigator)

        self.ButtonQuitNavigator = QtWidgets.QPushButton('Quit')
        self.ButtonQuitNavigator.setFixedSize(150, 25)        
        self.ButtonQuitNavigator.clicked.connect(self.ExecuteQuitNavigator)

        self.ButtonSelectWebSite = QtWidgets.QComboBox()        
        self.ButtonSelectWebSite.setFixedSize(180, 25)
        self.ButtonSelectWebSite.setObjectName("websites")        
        
        self.ButtonSelectWebSite.addItem("Fast People Search")
        self.ButtonSelectWebSite.addItem("All sites -not available-")
        self.ButtonSelectWebSite.addItem("True People Search -not available-")
        self.ButtonSelectWebSite.addItem("Spokeo -not available-")        

        self.ButtonSearchByAddress = QtWidgets.QPushButton('Address')
        self.ButtonSearchByAddress.setFixedSize(150, 25)
        self.ButtonSearchByAddress.setCheckable(True)
        self.ButtonSearchByAddress.clicked.connect(self.ExecuteSearchByAddress)

        self.showDataBase = QtWidgets.QCheckBox("data base")
        self.showDataBase.setCheckState(Qt.CheckState.Checked)
        self.showDataBase.setChecked(True)
        self.showDataBase.stateChanged.connect(self.ExecuteShowDataBase)

        self.showCurrentFile = QtWidgets.QCheckBox("Current file")
        self.showCurrentFile.setCheckState(Qt.CheckState.Checked)
        self.showCurrentFile.stateChanged.connect(self.ExecuteShowCurrentFile)
        self.showCurrentFile.setChecked(False)
        

        self.ButtonSearchByName = QtWidgets.QPushButton('Name')
        self.ButtonSearchByName.setFixedSize(150, 25)
        self.ButtonSearchByName.setCheckable(True)
        self.ButtonSearchByName.clicked.connect(self.ExecuteSearchByName)

        self.ButtonLoadFile = QtWidgets.QPushButton('Load File')
        self.ButtonLoadFile.setFixedSize(150, 25)        
        self.ButtonLoadFile.clicked.connect(self.ExecuteLoadFile)

        self.ButtonExportFile = QtWidgets.QPushButton('Export File')
        self.ButtonExportFile.setFixedSize(150, 25)        
        self.ButtonExportFile.clicked.connect(self.ExecuteExportFile)

        self.rowlabel = QtWidgets.QLabel('Last row')
        self.rowlabel.setFixedSize(250, 25)

        self.textLastRow = QtWidgets.QLineEdit()
        self.textLastRow.setFixedSize(150, 25)
        self.textLastRow.setText('0')
        # self.textLastRow.textChanged.connect(self.ChangetextLastRow)

        self.FileNamelabel = QtWidgets.QLabel('File name')
        self.FileNamelabel.setFixedSize(250, 25)

        self.FileName = QtWidgets.QLineEdit()
        self.FileName.setFixedSize(150, 25)
        # self.FileName.textChanged.connect(self.FileName)

        self.CityStateZiplabel = QtWidgets.QLabel('City State Zip')
        self.CityStateZiplabel.setFixedSize(250, 25)

        self.InputCityStateZip = QtWidgets.QLineEdit()
        self.InputCityStateZip.setFixedSize(150, 25)
        # self.InputCityStateZip.textChanged.connect(self.ChangeInputCityStateZip)

        # STOP MESSAGE RESEND`
        self.ButtonStartPause = QtWidgets.QPushButton('Start')
        self.ButtonStartPause.setFixedSize(150, 25)        
        self.ButtonStartPause.clicked.connect(self.ExecuteStartPause)

        # STOP MESSAGE RESEND
        self.ButtonStop = QtWidgets.QPushButton('Stop')
        self.ButtonStop.setFixedSize(150, 25)
        self.ButtonStop.setCheckable(True)
        self.ButtonStop.clicked.connect(self.ExecuteStop)

        # STOP MESSAGE RESEND
        self.ButtonRestart = QtWidgets.QPushButton('Restart')

        self.ButtonRestart.setFixedSize(150, 25)
        self.ButtonRestart.setCheckable(True)
        self.ButtonRestart.clicked.connect(self.ExecuteRestart)

        # self.selected_file = '*'
        self.dbase = createConection()
        self.Table = UpdateTable(self)

        SetInicio(self)

        ############## SECTION PROCESS CONTROL ###################
        worker = Worker()
        thread = QtCore.QThread()

        self.cargarSignal.connect(worker.activateFunction)  ###     LOAD INFO TO SECOND CLASS ###
        self.updateFile.connect(self.ExecuteUploadFile)
        self.updateExportFile.connect(self.ExecuteUploadExportFile)
        worker.descargarSignal.connect(self.cargarFunct)
        #-updartetable-
        worker.solveCaptchaSignal.connect(self.alertSolveCaptcha)

        Worker.selected_file = self.selected_file
        Worker.export_file_name = ''
        # self.retrieve.connect(worker.onRetrieve)
        # worker.retrieved.connect(self.onRetrieved)
        worker.moveToThread(thread)
        thread.start()

        self._thread = thread # protect from destroying by gc
        self._worker = worker # protect from destroying by gc

        #############################################################
        #                   SETTINGS INITIAL FLAGS                  #
        #############################################################
        self.launchNavigatorFlag = False
        self.loadFileFlag = False
        self.exportFileFlag = False
        self._stop = True


    def ExecuteLaunchNavigator(self):
        Worker.selected_file = self.selected_file        
        #self.loadFileFlag = True
        #self.exportFileFlag = True
        if self.loadFileFlag and self.exportFileFlag:
            try:
                launchNavigator()
                self.launchNavigatorFlag = True
            except:
                QMessageBox.about(self, "Error", "Please close all Chrome windows")
        
        if not self.loadFileFlag and not self.exportFileFlag:
            QMessageBox.about(self, "Error", "Please select an input file and output file path")
        else:
            if not self.loadFileFlag:
                QMessageBox.about(self, "Error", "Please select an input file: ")

            if not self.exportFileFlag:
                QMessageBox.about(self, "Error", "Please select an output file path")

    def ExecuteQuitNavigator(self):        
        if self.launchNavigatorFlag:
            closeDriver()
            self.launchNavigatorFlag = False
        else: 
            QMessageBox.about(self, "Error", 'Please first push button "Launch Naviagtor"')       

    def ExecuteStartPause(self):        
        if self.launchNavigatorFlag:
            flag_block = True
            if self._stop and flag_block:                
                self.ButtonStartPause.setText("Pause") 
                self.ButtonStop.setChecked(False)    
                self._stop = False
                Worker._stop = self._stop
                self.cargarSignal.emit()
                flag_block = False

            if not self._stop and flag_block:                
                self.ButtonStartPause.setText("Start")
                self._stop = True
        else:
            QMessageBox.about(self, "Error", 'Please first push button "Launch Navigator"')

    def ExecuteStop(self): 
        self.ButtonStartPause.setText("Start")
        self.ButtonStop.setChecked(True)
        self._stop = True        
        Worker._stop = self._stop
        closeDriver()

    def ExecuteRestart(self):         
        Worker._i = 0
        self.textLastRow.setText('0')
        self.last_row_dict[self.selected_file.split('/')[-1]] = {'last_row':current_row}
        # saveCheckPoint('check_points/last_row.json', last_row_dict)
        saveCheckPoint('check_points/last_row.json', self.last_row_dict)
        self.updateFile.emit()
        # , FileName
        #  if self.TasaBCV.text()!='':
        #     SetInicio(self)
        #     ButtonActionInicio(self)
        # else:
        #     QMessageBox.about(self, "Error", "Ingrese tasa de cambio valida")

    ###################   FUNTION TO CONNECT ##################
    def cargarFunct(self):        
        #-updartetable-        
        _,self.last_row_dict, self.current_row = search_check_points(self.selected_file, check_point_filename = 'check_points/last_row.json')
        self.textLastRow.setText(str(self.current_row))
        self.Table = UpdateTable(self)
        self.Tablelayout.itemAt(1).widget().setParent(None)
        self.Tablelayout.addWidget(self.Table)    
        # process data
        if self._stop:
            # self._stop = _stop            
            self.ButtonStartPause.setText("Start")
            return
        # self._i = Descargar._i
        else:
            self.cargarSignal.emit()
    
    def alertSolveCaptcha(self):        
        # QMessageBox.about(self, "Please solve Captcha to continue...", "Solved")        
        self.alertWindows = WindowAlertCatpcha()
        self.alertWindows.reactivateSignal.connect(self.continueExtraction)
        self.alertWindows.show()

    def continueExtraction(self):
        self._stop = False
        self.captcha_flag = False
        Worker.captcha_flag = False
        self.alertWindows.close()
        self.cargarSignal.emit()

    def ExecuteSearchByAddress(self):
        self.ButtonSearchByAddress.setChecked(True)
        self.ButtonSearchByName.setChecked(False)

    def ExecuteShowDataBase(self):        
        
        if self.showDataBase.isChecked():
            self.showCurrentFile.setChecked(False)
            self.Table= UpdateTable(self)
            self.Tablelayout.itemAt(1).widget().setParent(None)
            self.Tablelayout.addWidget(self.Table)    

    def ExecuteShowCurrentFile(self):        

        if self.showCurrentFile.isChecked():
            self.showDataBase.setChecked(False)
            self.Table= UpdateTable(self)
            self.Tablelayout.itemAt(1).widget().setParent(None)
            self.Tablelayout.addWidget(self.Table)

    def ExecuteSearchByName(self):
        self.ButtonSearchByName.setChecked(True)
        self.ButtonSearchByAddress.setChecked(False)    

    def ExecuteLoadFile(self):        
        # options = QFileDialog.Options()
        # options |= QFileDialog.ReadOnly
        # file_dialog = QFileDialog()
        # file_dialog.setOptions(options)        
        # self.selected_file, _ = file_dialog.getOpenFileName(self, "Open File", ".csv", "All files (*)")
        self.selected_file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if self.selected_file:
            self.updateFile.emit()
            _,self.last_row_dict, self.current_row = search_check_points(self.selected_file, check_point_filename = 'check_points/last_row.json')
            self.textLastRow.setText(str(self.current_row))
            list_missed_columns = validate_file_colums(self.selected_file)
            if len(list_missed_columns) != 0:                
                self.WindowAlertMissedColumns= WindowAlertMissedColumns()
                self.WindowAlertMissedColumns.missedcolumns = "Missed columns: "+ str(' ,'.join(list_missed_columns))
                print(self.WindowAlertMissedColumns.missedcolumns)
                self.WindowAlertMissedColumns.show()
            else:
                self.loadFileFlag = True

        previous_registers = getPeopleContactByFile(self.dbase, self.selected_file)        
        if len(previous_registers)!=0:        
            self.WindowsSelectCheckPoint= WindowsSelectCheckPoint()
            self.WindowsSelectCheckPoint.last_row = len(previous_registers)
            self.WindowsSelectCheckPoint.setcheckpoint.connect(self.ExecuteSetCheckPoint)
            self.WindowsSelectCheckPoint.show()

    def ExecuteExportFile(self):        
        # options = QFileDialog.Options()
        # folder_dialog = QFileDialog()
        # folder_dialog.setOptions(options)
        # folder_dialog.setFileMode(QFileDialog.Directory)

        # Show the folder dialog and get the selected folder
        # self.export_file_name, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        # self.export_file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt);;Image Files (*.png *.jpg)")
        self.export_file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")

        if self.export_file_name:            
            self.updateExportFile.emit()
            self.exportFileFlag = True

    def ExecuteUploadFile(self):        
        Worker.selected_file = self.selected_file
        self.FileName.setText(self.selected_file.split('/')[-1])
        # Worker._i = 0

    def ExecuteUploadExportFile(self):
        
        Worker.export_file_name = self.export_file_name
        # Worker._i = 0

    def ExecuteSetCheckPoint(self):
        self.textLastRow = str(self.WindowsSelectCheckPoint.last_row)

def UpdateTable(self):    
    if self.showDataBase.isChecked():        
        results = getPeopleContact(self.dbase)

    if self.showCurrentFile.isChecked():        
        results = getPeopleContactByFile(self.dbase, self.selected_file.split('/')[-1])

    nrows = len(results)
    self.Table = TableUser(results, nrows, 3)
    return self.Table

def SetInicio(self):
    #               LAYERS SETTING                      
    #####################################################
    #                                                   #
    #           FirstButtonlayout                       #
    #                                                   #
    #####################################################
    #                    #                              #
    #       SideButton   #      Table                   #
    #                    #                              #
    #                    #                              #
    #                    #                              #
    #                    #                              #
    #####################################################
	# CleanSideButtonTable(self)
	# MAIN LAYOUT VERTICAL#       
    self.Mainlayout = QVBoxLayout()

    # FIRST ROWS OF BUTTONS
    self.FirstButtonlayout = QHBoxLayout()

    # SIDE LAYOUT SETTED TO THE LEFT
    self.SideButton = QVBoxLayout()
    # LAYOUT FOR THE TABLE
    self.Tablelayout = QHBoxLayout()    

    # Add Buttons to Buttons layout    
    self.FirstButtonlayout.addWidget(self.ButtonLaunchNavigator, 0)    
    self.FirstButtonlayout.addWidget(self.ButtonQuitNavigator, 0)
    self.FirstButtonlayout.addWidget(self.ButtonSelectWebSite, 0)
    self.FirstButtonlayout.addWidget(self.ButtonSearchByAddress, 0)
    self.FirstButtonlayout.addWidget(self.ButtonSearchByName, 0)    
    self.FirstButtonlayout.addWidget(self.ButtonLoadFile, 0)    
    self.FirstButtonlayout.addWidget(self.ButtonExportFile, 0)
    # Add table and side buttons to Table layout.
    self.Tablelayout.addLayout(self.SideButton)
    self.Tablelayout.addWidget(self.Table)

    # ADD ELEMENTS TO THE SIDEBUTTON LAYOUT    
    # self.SideButton.addWidget(self.ButtonStart)

    
    self.SideButton.addWidget(self.showCurrentFile)
    self.SideButton.addWidget(self.showDataBase)

    self.SideButton.addWidget(self.rowlabel)
    self.SideButton.addWidget(self.textLastRow)

    self.SideButton.addWidget(self.FileNamelabel)
    self.SideButton.addWidget(self.FileName)
    
    self.SideButton.addWidget(self.CityStateZiplabel)
    self.SideButton.addWidget(self.InputCityStateZip)

    self.SideButton.addWidget(self.ButtonStartPause)
    self.SideButton.addWidget(self.ButtonStop)
    self.SideButton.addWidget(self.ButtonRestart)

    # CREATE AND ADD VERTICAL SPACER TO LAYER SIDEBUTTONS
    self.VerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    # self.VerticalSpacer = QFrame()
    # self.VerticalSpacer.Shape(QFrame.VLine)
    # self.VerticalSpacer.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)    

    self.SideButton.addItem(self.VerticalSpacer)
    # self.SideButton.addWidget(self.VerticalSpacer)

    # ADD OTHERS LAYOUTS TO THE MAIN LAYOUT
    self.Mainlayout.addLayout(self.FirstButtonlayout)
    self.Mainlayout.addLayout(self.Tablelayout)
    self.setLayout(self.Mainlayout)
        
    self.setWindowTitle("Fast People Search")
    # self.setGeometry(100,100, 220, 260)

class TableUser(QTableWidget):
    def __init__(self, results, *args):
        QTableWidget.__init__(self, *args)        
        self.results = results
        self.setData()
        # self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.header = self.horizontalHeader()
        self.header.setStretchLastSection(True)

    def setData(self): 
        
        horHeaders = ['Name','Phone', 'Address']
        self.setColumnWidth(0, 150)
        self.setColumnWidth(1, 180)
        self.setColumnWidth(2, 250)
        
        for n, result in enumerate(self.results):

            for m, item in enumerate(result):

                newitem = QTableWidgetItem(str(item))
                # self.showCurrentFile.setCheckState(Qt.CheckState.Checked)
                # newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                newitem.setFlags(newitem.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                self.setItem( n, m, newitem)

        self.setHorizontalHeaderLabels(horHeaders)

class WindowAlertCatpcha(QWidget):
    reactivateSignal = pyqtSignal()
    def __init__(self):
        super().__init__()      
        self.setWindowTitle("Alert need help solving CAPTCHA...")
        self.setGeometry(150, 150, 260, 180)

        self.ButtonContinue = QtWidgets.QPushButton('Continue')
        self.ButtonContinue.setFixedSize(120, 20)
        self.ButtonContinue.clicked.connect(self.reactivateSearch)

        self.Mainlayout = QHBoxLayout()
        self.Mainlayout.addWidget(self.ButtonContinue)

        self.setLayout(self.Mainlayout) 

    def reactivateSearch(self):        
        time.sleep(0.2)
        self.close() 
        self.reactivateSignal.emit()
 
class WindowsSelectCheckPoint(QWidget):
    setcheckpoint = pyqtSignal()
    def __init__(self):
        super().__init__()      
        self.setWindowTitle("Is there a previous registration related to this file. Do you want to continue from the same point?")
        self.setGeometry(150, 150, 260, 180)

        self.ButtonContinue = QtWidgets.QPushButton('Continue')
        self.ButtonContinue.setFixedSize(120, 20)
        self.ButtonContinue.clicked.connect(self.setContinue)

        self.ButtonRestart = QtWidgets.QPushButton('Restart')
        self.ButtonRestart.setFixedSize(120, 20)
        self.ButtonRestart.clicked.connect(self.setRestart)

        self.Mainlayout = QHBoxLayout()
        self.Mainlayout.addWidget(self.ButtonContinue)
        self.Mainlayout.addWidget(self.ButtonRestart)

        self.setLayout(self.Mainlayout) 

    def setContinue(self):        
        time.sleep(0.2)
        self.close()        
        self.setcheckpoint.emit(self)

    def setRestart(self):        
        time.sleep(0.2)
        self.close()
        self.last_row = 0
        self.setcheckpoint.emit(self)

class WindowAlertMissedColumns(QWidget):
    # reactivateSignal = pyqtSignal()
    def __init__(self):
        super().__init__()      
        self.setWindowTitle("Missed Columns...")
        self.setGeometry(150, 150, 260, 180)

        self.ButtonError = QtWidgets.QPushButton('Check columns names')
        self.ButtonError.setFixedSize(180, 20)
        self.ButtonError.clicked.connect(self.CloseWindows)

        # self.MissedColumns = QtWidgets.QTextEdit()        
        # self.MissedColumns.setFixedSize(350, 100)
        # self.MissedColumns.setText(missedcolumns)


        self.Mainlayout = QVBoxLayout()
        self.Mainlayout.addWidget(self.ButtonError)
        # self.Mainlayout.addWidget(self.MissedColumns)
        

        self.setLayout(self.Mainlayout) 

    def CloseWindows(self):        
        time.sleep(0.2)
        self.close()        

if __name__ == "__main__":	
    app = QApplication(sys.argv)
    window = WindowMain()
    # window.setCentralWidget (frm)
    # window.resize(340, 440)
    window.show()
    # sys.exit(app.exec_())    
    app.exec()
    closeConection(dbase)
    driver.close()
