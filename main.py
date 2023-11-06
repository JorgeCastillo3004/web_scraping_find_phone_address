
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
        self.search_by_name = True
        self.current_row = 0
    # ACTION OR PROCCESS TO MANIPULATE START OR STOP
    def activateFunction(self):
        def incAndEmit():
            self._i, self._stop, self.captcha_flag, self.current_row = processControl(self._i, self.dict_parameter)
            if self.captcha_flag:                
                self._stop = True
                self.solveCaptchaSignal.emit(self)
            else:
                self.descargarSignal.emit(self)
        QtCore.QTimer.singleShot(100, incAndEmit)

class WindowMain(QWidget):

    cargarSignal = QtCore.pyqtSignal() # TO CONNECT WITHO OTHER PROCCESS OR OBJEC
    updateFile = QtCore.pyqtSignal() 
    # updateExportFile = QtCore.pyqtSignal() 

    def __init__(self):
        super().__init__()
        # INICIALIZACION DE VENTANA ACTUAL
        self.fecha = date.today().strftime("%d/%m/%Y")        
        ############### Creacion de botones y elementos asociacion con funciones #################        
        
        # LAUNCH NAVIGATOR
        self.ButtonLaunchNavigator = QtWidgets.QPushButton('Launch Navigator')
        self.ButtonLaunchNavigator.setFixedSize(120, 25)        
        self.ButtonLaunchNavigator.clicked.connect(self.ExecuteLaunchNavigator)

        self.ButtonQuitNavigator = QtWidgets.QPushButton('Quit')
        self.ButtonQuitNavigator.setFixedSize(80, 25)        
        self.ButtonQuitNavigator.clicked.connect(self.ExecuteQuitNavigator)

        # self.ButtonSelectWebSite = QtWidgets.QComboBox()        
        # self.ButtonSelectWebSite.setFixedSize(180, 25)
        # self.ButtonSelectWebSite.setObjectName("websites")        
        
        # self.ButtonSelectWebSite.addItem("Fast People Search")
        # self.ButtonSelectWebSite.addItem("All sites -not available-")
        # self.ButtonSelectWebSite.addItem("True People Search -not available-")
        # self.ButtonSelectWebSite.addItem("Spokeo -not available-")        

        self.ButtonSearchByAddress = QtWidgets.QPushButton('Address')
        self.ButtonSearchByAddress.setFixedSize(80, 25)
        self.ButtonSearchByAddress.setCheckable(True)
        self.ButtonSearchByAddress.clicked.connect(self.ExecuteSearchByAddress)

        self.showDataBase = QtWidgets.QCheckBox("data base")
        self.showDataBase.setCheckState(Qt.CheckState.Checked)
        self.showDataBase.setChecked(False)
        self.showDataBase.stateChanged.connect(self.ExecuteShowDataBase)

        self.showCurrentFile = QtWidgets.QCheckBox("Current file")
        self.showCurrentFile.setCheckState(Qt.CheckState.Checked)
        self.showCurrentFile.stateChanged.connect(self.ExecuteShowCurrentFile)
        self.showCurrentFile.setChecked(True)
        

        self.ButtonSearchByName = QtWidgets.QPushButton('Name')
        self.ButtonSearchByName.setFixedSize(80, 25)
        self.ButtonSearchByName.setCheckable(True)
        self.ButtonSearchByName.setChecked(True)
        self.ButtonSearchByName.clicked.connect(self.ExecuteSearchByName)

        self.ButtonLoadFile = QtWidgets.QPushButton('Load File')
        self.ButtonLoadFile.setFixedSize(80, 25)        
        self.ButtonLoadFile.clicked.connect(self.ExecuteLoadFile)

        # self.ButtonExportFile = QtWidgets.QPushButton('Export File')
        # self.ButtonExportFile.setFixedSize(80, 25)        
        # self.ButtonExportFile.clicked.connect(self.ExecuteExportFile)

        self.ButtonFilterResults = QtWidgets.QPushButton('Filter')
        self.ButtonFilterResults.setFixedSize(80, 25)        
        self.ButtonFilterResults.clicked.connect(self.ExecuteFilterResults)

        self.rowlabel = QtWidgets.QLabel('Last row')
        self.rowlabel.setFixedSize(220, 25)

        self.textLastRow = QtWidgets.QLineEdit()
        self.textLastRow.setFixedSize(120, 25)
        self.textLastRow.setText('0')
        # self.textLastRow.textChanged.connect(self.ChangetextLastRow)

        self.FileNamelabel = QtWidgets.QLabel('File name')
        self.FileNamelabel.setFixedSize(220, 25)

        self.FileName = QtWidgets.QLineEdit()
        self.FileName.setFixedSize(120, 25)
        # self.FileName.textChanged.connect(self.FileName)

        # self.CityStateZiplabel = QtWidgets.QLabel('City State Zip')
        # self.CityStateZiplabel.setFixedSize(250, 25)

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

        #############################################################
        #                   SETTINGS INITIAL FLAGS                  #
        #############################################################
        self.launchNavigatorFlag = False
        self.loadFileFlag = False
        # self.exportFileFlag = False
        self._stop = True        
        self.dbase = createConection()
        self.dict_parameter = {'dbase':self.dbase}
        self.dict_parameter['search_by_name'] = True
        self.dict_parameter['selected_file'] = 'not selected file'
        
        self.Table = UpdateTable(self)

        SetInicio(self)

        ############## SECTION PROCESS CONTROL ###################
        self.worker = Worker()
        thread = QtCore.QThread()

        self.cargarSignal.connect(self.worker.activateFunction)  ###     LOAD INFO TO SECOND CLASS ###
        self.updateFile.connect(self.ExecuteUploadFile)
        # self.updateExportFile.connect(self.ExecuteUploadExportFile)
        self.worker.descargarSignal.connect(self.cargarFunct)
        #-updartetable-
        self.worker.solveCaptchaSignal.connect(self.alertSolveCaptcha)

        # Worker.selected_file = self.selected_file
        # Worker.export_file_name = ''
        # self.retrieve.connect(worker.onRetrieve)
        # worker.retrieved.connect(self.onRetrieved)
        self.worker.moveToThread(thread)
        thread.start()

        self._thread = thread # protect from destroying by gc
        self._worker = self.worker # protect from destroying by gc

    # Files selection 
    def ExecuteLoadFile(self):
        selected_file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        self.dict_parameter['selected_file'] = selected_file
        if selected_file!='':
            self.loadFileFlag = True
            self.updateFile.emit()            
            self.previous_registers = getPreviousRegisters_all(self.dbase, selected_file.split('/')[-1])
            columns = show_columns(self.dbase)
            self.previous_registers = pd.DataFrame(self.previous_registers, columns = columns)            

            print("Inside load input file:", selected_file.split('/')[-1],"#")
            print("len self.previous_registers: ", len(self.previous_registers))
            
            # list_missed_columns = validate_file_colums(selected_file, self.dict_parameter['search_by_name'])
            # if len(list_missed_columns) != 0:                
            self.WindowSelecColumnsNames = WindowSelecColumnsNames(selected_file)
            self.WindowSelecColumnsNames.signal_launch_previous_point.connect(self.ExecuteOpenWindowsCheckPoint)
            self.WindowSelecColumnsNames.show()
        else:
            self.loadFileFlag = False

    # def ExecuteExportFile(self):
    #     export_file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
    #     self.dict_parameter['export_file_name'] = export_file_name
    #     if export_file_name:
    #         self.exportFileFlag = True
    #         print("Path to export selected: ")
    
    def ExecuteLaunchNavigator(self):
        # Worker.selected_file = self.selected_file
        #self.loadFileFlag = True
        #self.exportFileFlag = True        
        if self.loadFileFlag:
            try:
                launchNavigator(load_profile = False, search_by_name = self.dict_parameter['search_by_name'])
                self.launchNavigatorFlag = True
            except:
                QMessageBox.about(self, "Error", "Please close all Chrome windows")
        
        if not self.loadFileFlag: #and not self.exportFileFlag:
            QMessageBox.about(self, "Error", "Please select an input file and output file path")
        else:
            if not self.loadFileFlag:
                QMessageBox.about(self, "Error", "Please select an input file: ")

            # if not self.exportFileFlag:
            #     QMessageBox.about(self, "Error", "Please select an output file path")

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
                # Worker._stop = self._stop
                # Worker._stop = self.search_by_name
                self.worker.dict_parameter = self.dict_parameter                
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
        # closeDriver()

    def ExecuteRestart(self):         
        Worker._i = 0
        self.textLastRow.setText('0')
        self.last_row_dict[self.selected_file.split('/')[-1]] = {'last_row':0}        
        saveCheckPoint('check_points/last_row.json', self.last_row_dict)
        self.updateFile.emit()

    ###################   FUNTION TO CONNECT ##################
    def cargarFunct(self):        
        #-updartetable-        
        # _,self.last_row_dict, self.current_row = search_check_points(self.selected_file, check_point_filename = 'check_points/last_row.json')
        
        self.textLastRow.setText(str(self.worker.current_row))
        self.Table = UpdateTable(self)
        self.Tablelayout.itemAt(1).widget().setParent(None)
        self.Tablelayout.addWidget(self.Table)
        # check stop update
        if self.worker._stop:
            self._stop = self.worker._stop
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
        self.dict_parameter['search_by_name'] = True
        # self.loadFileFlag = False

    def ExecuteSearchByAddress(self):
        self.ButtonSearchByAddress.setChecked(True)
        self.ButtonSearchByName.setChecked(False)
        self.dict_parameter['search_by_name'] = False
        # self.loadFileFlag = False

    def ExecuteFilterResults(self):
        print("Open windos filter results: ")
        self.WindowsFilterResults = WindowsFilterResults(self.dbase, self.dict_parameter['search_by_name'], self.dict_parameter['selected_file'])
        # self.WindowsFilterResults.selected_file = self.dict_parameter['selected_file'].split('/')[-1]        
        # self.WindowsFilterResults.dbase = self.dbase
        # self.WindowsFilterResults.flag_init = True
        self.WindowsFilterResults.show()

    def ExecuteUploadFile(self):
        self.FileName.setText(self.dict_parameter['selected_file'].split('/')[-1])

    def ExecuteOpenWindowsCheckPoint(self):
        if len(self.previous_registers)!= 0:
            self.WindowsSelectCheckPoint = WindowsSelectCheckPoint(self.previous_registers, self.dict_parameter['selected_file'].split('/')[-1], self.dbase)
            self.WindowsSelectCheckPoint.setcheckpoint.connect(self.ExecuteSetCheckPoint)
            self.WindowsSelectCheckPoint.show()
        else:                    
            self.dict_parameter['previous_registers'] = self.previous_registers
            self.dict_parameter['last_row'] = 0
            self.textLastRow.setText(str(0))

    def ExecuteSetCheckPoint(self):        
        self.dict_parameter['previous_registers'] = self.WindowsSelectCheckPoint.previous_registers
        self.dict_parameter['last_row'] = getLastRow(self.dbase, self.dict_parameter['selected_file'].split('/')[-1])
        self.textLastRow.setText(str(self.dict_parameter['last_row']))

