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
    def __init__(self, previous_window, fpl): 
        super().__init__() 
        self.previous_window = previous_window  
        self.fpl = fpl  
        self.settings = Settings()  
        self.setStyleSheet(f'background-color: {self.settings.colour_scheme.primary_colour}')  
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
    
    def back_window(self): 
        if self.previous_window: 
            self.open_window(self.previous_window) 

    def apply_colour(self, widget): 
        widget.setStyleSheet(self.colour_switcher[widget.colour]) 
    
    def apply_colours(self): 
        for widget in self.findChildren(QWidget): 
            if hasattr(widget, 'colour'): 
                self.apply_colour(widget)  

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

class Settings: 
    def __init__(self): 
        self.settings_path = os.path.join(os.getcwd(), 'json_data', 'settings.json') 
        try: 
            settings = utils.read_json(self.settings_path) 
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
    def __init__(self, previous_window=None, fpl=None): 
        super().__init__(previous_window, fpl)    
        self.session = requests.Session() 
        self.window_id = 0   
        self.setup_ui() 
        self.apply_colours() 
    
    def setup_ui(self): 
        self.setFixedSize(750, 750) 
        self.title_label = QtWidgets.QLabel(self) 
        self.title_label.setGeometry(QtCore.QRect(0, 15, 750, 75)) 
        self.title_label.colour = 1 
        self.title_label.setFont(QFont(self.settings.font, 30))  
        self.title_label.setText('FPL Helper') 

        self.email_edit = QtWidgets.QLineEdit(self) 
        self.email_edit.setGeometry(QtCore.QRect(75, 135, 300, 30)) 
        self.email_edit.colour = 1 
        self.email_edit.setPlaceholderText('Enter Email') 
        self.email_edit.setFont(QFont(self.settings.font, 12)) 

        self.password_edit = QtWidgets.QLineEdit(self) 
        self.password_edit.setGeometry(QtCore.QRect(75, 210, 300, 30)) 
        self.password_edit.colour = 1 
        self.password_edit.setPlaceholderText('Enter Password') 
        self.password_edit.setFont(QFont(self.settings.font, 12)) 
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password) 

        self.Email_label = QtWidgets.QLabel(self) 
        self.Email_label.setGeometry(QtCore.QRect(75, 105, 300, 30)) 
        self.Email_label.colour = 0  
        self.Email_label.setText('Email:') 
        self.Email_label.setFont(QFont(self.settings.font, 12))  

        self.password_label = QtWidgets.QLabel(self) 
        self.password_label.setGeometry(QtCore.QRect(75, 180, 300, 30)) 
        self.password_label.colour = 0 
        self.password_label.setText('Password:') 
        self.password_label.setFont(QFont(self.settings.font, 12))   

        self.error_label = QtWidgets.QLabel(self) 
        self.error_label.setGeometry(QtCore.QRect(150, 105, 300, 30)) 
        self.error_label.setStyleSheet(f'color: {self.settings.colour_scheme.error_colour}')
        self.error_label.setFont(QFont(self.settings.font, 12))  

        self.login_button = CustomButton(self) 
        self.login_button.setGeometry(QtCore.QRect(75, 255, 300, 30)) 
        self.login_button.colour = 1 
        self.login_button.setText('Login') 
        self.login_button.setFont(QFont(self.settings.font, 12)) 
        self.login_button.clicked.connect(self.check_login) 

        self.exit_button = CustomButton(self) 
        self.exit_button.setGeometry(QtCore.QRect(75, 300, 300, 30)) 
        self.exit_button.colour = 1 
        self.exit_button.setText('Exit') 
        self.exit_button.setFont(QFont(self.settings.font, 12)) 
        self.exit_button.clicked.connect(lambda: self.open_window(5))   

    def check_login(self): 
        cookies = utils.get_account_cookies(self.session, self.email_edit.text(), self.password_edit.text())  
        if cookies: 
            user = utils.create_user_object(self.session, cookies) 
            fpl = FPL(self.session, user) 
            self.open_window(1) 
        else: 
            raise Exception('Invalid Login') 

class MainWindow(WindowParent): 
    def __init__(self, previous_window, fpl): 
        super().__init__(previous_window, fpl) 
    
    def setup_ui(self): 
        pass 

class LineupWindow(WindowParent): 
    pass 

class LeagueWindow(WindowParent): 
    pass  

class DatabaseWindow(WindowParent): 
    pass 

class SettingsWindow(WindowParent): 
    pass 

class ExitWindow(WindowParent): 
    pass 




if __name__ == '__main__': 
    app = QtWidgets.QApplication(sys.argv) 
    window = LoginWindow() 
    window.show()  
    sys.exit(app.exec()) 
