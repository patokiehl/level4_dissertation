import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox, QRadioButton, QButtonGroup
)

from src.Log import Logger 
class MetaPage(QMainWindow):
    def __init__(self, on_submit):
        super().__init__()
        self.on_submit = on_submit
        self.setWindowTitle('User Input Page')
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # USERID input
        self.userid_label = QLabel('USERID:')
        self.userid_input = QLineEdit()
        self.layout.addWidget(self.userid_label)
        self.layout.addWidget(self.userid_input)

        # Gender 
        self.gender_layout = QHBoxLayout()
        self.gender_layout.addWidget(QLabel('Gender:'))
        self.male = QRadioButton('Male')
        self.female = QRadioButton('Female') 
        self.other_gender = QRadioButton('Other')
        self.gender_group = QButtonGroup(self)
        self.gender_group.addButton(self.male)
        self.gender_group.addButton(self.female)
        self.gender_group.addButton(self.other_gender)
        self.gender_layout.addWidget(self.male)
        self.gender_layout.addWidget(self.female)
        self.gender_layout.addWidget(self.other_gender)
        self.layout.addLayout(self.gender_layout)

        # Temperature of Room 
        self.temp_label = QLabel('Recorded Temp at start:')
        self.temp_input = QLineEdit()
        self.layout.addWidget(self.temp_label)
        self.layout.addWidget(self.temp_input)
        
        # Participant Agge
        self.radio_layout = QHBoxLayout() 
        self.radio_layout.addWidget(QLabel('Age:'))
        self.age_18_24 = QRadioButton('18-24')
        self.age_24_30 = QRadioButton('24-30')
        self.age_30_36 = QRadioButton('30-36')
        self.age_group = QButtonGroup(self)
        self.age_group.addButton(self.age_18_24)
        self.age_group.addButton(self.age_24_30)
        self.age_group.addButton(self.age_30_36)
        self.radio_layout.addWidget(self.age_18_24)
        self.radio_layout.addWidget(self.age_24_30)
        self.radio_layout.addWidget(self.age_30_36)
        self.layout.addLayout(self.radio_layout)

        # Manaul Labour - does this have an effect 
        self.manual_layout = QVBoxLayout()
        self.manual_layout.addWidget(QLabel('How many hours a day do you work in a manual labour sense?:'))

        self.manual_layout_buttons = QHBoxLayout()
        self.manual_0_1 = QRadioButton('0-1')
        self.manual_1_3 = QRadioButton('1-3')
        self.manual_3_6 = QRadioButton('3-6') 
        self.manual_6_plus = QRadioButton('6+')
        self.manual_group = QButtonGroup(self)
        self.manual_group.addButton(self.manual_0_1)
        self.manual_group.addButton(self.manual_1_3)
        self.manual_group.addButton(self.manual_3_6)
        self.manual_group.addButton(self.manual_6_plus)
        self.manual_layout_buttons.addWidget(self.manual_0_1)
        self.manual_layout_buttons.addWidget(self.manual_1_3)
        self.manual_layout_buttons.addWidget(self.manual_3_6)
        self.manual_layout_buttons.addWidget(self.manual_6_plus)

        self.manual_layout.addLayout(self.manual_layout_buttons)
        self.layout.addLayout(self.manual_layout)

        # Submit Button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
    
    def submit(self):
        userid = self.userid_input.text().strip()
        if not userid:
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid User ID.')
            return
        
        temperature = self.temp_input.text().strip()

        selected_manual = self.manual_group.checkedButton()
        manual = selected_manual.text() if selected_manual else QMessageBox.warning(self, 'Input Error', 'Please fill out the manual labour field.')

        selected_gender = self.gender_group.checkedButton()
        gender = selected_gender.text() if selected_gender else QMessageBox.warning(self, 'Input Error', 'Please select a Gender.')

        selected_age = self.age_group.checkedButton()
        age_range = selected_age.text() if selected_age else QMessageBox.warning(self, 'Input Error', 'Please select an age range')

        self.Logger = Logger(userid)
        self.Logger.write_meta(userid, age_range, gender, temperature, manual)
        self.on_submit(userid)
        self.close()