def UpdateTable(self):    
    if self.showDataBase.isChecked():        
        results = getPeopleContact(self.dbase)

    if self.showCurrentFile.isChecked():
        results = getPreviousRegisters(self.dbase, self.dict_parameter['selected_file'].split('/')[-1])
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
    # self.FirstButtonlayout.addWidget(self.ButtonSelectWebSite, 0)
    self.FirstButtonlayout.addWidget(self.ButtonSearchByAddress, 0)
    self.FirstButtonlayout.addWidget(self.ButtonSearchByName, 0)    
    self.FirstButtonlayout.addWidget(self.ButtonLoadFile, 0)    
    # self.FirstButtonlayout.addWidget(self.ButtonExportFile, 0)
    self.FirstButtonlayout.addWidget(self.ButtonFilterResults, 0)
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
    
    # self.SideButton.addWidget(self.CityStateZiplabel)
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

class TableColumns(QTableWidget):
    def __init__(self, dict_columns_names,*args):
        QTableWidget.__init__(self, *args)
        self.dict_columns_names = dict_columns_names
        self.setData()        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.header = self.horizontalHeader()
        self.header.setStretchLastSection(True)

    def setData(self):         
        horHeaders = ['Name','Address', 'City & State & Zip']
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 300)
        self.setColumnWidth(2, 300)
        # 'name','address', 'city_state_zip'
        self.set_columns_values('name', 0)
        self.set_columns_values('address', 1)
        self.set_columns_values('city_state_zip', 2)
        # try:
        #     for m, column_name in enumerate(dict_columns_names['name']):
        #         newitem = QTableWidgetItem(str(item))
        #         self.setItem( 0, m, newitem)
        # except:
        #     continue

        # for n, result in enumerate(self.results):            

        #     for m, item in enumerate(result):
        #         newitem = QTableWidgetItem(str(item))
        #         self.setItem( n, m, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

    def get_localization(self):        
        self.actcell = self.item(self.currentRow(), self.currentColumn()).text()
        print("Current cell value: ", self.actcell)
        # Columns Names
        # if self.item(self.currentRow(), 3) is not None:
        #     self.NumbFactDetalles = self.item(self.currentRow(), 3).text()
        # else:
        #     self.NumbFactDetalles = ''
    def set_columns_values(self, key, column_number):
        try:
            for m, column_name in enumerate(self.dict_columns_names[key]):
                newitem = QTableWidgetItem(str(column_name))
                self.setItem(m, column_number, newitem)
        except:
            pass

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

    def __init__(self, previous_registers, selected_file, dbase):
        self.previous_registers = previous_registers
        self.selected_file = selected_file
        self.dbase = dbase
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
        print("Continue")
        time.sleep(0.2)
        self.close()        
        self.setcheckpoint.emit()

    def setRestart(self):
        print("Restar")
        print("file name: ", self.selected_file, "#")        
        time.sleep(0.2)
        self.close()
        deletePreviosRegister(self.dbase, self.selected_file)
        print("Previous registers related from file {} was deleted ".format(self.selected_file))
        self.previous_registers = pd.DataFrame()
        self.setcheckpoint.emit()

