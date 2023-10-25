from PyQt6 import QtCore, QtWidgets, QtGui, QtMultimedia
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QColorDialog, QFontDialog, QVBoxLayout, QHBoxLayout, QComboBox 
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
        self.new_window = self.window_switcher[window](fpl=self.fpl, previous_window=self.window_id)     
        self.new_window.show() 
    
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
        self.email_edit.setText('harryespley@outlook.com') 

        self.password_edit = QtWidgets.QLineEdit(self) 
        self.password_edit.setGeometry(QtCore.QRect(75, 210, 300, 30)) 
        self.password_edit.colour = 1 
        self.password_edit.setPlaceholderText('Enter Password') 
        self.password_edit.setFont(QFont(self.settings.font, 12)) 
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  
        self.password_edit.setText('James141005!') 

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
            fpl_cookies = self.session.cookies 
            self.fpl = FPL(self.session, user)   
            self.fpl.session.cookies = fpl_cookies  
            self.open_window(1) 
        else:     
            raise Exception('Invalid Login') 

class MainWindow(WindowParent): 
    def __init__(self, previous_window, fpl): 
        super().__init__(previous_window, fpl)  
        self.window_id = 1 
        self.setup_ui()  
        self.apply_colours() 
    
    def setup_ui(self): 
        self.setFixedSize(1000, 1000)  
        self.title_label = QtWidgets.QLabel(self) 
        self.title_label.setGeometry(QtCore.QRect(0, 10, 1000, 100))  
        self.title_label.colour = 1 
        self.title_label.setFont(QFont(self.settings.font, 20)) 
        self.title_label.setText('FPL Companion')  

        self.rank_label = QtWidgets.QLabel(self) 
        self.rank_label.setGeometry(QtCore.QRect(350, 150, 250, 50)) 
        self.rank_label.colour = 0 
        self.rank_label.setFont(QFont(self.settings.font, 16)) 
        self.rank_label.setText(f'Current Rank: {self.fpl.get_current_user_rank()}') 

        self.lineup_button = CustomButton(self) 
        self.lineup_button.setGeometry(QtCore.QRect(300, 250, 400, 80)) 
        self.lineup_button.colour = 1 
        self.lineup_button.setFont(QFont(self.settings.font, 14)) 
        self.lineup_button.setText('View my lineup')    
        self.lineup_button.clicked.connect(lambda: self.open_window(2)) 

        self.league_button = CustomButton(self) 
        self.league_button.setGeometry(QtCore.QRect(300, 330, 400, 80)) 
        self.league_button.colour = 1 
        self.league_button.setFont(QFont(self.settings.font, 14)) 
        self.league_button.setText('Leagues Viewer')  
        self.league_button.clicked.connect(lambda: self.open_window(3)) 

        self.database_button = CustomButton(self) 
        self.database_button.setGeometry(QtCore.QRect(300, 410, 400, 80))  
        self.database_button.colour = 1 
        self.database_button.setFont(QFont(self.settings.font, 14)) 
        self.database_button.setText('Player Database')  

        self.settings_button = CustomButton(self) 
        self.settings_button.setGeometry(QtCore.QRect(300, 490, 400, 80)) 
        self.settings_button.colour = 1 
        self.settings_button.setFont(QFont(self.settings.font, 14)) 
        self.settings_button.setText('Settings')   
        self.settings_button.clicked.connect(lambda: self.open_window(5)) 

        self.exit_button = CustomButton(self) 
        self.exit_button.setGeometry(QtCore.QRect(300, 570, 400, 80)) 
        self.exit_button.colour = 1 
        self.exit_button.setFont(QFont(self.settings.font, 14)) 
        self.exit_button.setText('Exit') 

