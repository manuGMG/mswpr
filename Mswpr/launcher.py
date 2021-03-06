import sys, os, subprocess, pathlib
from os import listdir
from os.path import isfile, join
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QApplication, QMainWindow, QGroupBox, QRadioButton, QLabel, QSlider, QComboBox, QPushButton

main_dir = pathlib.Path(__file__).parent.absolute()

class Launcher():
    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        self.win = QMainWindow()
        self.win.setWindowTitle('Mswpr')
        self.widget = QtWidgets.QWidget(self.win)
        self.win.setCentralWidget(self.widget)

        grid = QGridLayout()
        grid.addWidget(self.widget_logo(), 0, 0)
        grid.addWidget(self.widget_modes_group(), 1, 0)
        grid.addWidget(self.widget_settings_group(), 2, 0)
        self.load_settings()

        play_button = QPushButton('Launch Mswpr!')
        play_button.clicked.connect(self.launch_game)
        grid.addWidget(play_button, 3, 0)

        self.win.setWindowIcon(QIcon(os.path.join(main_dir, 'res', '64x64-ico.png')))
        self.win.setWindowFlags(self.win.windowFlags() & Qt.CustomizeWindowHint)
        self.win.setWindowFlags(self.win.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        self.win.setFixedSize(0, 0)
        self.widget.setLayout(grid)
        self.win.show()
        sys.exit(app.exec_())
    
    def widget_logo(self):
        pic = QLabel()
        pic.setStyleSheet('padding: 10px;')
        pic.setPixmap(QPixmap(os.path.join(main_dir, 'res', 'logo.png')))
        return pic

    def widget_modes_group(self):
        modes = QGroupBox('Modes')

        self.beginner_radio = QRadioButton('Beginner (8x8)')
        self.intermediate_radio = QRadioButton('Intermediate (16x16)')
        self.expert_radio = QRadioButton('Expert (16x30)')

        vbox = QVBoxLayout()
        vbox.addWidget(self.beginner_radio)
        vbox.addWidget(self.intermediate_radio)
        vbox.addWidget(self.expert_radio)
        vbox.addStretch(1)

        modes.setLayout(vbox)
        return modes
    
    def widget_settings_group(self):
        settings = QGroupBox('Settings')

        setting1_label = QLabel('Block size')

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(20, 80)
        self.slider.valueChanged.connect(self.resize_text)

        self.size_label = QLabel()
        self.size_label.setText(str(self.slider.value()))

        setting2_label = QLabel('Select theme')

        self.themes_dropdown = QComboBox()
        [self.themes_dropdown.addItem(f.replace('.json', '')) for f in listdir(os.path.join(main_dir, 'themes')) if isfile(join(os.path.join(main_dir, 'themes'), f))]

        grid = QGridLayout()
        grid.addWidget(setting1_label, 0, 0)
        grid.addWidget(self.slider, 1, 0)
        grid.addWidget(self.size_label, 1, 1)
        grid.addWidget(setting2_label, 2, 0)
        grid.addWidget(self.themes_dropdown, 3, 0, 2, 2)
        settings.setLayout(grid)
        return settings
  
    def launch_game(self):
        self.win.hide()

        if self.beginner_radio.isChecked() == True:
            self.mode = ['Beginner', '8', '8', '10']
        elif self.intermediate_radio.isChecked() == True:
            self.mode = ['Intermediate', '16', '16', '40']
        else:
            self.mode = ['Expert', '30', '16', '99']

        self.save_settings()
        subprocess.call([sys.executable, os.path.join(main_dir, 'game.py'),
         self.themes_dropdown.currentText() + '.json', 
         self.size_label.text(), 
         self.mode[1], self.mode[2], self.mode[3]])
        self.win.show()
    
    def save_settings(self):
        with open(os.path.join(main_dir, 'settings'), 'w') as f:
            settings = self.themes_dropdown.currentText()
            settings += '\n' + self.size_label.text()
            settings += '\n' + self.mode[0]
            f.write(settings)

    def load_settings(self):
        try:
            with open(os.path.join(main_dir, 'settings'), 'r') as f:
                settings = f.read().splitlines()
        except:
            settings = None

        if settings is not None:
            # Set Mode
            if settings[2].lower() == 'beginner':
                self.beginner_radio.setChecked(True)

            elif settings[2].lower() == 'intermediate':
                self.intermediate_radio.setChecked(True)

            elif settings[2].lower() == 'expert':
                self.expert_radio.setChecked(True)
            
            # Set Block size
            self.slider.setValue(int(settings[1]))

            # Set Theme
            self.themes_dropdown.setCurrentText(settings[0])
        else:
            self.beginner_radio.setChecked(True)
        
    def resize_text(self, value):
        self.size_label.setText(str(value))

Launcher()