class WindowsFilterResults(QWidget):
    signal_make_filter = pyqtSignal()
    def __init__(self, dbase, search_by_name, selected_file):
        super().__init__()
        self.search_by_name = search_by_name
        self.dbase = dbase
        self.selected_file = selected_file
        self.setWindowTitle("Filter results")
        self.setGeometry(150, 150, 260, 180)        

        # self.ButtonFilter = QtWidgets.QPushButton('Filter')
        # self.ButtonFilter.setFixedSize(120, 20)
        # self.ButtonFilter.clicked.connect(self.Executemakefilter)

        self.ButtonExport = QtWidgets.QPushButton('Export File')
        self.ButtonExport.setFixedSize(120, 20)
        self.ButtonExport.clicked.connect(self.ExecuteExportFile)

        self.Mainlayout = QVBoxLayout()
        self.layout = QVBoxLayout()

        self.last_name_checkbox = QCheckBox("Contains Last Name")
        self.last_name_checkbox.setCheckState(Qt.CheckState.Checked)
        self.last_name_checkbox.setChecked(True)        
        # self.df = pd.DataFrame(getAllInfoPeopleContact(self.dbase))

        self.address_check = QCheckBox("Address")
        self.address_check.setCheckState(Qt.CheckState.Checked)
        self.address_check.setChecked(True)

        self.city_checkbox = QCheckBox("City")
        self.city_checkbox.setCheckState(Qt.CheckState.Checked)
        self.city_checkbox.setChecked(True)
        # self.city_checkbox.stateChanged.connect(self.FilterCity)
        
        self.state_checkbox = QCheckBox("State")
        self.state_checkbox.setCheckState(Qt.CheckState.Checked)
        self.state_checkbox.setChecked(True)
        # self.state_checkbox.stateChanged.connect(self.FilterState)

        self.zip_checkbox = QCheckBox("Zip")
        self.zip_checkbox.setCheckState(Qt.CheckState.Checked)
        self.zip_checkbox.setChecked(True)

        self.layout.addWidget(self.last_name_checkbox)
        self.layout.addWidget(self.address_check)
        self.layout.addWidget(self.city_checkbox)
        self.layout.addWidget(self.state_checkbox)
        self.layout.addWidget(self.zip_checkbox)
        
        # self.layout.addWidget(self.ButtonFilter)
        self.layout.addWidget(self.ButtonExport)
        self.setLayout(self.layout)
        
        # self.Mainlayout.addWidget(self.ButtonFilter)
        # self.Mainlayout.addWidget(self.ButtonExport)
        # signal make filter connection
        self.signal_make_filter.connect(self.ExecuteFilterSignal)

    def FileSelected(self):
        if self.current_file_checkbox.isChecked():
            self.database_checkbox.setChecked(False)
            self.current_file_checkbox.setChecked(True)
        else:
            self.database_checkbox.setChecked(True)
            self.current_file_checkbox.setChecked(False)

    def DateBaseSelected(self):
        if self.database_checkbox.isChecked():
            self.current_file_checkbox.setChecked(False)
            self.database_checkbox.setChecked(True)
        else:
            self.current_file_checkbox.setChecked(True)
            self.database_checkbox.setChecked(False)

    # def Executemakefilter(self):
    #     self.signal_make_filter.emit()

    def ExecuteFilterSignal(self):
        print("Make filter")
        
        columns = show_columns(self.dbase)        
        data = getAllInfoPeopleContact(self.dbase)
        df_data_base = pd.DataFrame(data, columns = columns)

        df_file = pd.read_csv(self.selected_file)       
        
        # Flag selected city
        cond1_e = self.address_check.isChecked()
        cond2_2 = self.last_name_checkbox.isChecked()
        cond2_3 = self.city_checkbox.isChecked()
        cond2_4 = self.state_checkbox.isChecked()
        cond2_5 = self.zip_checkbox.isChecked()
    
        # Make filtered
        # self.df_filtered = self.df[self.cond1 & self.cond2 & self.cond3 & self.cond4]
        self.df_filtered, self.df_unfound = filter_by_file(df_data_base, df_file, cond1_e = True, cond2_e = True, cond3_e = True, cond4_e = True, cond5_e = True)
        print("The resulted file contain: {} Total rows".format(len(self.df_filtered)))
        print("Unfound rows: ",len(self.df_unfound))
        QMessageBox.about(self, "Filtered results ", "Total results {}".format(len(self.df_filtered)))

    def ExecuteExportFile(self):
        print("Make filter")
        export_file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        time.sleep(0.3)
        if export_file_name!='':
            self.signal_make_filter.emit()
            self.df_filtered.to_csv(export_file_name)
            export_file_name = export_file_name if export_file_name.endswith('.csv') else export_file_name + '.csv'
            self.df_unfound.to_csv(export_file_name.replace('.csv', '_pending.csv'))

