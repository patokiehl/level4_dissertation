from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

class InputsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_edits = {}
        self.previous_values = {}

        self.layout = QVBoxLayout()

        self.input_layout = QHBoxLayout()
        self.create_line_edit("Enter Amplitude", "AMPL")
        self.create_line_edit("Enter Pulse Width", "PW")
        self.create_line_edit("Enter Pulse Interval", "PI")
        self.create_line_edit("Enter Pulses per Burst", "PPB")
        self.create_line_edit("Enter Frequency", "FREQ")
        self.layout.addLayout(self.input_layout)


        self.button_layout = QHBoxLayout()
        self.set_default_min_button = QPushButton("Set Default Min")   
        self.set_default_min_button.clicked.connect(self.set_default_min_values)

        self.set_default_max_button = QPushButton("Set Default Max")
        self.set_default_max_button.clicked.connect(self.set_default_max_values)

        self.button_layout.addWidget(self.set_default_min_button)
        self.button_layout.addWidget(self.set_default_max_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def create_line_edit(self, placeholder, prefix):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_edits[prefix] = line_edit
        self.previous_values[prefix] = 0.0

        self.input_layout.addWidget(line_edit)

    def collect_inputs_as_string(self):
        parts = []
        for prefix, line_edit in self.line_edits.items():
            text_value = line_edit.text().strip()
            if text_value:
                try:
                    float_val = float(text_value)
                    self.previous_values[prefix] = float_val
                except ValueError:
                    float_val = self.previous_values[prefix]
            else:
                float_val = self.previous_values[prefix]

            part = f"{prefix}:{float_val}"
            parts.append(part)

        final_string = "|".join(parts)
        return final_string

    def set_default_max_values(self):
        default_max_values = {"AMPL": 3.0,"PW": 1,"PI": 300,"PPB": 3, "FREQ": 0.3}
        for key, value in default_max_values.items():
            self.line_edits[key].setText(str(value)) 
            self.previous_values[key] = value 

    def set_default_min_values(self):
        default_min_values = {"AMPL": 1.5,"PW": 2,"PI": 300,"PPB": 3,"FREQ": 0.3 }
        for key, value in default_min_values.items():
            self.line_edits[key].setText(str(value))
            self.previous_values[key] = value