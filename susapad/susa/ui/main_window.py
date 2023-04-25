
import dataclasses as ds
import time

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from susapad.susa.controler import susapad
from . import settings_window, alert_dialog
from .widgets.common import window
from .widgets import main_window


class MainWindow(window.BaseWindow):

    def __init__(self, susapad):

        ## Configuration
        super().__init__(susapad)

        ## Configure Layout
        self.main_widget = main_window.WindowLayout(self)
        self.layout.addWidget(self.main_widget)

        ## Startup
        self.connect_to_susapad()

    
    @QtCore.Slot()
    def connect_to_susapad(self):
        port = self.susapad.find()
        if "" == port:
            # Todo: set it as false for production
            self.main_widget.group_button.main.set_found(True)
            self.main_widget.group_header.status.setText("SusaPad não encontrado!")
            
            alert = alert_dialog.AlertDialog(self)
            alert.show()

        else:
            self.main_widget.group_button.main.set_found(True)
            self.main_widget.group_header.status.setText(f"SusaPad encontrado na porta {port}")

    @QtCore.Slot()
    def open_settings_window(self):
        pass

    ## Style Configuration

    def _configure_shadows(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setOffset(QtCore.QPoint(0,0))
        shadow.setBlurRadius(30)
        shadow.setColor(QtGui.QColor(0,0,0))
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None