class LineupWindow(WindowParent): 
    def __init__(self, previous_window, fpl): 
        super().__init__(previous_window, fpl) 
        self.window_id = 2  
        self.setup_ui()  
        self.apply_colours()  
        for x in self.fpl.get_current_user_picks(): 
            print(self.fpl.get_player_from_id(x['element'])) 
    
    def setup_ui(self): 
        self.setFixedSize(1000, 1000) 

        self.formation_button = CustomButton(self) 
        self.formation_button.setGeometry(QtCore.QRect(290, 10, 100, 40)) 
        self.formation_button.colour = 1 
        self.formation_button.setFont(QFont(self.settings.font, 8)) 
        self.formation_button.setText('Formation View')  
        self.formation_button.clicked.connect(self.toggle)  

        self.list_button = CustomButton(self) 
        self.list_button.setGeometry(QtCore.QRect(400, 10, 100, 40)) 
        self.list_button.colour = 1 
        self.list_button.setFont(QFont(self.settings.font, 8)) 
        self.list_button.setText('List View')  
        self.list_button.clicked.connect(self.toggle)   

        self.widget = QtWidgets.QWidget(self) 
        self.widget.setGeometry(QtCore.QRect(0, 50, 1000, 900))
    
    def toggle(self): 
        if self.sender() == self.formation_button or self.sender() == None:  
            self.formation_button.setStyleSheet('background-color: rgb(0, 255, 0);')  
            self.apply_colour(self.list_button) 
            self.setup_formation_view() 
        else: 
            self.list_button.setStyleSheet('background-color: rgb(0, 255, 0);')  
            self.apply_colour(self.formation_button) 
            self.setup_list_view() 

    def setup_list_view(self): 
        layout = QVBoxLayout() 
        self.starting_eleven = QtWidgets.QTableWidget(self) 
        self.starting_eleven.colour = 1 
        self.starting_eleven.setFont(QFont(self.settings.font, 8)) 
        self.starting_eleven.setColumnCount(5) 
        self.starting_eleven.setRowCount(11) 
        self.starting_eleven.setHorizontalHeaderLabels(['Name', 'Team', 'Position', 'Price', 'Points'])  

        self.bench  = QtWidgets.QTableWidget(self)  
        self.bench.colour = 1 
        self.bench.setFont(QFont(self.settings.font, 8)) 
        self.bench.setColumnCount(5) 
        self.bench.setRowCount(4) 
        self.bench.setHorizontalHeaderLabels(['Name', 'Team', 'Position', 'Price', 'Points'])  

        layout.addWidget(self.starting_eleven)
        layout.addWidget(self.bench) 
        self.widget.setLayout(layout) 

    def setup_formation_view(self):  
        layout = QVBoxLayout() 
        self.widget.setLayout(layout) 


class LeagueWindow(WindowParent): 
    def __init__(self, previous_window, fpl): 
        super().__init__(previous_window, fpl) 
        self.window_id = 3  
        self.leagues = self.fpl.get_current_user_leagues() 
        self.setup_ui() 
        self.apply_colours() 
    
    def setup_ui(self): 
        self.setFixedSize(1000, 1000) 

        self.league_chooser = QComboBox(self)  
        self.league_chooser.setGeometry(QtCore.QRect(0, 0, 200, 50))  
        self.league_chooser.colour = 1 
        for x in self.fpl.get_current_user_leagues():  
            self.league_chooser.addItem(x['name'])  

        self.view_league_button = CustomButton(self)   
        self.view_league_button.setGeometry(QtCore.QRect(0, 50, 200, 50))   
        self.view_league_button.colour = 1  
        self.view_league_button.setFont(QFont(self.settings.font, 8))
        self.view_league_button.setText('View League')  
        self.view_league_button.clicked.connect(self.view_league) 

        self.league_table = QtWidgets.QTableWidget(self) 
        self.league_table.setGeometry(QtCore.QRect(0, 100, 1000, 900))  
        self.league_table.colour = 1 
        self.league_table.setFont(QFont(self.settings.font, 8)) 
        self.league_table.setColumnCount(5) 
        self.league_table.setHorizontalHeaderLabels(['Rank', 'Name', 'Team Name', 'Gameweek Points', 'Total Points'])  
    
    def view_league(self):  
        self.league_table.clearContents() 
        league = self.league_chooser.currentText() 
        league_id = [x for x in self.leagues if x['name'] == league][0]['id'] 
        standings = self.fpl.get_league_standings(league_id)  
        self.league_table.setRowCount(len(standings))   
        for x in standings:  
            self.league_table.setItem(x['rank']-1, 0, QtWidgets.QTableWidgetItem(str(x['rank']))) 
            self.league_table.setItem(x['rank']-1, 1, QtWidgets.QTableWidgetItem(x['player_name'])) 
            self.league_table.setItem(x['rank']-1, 2, QtWidgets.QTableWidgetItem(x['entry_name'])) 
            self.league_table.setItem(x['rank']-1, 3, QtWidgets.QTableWidgetItem(str(x['event_total']))) 
            self.league_table.setItem(x['rank']-1, 4, QtWidgets.QTableWidgetItem(str(x['total']))) 

