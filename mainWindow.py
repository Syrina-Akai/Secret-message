import sys
import cv2, imutils
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from codage import Encode

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
        self.btn_decodage.clicked.connect(self.decodage_function)
        #self.btn_decodage.setEnabled(False)

        #button of encodage
        self.btn_encodage = self.findChild(QtWidgets.QPushButton, "btn_encodage")
        self.btn_encodage.clicked.connect(self.codage_function)
        #self.btn_encodage.setEnabled(False)

        #button of creation img from text
        self.btn_create_img_text = self.findChild(QtWidgets.QPushButton, "btn_create_img_text")
        self.btn_create_img_text.clicked.connect(self.code_text)

        #button to save encoded image
        self.btn_enregistrer = self.findChild(QtWidgets.QPushButton, "btn_enregistrer")
        self.btn_enregistrer.clicked.connect(self.enregistrer_img)
        self.btn_enregistrer.hide()
        
        #the plot img_text_encode 
        self.plot_img_text_encode = self.findChild(QtWidgets.QVBoxLayout,"plot_img_text_encode")
        self.img_frame_text = QtWidgets.QLabel()
        self.plot_img_text_encode.addWidget(self.img_frame_text)

        #the plot img encodage
        self.plot_img_encodage = self.findChild(QtWidgets.QVBoxLayout,"plot_img_encodage")
        self.image_frame_encodage = QtWidgets.QLabel()
        self.plot_img_encodage.addWidget(self.image_frame_encodage)
        self.img_encodage = cv2.imread("no_image.jpg", cv2.IMREAD_COLOR)
        self.getPlot('encodage')
        self.img_encode_path = None

        #the plot img decodage
        self.plot_img_decodage = self.findChild(QtWidgets.QVBoxLayout,"plot_img_decodage")
        self.image_frame_decodage = QtWidgets.QLabel()
        self.plot_img_decodage.addWidget(self.image_frame_decodage)
        self.img_decodage = cv2.imread("no_image.jpg", cv2.IMREAD_COLOR)
        self.getPlot('decodage')
        self.img_decode_path = None

        #the plot img_text_decode
        self.plot_img_text_decod = self.findChild(QtWidgets.QVBoxLayout,"plot_img_text_decod")
        self.findChild(QtWidgets.QVBoxLayout,"plot_img_text_encode")
        self.img_frame_text_decode = QtWidgets.QLabel()
        self.plot_img_text_decod.addWidget(self.img_frame_text_decode)

        #text secret encodage
        self.secretText_encodage = self.findChild(QtWidgets.QTextEdit, "secretText_encodage")

        
        self.show()
        
#***************************************************IMPORT IMAGE****************************************************  
    def upload_data_encodage(self):
        
        dialog = QtWidgets.QFileDialog()
        fname = dialog.getOpenFileName(None, "Import image", filter="JPG(*.jpg);;PNG(*.png)")
        if fname[0]!="":
            self.getData_encodage(fname[0])

    def upload_data_decodage(self):
        dialog = QtWidgets.QFileDialog()
        fname = dialog.getOpenFileName(None, "Import image", filter="JPG(*.jpg);;PNG(*.png)")
        if fname[0]!="":
            self.getData_decodage(fname[0])

    def getData_encodage(self, path):
        self.img_encode_path = path

        if path.endswith(".jpg"):
            self.data_file_type = "jpg"      

        elif path.endswith(".png"):
            self.data_file_type = "png"

        self.img_encodage = cv2.imread(path, cv2.IMREAD_COLOR)
        if self.img_encodage is None :
            print("image vide")
        else : 
            self.getPlot(layout='encodage')
            #self.btn_encodage.setEnabled(True)

    def getData_decodage(self, path):
        self.img_decode_path = path
        if path.endswith(".jpg"):
            self.data_file_type = "jpg"           
        elif path.endswith(".png"):
            self.data_file_type = "png"
        self.img_decodage = cv2.imread(path, cv2.IMREAD_COLOR)
        if self.img_decodage is None :
            print("image vide")
        else : 
            self.getPlot(layout='decodage')
            #self.btn_decodage.setEnabled(True)

#***************************************************SAVE IMAGE**************************************************** 
    def enregistrer_img(self):
        dialog = QtWidgets.QFileDialog()
        name = dialog.getSaveFileName(self,"Save image","",filter="PNG(*.png)")
        if(name[0]!=''):	
            cv2.imwrite(name[0], self.img_encodage)
            print("image saved.")
            self.btn_enregistrer.hide()

#***************************************************SHOW IMAGE****************************************************     
    def getPlot(self, layout):       
        if layout == 'encodage' :
            image = imutils.resize(self.img_encodage,width=500, height = self.img_encodage.shape[0])
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QtGui.QImage.Format_RGB888)
            self.image_frame_encodage.setPixmap(QtGui.QPixmap.fromImage(image))

        elif layout == 'decodage' :
            image = imutils.resize(self.img_decodage,width=500, height = self.img_decodage.shape[0])
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QtGui.QImage.Format_RGB888)
            self.image_frame_decodage.setPixmap(QtGui.QPixmap.fromImage(image))
#***************************************************CODE TEXT*****************************************************

    def code_text(self):
        text = self.secretText_encodage.toPlainText()
        
        if text != '':
            encodage = Encode(text = text)
            self.img_text = encodage.convert_text_img()
            image = imutils.resize(self.img_text,width=500, height = self.img_text.shape[0])
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QtGui.QImage.Format_RGB888)
            self.img_frame_text.setPixmap(QtGui.QPixmap.fromImage(image))

#***************************************************CODE IMAGE**************************************************** 
    def codage_function(self):
        if self.img_encode_path is not None :
            encode = Encode(self.img_encode_path)
            if len(self.img_text.ravel())+9 < len(self.img_encodage.ravel()) :
                self.img_encodage =  encode.insert_into_image(self.img_text)
                if self.img_encodage!= []:
                    self.secretText_encodage.setPlainText('')
                    self.btn_enregistrer.show()
        else : 
            message = "Aucune image n'est selectionné "
            if self.secretText_encodage.toPlainText() == '':
                message += "et text secret vide !"
            else : message += "!"
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            
            msg.setText(message)
            msg.setWindowTitle("Alerte codage")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            retval = msg.exec_()
                
#***************************************************DECODE IMAGE**************************************************** 
    def decodage_function(self):
        if self.img_decode_path is not None :
            encode = Encode(self.img_decode_path)
            img_text_decode =  encode.get_from_img()
            image = imutils.resize(img_text_decode,width=500, height = img_text_decode.shape[0])
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QtGui.QImage.Format_RGB888)
            self.img_frame_text_decode.setPixmap(QtGui.QPixmap.fromImage(image))
        else : 
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            
            msg.setText("Aucune image n'est selectionné pour le décodage !")
            msg.setWindowTitle("Alerte décodage")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            retval = msg.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
