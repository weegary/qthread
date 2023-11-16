# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 09:09:22 2023

@author: weeda
test threading in pyside6's qthread 
"""

from datetime import datetime
import time
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton)
from PySide6.QtCore import QRunnable, Slot, QThreadPool

class RunClass(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(RunClass, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.isRun = True

    @Slot()
    def run(self):
        while self.isRun:
            self.fn(*self.args, **self.kwargs)

class MainWindow(QMainWindow):
    def execute_this_def(self):
            self.frames.append(datetime.now())
            print(datetime.now())
            time.sleep(1)    
    
    def button_start_clicked(self):
        print("start")
        self.frames = []
        self.runclass = RunClass(self.execute_this_def)
        self.threadpool.start(self.runclass)
    
    def button_stop_clicked(self):
        self.runclass.isRun = False
        print("stop")
    
    def __init__(self, loop=None):
        super(MainWindow, self).__init__()
        self.threadpool = QThreadPool()
        
        layout = QVBoxLayout()
        button1 = QPushButton("Start")
        button1.clicked.connect(self.button_start_clicked)
        
        button2 = QPushButton("Stop")
        button2.clicked.connect(self.button_stop_clicked)
        
        layout.addWidget(button1)
        layout.addWidget(button2)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("Test QThread in Pyside6") 

if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
window = MainWindow()
window.show()
app.exec_()
