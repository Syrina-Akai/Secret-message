import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pandas.api.types import is_numeric_dtype
from PyQt5 import QtCore, QtGui, QtWidgets, uic

#☺

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainWindow.ui', self)
        
        #import button
        self.btn_import_encodage = self.findChild(QtWidgets.QPushButton, "btn_import_encodage")
        self.btn_import_encodage.clicked.connect(self.upload_data_encodage)

        self.btn_import_decodage = self.findChild(QtWidgets.QPushButton, "btn_import_decodage")
        self.btn_import_decodage.clicked.connect(self.upload_data_decodage)

        #button of decodage
        self.btn_decodage = self.findChild(QtWidgets.QPushButton, "btn_decodage")
        self.btn_decodage.setEnabled(False)

        #button of encodage
        self.btn_encodage = self.findChild(QtWidgets.QPushButton, "btn_encodage")
        self.btn_encodage.setEnabled(False)

        
        #the plot img encodage
        self.plot_img_encodage = self.findChild(QtWidgets.QVBoxLayout,"plot_img_encodage")

        #the plot img decodage
        self.plot_img_decodage = self.findChild(QtWidgets.QVBoxLayout,"plot_img_decodage")
        
        #text secret encodage
        self.secretText_encodage = self.findChild(QtWidgets.QTextEdit, "secretText_encodage")

        #text secret decodage
        self.secretText_decodage = self.findChild(QtWidgets.QTextEdit, "secretText_decodage")
        
        self.show()
        
#***************************************************IMPORT IMAGE****************************************************  
    def upload_data_encodage(self):
        dialog = QtWidgets.QFileDialog()
        fname = dialog.getOpenFileName(None, "Import file", "")
        if fname[0]!="":
            self.getData_encodage(fname[0])

    def upload_data_decodage(self):
        dialog = QtWidgets.QFileDialog()
        fname = dialog.getOpenFileName(None, "Import file", "")
        if fname[0]!="":
            self.getData_decodage(fname[0])

    def getData_encodage(self, path):
        self.data_path = path
        if path.endswith(".jpg"):
            self.data_file_type = "jpg"
            self.img = cv2.imread(path, cv2.IMREAD_COLOR)
            if self.img is None :
                print("image vide")
            else : 
                self.getPlot(layout='encodage')
            
        elif path.endswith(".png"):
            self.data_file_type = "png"
            self.img = cv2.imread(path, cv2.IMREAD_COLOR)
            if self.img is None :
                print("image vide")
            else : 
                self.getPlot(layout='encodage')

    def getData_decodage(self, path):
        self.data_path = path
        if path.endswith(".jpg"):
            self.data_file_type = "jpg"
            self.img = cv2.imread(path, cv2.IMREAD_COLOR)
            if self.img is None :
                print("image vide")
            else : 
                self.getPlot(layout='decodage')
            
        elif path.endswith(".png"):
            self.data_file_type = "png"
            self.img = cv2.imread(path, cv2.IMREAD_COLOR)
            if self.img is None :
                print("image vide")
            else : 
                self.getPlot(layout='decodage')
        


    def enregistrer_img(self):
        """if self.data_file_type == "xlsx": 
            dialog = QtWidgets.QFileDialog()
            name = dialog.getSaveFileName(self,"Save File","","Excel (*.xlsx)")
            if(name[0]!=''):
                self.data.to_excel(name[0], index=False)
        elif self.data_file_type == "csv":
            dialog = QtWidgets.QFileDialog()
            name = dialog.getSaveFileName(self,"Save File","","CSV (*.csv)")
            if(name[0]!=''):
                self.data.to_csv(name[0], index=False)
        elif self.data_file_type == "json":
            dialog = QtWidgets.QFileDialog()
            name = dialog.getSaveFileName(self,"Save File","","JSON (*.json)")
            if(name[0]!=''):
                self.data.to_json(name[0], index=False)"""
        pass

    def clearPlotLayout(self, layout):
        if layout == 'encodage' :
            for i in reversed(range(self.plot_img_encodage.count())): 
                self.plot_img_encodage.itemAt(i).widget().deleteLater()
        elif layout == 'decodage' :
            for i in reversed(range(self.plot_img_decodage.count())): 
                self.plot_img_decodage.itemAt(i).widget().deleteLater()
        

            
    def getPlot(self, layout):
        fig, ax = plt.subplots()
        self.img = ax.imshow(self.img, extent=[0, 300, 0, 300])
        ax.axis(False)
        self.canvas = FigureCanvas(fig)
        self.clearPlotLayout(layout)
        if layout == 'encodage' :
            self.plot_img_encodage.addWidget(self.canvas)
        elif layout == 'decodage' :
            self.plot_img_decodage.addWidget(self.canvas)
        self.canvas.draw()
    

    
  

    

        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())