class DatabaseWindow(WindowParent): 
    pass 

class SettingsWindow(WindowParent): 
    def __init__(self, previous_window, fpl): 
        super().__init__(previous_window, fpl) 
        self.window_id = 5 
        self.settings_dict = {} 
        self.recent_press = None 
        self.section_switcher = { 
            'colour': self.open_colour_settings, 
            'font': self.open_font_settings, 
            'button_sound': self.open_sound_settings
        }  
        self.setup_ui() 
        self.apply_colours() 

    def settings_window_refresh(self): 
        pass 

    def open_colour_settings(self): 
        pass 

    def open_font_settings(self): 
        pass 

    def open_sound_settings(self): 
        pass  
    
    def open_font_window(self): 
        pass 

    def open_colour_window(self): 
        pass 

    def add_to_settings(self): 
        pass 

    def apply_settings(self): 
        pass   
    
    def setup_ui(self):  
        self.setFixedSize(600, 600) 
        self.title_label = QtWidgets.QLabel(self)  
        self.title_label.setGeometry(QtCore.QRect(0, 10, 600, 100))  
        self.title_label.colour = 1 
        self.title_label.setFont(QFont(self.settings.font, 20)) 
        self.title_label.setText('Settings')  

        self.back_button = CustomButton(self) 
        self.back_button.setGeometry(QtCore.QRect(0, 520, 100, 50)) 
        self.back_button.colour = 1 
        self.back_button.setFont(QFont(self.settings.font, 8)) 
        self.back_button.setText('Back')  
        self.back_button.clicked.connect(self.back_window)  

        self.apply_button = CustomButton(self) 
        self.apply_button.setGeometry(460, 520, 100, 40) 
        self.apply_button.colour = 1 
        self.apply_button.setFont(QFont(self.settings.font, 8)) 
        self.apply_button.setText('Apply') 
        self.apply_button.clicked.connect(self.apply_settings) 

        self.colour_button = CustomButton(self) 
        self.colour_button.setGeometry(QtCore.QRect(0, 150, 150, 40)) 
        self.colour_button.colour = 1 
        self.colour_button.setFont(QFont(self.settings.font, 8)) 
        self.colour_button.setText('Colour') 
        self.colour_button.clicked.connect(self.open_colour_settings)  

        self.font_button = CustomButton(self) 
        self.font_button.setGeometry(QtCore.QRect(0, 190, 150, 40)) 
        self.font_button.colour = 1 
        self.font_button.setFont(QFont(self.settings.font, 8))  
        self.font_button.setText('Font')  
        self.font_button.clicked.connect(self.open_font_settings)  

        self.sound_button = CustomButton(self) 
        self.sound_button.setGeometry(QtCore.QRect(0, 230, 150, 40)) 
        self.sound_button.colour = 1 
        self.sound_button.setFont(QFont(self.settings.font, 8)) 
        self.sound_button.setText('Button Sound')  
        self.sound_button.clicked.connect(self.open_sound_settings)  

        self.logout_button = CustomButton(self) 
        self.logout_button.setGeometry(QtCore.QRect(0, 270, 150, 40)) 
        self.logout_button.colour = 1 
        self.logout_button.setFont(QFont(self.settings.font, 8)) 
        self.logout_button.setText('Log Out')  


class ExitWindow(WindowParent): 
    pass 

if __name__ == '__main__': 
    app = QtWidgets.QApplication(sys.argv)  
    window = LoginWindow() 
    window.show()  
    sys.exit(app.exec()) 
