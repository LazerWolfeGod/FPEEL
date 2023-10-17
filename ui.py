from PyQt6 import QtCore, QtWidgets, QtGui, QtMultimedia
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QColorDialog, QFontDialog, QVBoxLayout, QHBoxLayout 
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor 
from PyQt6.QtCore import QUrl 
from PyQt6.QtMultimedia import QSoundEffect  
import requests 
import mysql.connector 
import json 
import sys   
import utils 


class WindowParent(QMainWindow): 
    def __init__(self, fpl, previous_window=None): 
        super().__init__() 
        self.fpl = fpl 
        self.previous_window = previous_window  
        self.settings = Settings()  
        self.setStyleSheet(f'background-color: {self.settings.colour_scheme.primary_colour}') 
        self.window_switcher = { 
            0: LoginWindow, 
            1: MainWindow, 
            2: LineupWindow, 
            3: LeagueWindow, 
            4: SettingsWindow, 
            5: ExitWindow
        } 
        self.colour_switcher = { 
            0: f'background-color: {self.settings.colour_scheme.primary_colour}'f'color: {self.settings.colour_scheme.secondary_colour}', 
            1: f'background-color: {self.settings.colour_scheme.secondary_colour}'f'color: {self.settings.colour_scheme.primary_colour}' 
        } 
    
    def refresh(self): 
        self.close() 
        self.new_window = self.window_switcher[self.window_id](self.fpl, previous_window=self.previous_window)  
        self.new_window.show()   

    def open_window(self, window): 
        if window != 4: 
            self.close() 
        self.new_window = self.window_switcher[window](self.fpl, previous_window=self.window_type) 
        self.new_window.show()  
    
    def back(self): 
        if self.previous_window: 
            self.open_window(self.previous_window) 
    
    def apply_colour(self, widget): 
        widget.setStyleSheet(self.colour_switcher[widget.colour]) 
    
    def apply_colours(self): 
        for widget in self.findChildren(QWidget): 
            if hasattr(widget, 'colour'): 
                self.apply_colour(widget)  
    
    def remove_widget(self, widget): 
        widget.setParent(None) 
    
    def clear_widgets(self, attr): 
        for widget in self.findChildren(widget): 
            if hasattr(widget, attr): 
                self.remove_widget(widget)  

class CustomButton(QPushButton): 
    def __init__(self, parent=None): 
        super().__init__(parent) 
        self.parent = parent 
        self.clicked.connect(self.handle_clicked) 
        if self.parent: 
            self.sound_effect = QSoundEffect() 
            self.sound_effect.setSource(QUrl.fromLocalFile(self.parent.settings.button_sound)) 
    
    def play_sound(self, volume): 
        self.sound_effect.setVolume(volume) 
        self.sound_effect.play() 
    
    def handle_clicked(self): 
        if self.parent: 
            self.play_sound(self.parent.settings.button_volume)  

class InfoLabel(QLabel): 
    def __init__(self): 
        super().__init__() 
    
    def setInfoText(self, text=None): 
        self.setToolTip(text) 
    
class LoginWindow(WindowParent): 
    pass 

class MainWindow(WindowParent): 
    pass 

class LineupWindow(WindowParent): 
    pass 

class LeagueWindow(WindowParent): 
    pass 

class SettingsWindow(WindowParent): 
    pass 

class ExitWindow(WindowParent): 
    pass 

class Settings: 
    pass 

class ColourScheme: 
    pass 