class WindowSelecColumnsNames(QWidget):
    signal_launch_previous_point = pyqtSignal()
    def __init__(self, selected_file):        
        self.selected_file = selected_file
        super().__init__()
        self.setWindowTitle("Confirm Columns Names")
        self.setGeometry(150, 150, 450, 350)

        # self.ButtonConfirm = QtWidgets.QPushButton('Confirm Columns')
        # self.ButtonConfirm.setFixedSize(180, 20)
        # self.ButtonConfirm.clicked.connect(self.CloseWindows)

        # Build table   
        # columns = getColumnsNames(self.dbase)
        dict_columns_names = load_check_point('check_points/columns_names.json')
        self.table = TableColumns(dict_columns_names,4,3)

        # Build buttons
        self.ButtonUpdateColumns = QtWidgets.QPushButton('Confirm Columns')
        self.ButtonUpdateColumns.setFixedSize(180, 20)
        self.ButtonUpdateColumns.clicked.connect(self.UpdateColumns)

        # Set elements
        self.Mainlayout = QVBoxLayout()
        self.Mainlayout.addWidget(self.table)
        self.Mainlayout.addWidget(self.ButtonUpdateColumns)
        # self.Mainlayout.addWidget(self.ButtonConfirm)
        # self.Tablelayout.itemAt(1).widget().setParent(None)        
        self.setLayout(self.Mainlayout) 
    def CloseWindows(self):
        self.close()

    def UpdateColumns(self):
        num_rows = self.table.rowCount()
        list_names_columns = []
        list_address_columns = []
        list_city_state_zip = []
        for current_row in range(0, num_rows):
            if self.table.item(current_row, 0):
                list_names_columns.append(self.table.item(current_row, 0).text())

            if self.table.item(current_row, 1):
                list_address_columns.append(self.table.item(current_row, 1).text())

            if self.table.item(current_row, 2):
                list_city_state_zip.append(self.table.item(current_row, 2).text())

        table_columns = list_names_columns + list_address_columns + list_city_state_zip

        df = pd.read_csv(self.selected_file)
        list_files_columns = df.columns

        cond1 = [item in list_files_columns for item in table_columns]
        not_found_indices = [i for i, value in enumerate(cond1) if not value]
        columns_approved = all(cond1)        
        
        list_columns_wrong = [table_columns[index] for index in not_found_indices]        

        if columns_approved:
            # Update database columns 
            dict_columns = {'name':list_names_columns, 'address':list_address_columns,'city_state_zip':list_city_state_zip}
            saveCheckPoint('check_points/columns_names.json', dict_columns)
            time.sleep(0.2)
            self.close()
            self.signal_launch_previous_point.emit()
        else:            
            QMessageBox.about(self, "Error", "The next columns are not in the input file: {}".format(' '.join(list_columns_wrong)))



if __name__ == "__main__":	
    app = QApplication(sys.argv)
    window = WindowMain()
    # window.setCentralWidget (frm)
    # window.resize(340, 440)
    window.show()
    # sys.exit(app.exec_())    
    app.exec()
    closeConection(dbase)
    try:
        driver.close()
    except:
        print('Chrome closed')
