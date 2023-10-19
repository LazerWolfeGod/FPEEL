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
    def __init__(self, previous_window=None, fpl=None): 
        super().__init__() 
        self.previous_window = previous_window 
        self.fpl = fpl  
        self.window_id = None 
        self.window_switcher = { 
            0: LoginWindow, 
            1: MainWindow, 
            2: LineupWindow, 
            3: LeagueWindow,  
            4: DatabaseWindow, 
            5: SettingsWindow, 
            6: ExitWindow
        } 
        self.colour_switcher = { 
            0: f'background-color: {self.settings.colour_scheme.primary_colour}'f'color: {self.settings.colour_scheme.secondary_colour}', 
            1: f'background-color: {self.settings.colour_scheme.secondary_colour}'f'color: {self.settings.colour_scheme.primary_colour}' 
        } 
    
    def refresh(self): 
        self.close() 
        self.new_window = self.window_switcher[self.window_id](fpl=self.fpl, previous_window=self.previous_window) 

    def open_window(self, window): 
        if window != 6: 
            self.close() 
        self.new_window = self.window_switcher[self.window_id](fpl=self.fpl, previous_window=self.window_id) 

class Settings: 
    def __init__(self): 
        self.settings_path = os.path.join(os.getcwd(), 'json_data', 'settings.json') 
        try: 
            settings = utils.read_jsoN(self.settings_path) 
        except json.JSONDecodeError: 
            settings = { 
                'primary_colour': None, 
                'secondary_colour': None, 
                'font': 'Arial', 
                'button_sound': None, 
                'button_volume': None 
            } 
            utils.write_json(settings, self.settings_path) 
        self.colour_scheme = ColourScheme(settings['primary_colour'], settings['secondary_colour']) 
        self.font = settings['font'] 
        self.button_sound = settings['button_sound'] 
        self.button_volume = settings['button_volume'] 
    
    def change_settings(self, settings_dict): 
        settings = utils.read_json(self.settings_path)
        for k in settings_dict: 
            settings[k] = settings_dict[k] 
            self.settings_switcher[k] = settings_dict[k] 
        utils.write_json(self.settings_path, settings) 

@dataclass 
class ColourScheme: 
    primary_colour: str = None 
    secondary_colour: str = None 
    error_colour = 'rgb(255, 0, 0);' 

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




if __name__ == '__main__': 
    app = QtWidgets.QApplication(sys.argv) 
    window = WindowParent()
    window.show()  
    print(window.previous_window) 
    sys.exit(app.exec()) 
