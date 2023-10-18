from PyQt6 import QtCore, QtWidgets, QtGui, QtMultimedia
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QColorDialog, QFontDialog, QVBoxLayout, QHBoxLayout 
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor 
from PyQt6.QtCore import QUrl 
from PyQt6.QtMultimedia import QSoundEffect   
from dataclasses import dataclass  
from fpl import FPL 
import requests 
import mysql.connector 
import json 
import sys    
import os 
import utils  
import base  

class WindowParent(QMainWindow): 
    pass 

class LoginWindow(WindowParent): 
    pass  

class FPLWindow(WindowParent): 
    pass 

class MainWindow(FPLWindow): 
    pass 

class LineupWindow(FPLWindow): 
    pass 

class LeagueWindow(FPLWindow): 
    pass  

class DatabaseWindow(FPLWindow): 
    pass 

class SettingsWindow(WindowParent): 
    pass 

class ExitWindow(WindowParent): 
    pass 




