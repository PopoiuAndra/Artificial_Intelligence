import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class YahtzeeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yahtzee Game")
        self.setGeometry(100, 100, 800, 600)
        self.rolls_left = 3
        self.dice = [0] * 5
        self.hold_flags = [False] * 5

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Dice Area
        self.dice_layout = QHBoxLayout()
        self.dice_labels = []
        self.hold_buttons = []

        for i in range(5):
            die_label = QLabel("0")
            die_label.setAlignment(Qt.AlignCenter)
            die_label.setStyleSheet("font-size: 24px; border: 1px solid black; padding: 10px; background-color: lightblue;")
            self.dice_labels.append(die_label)
            
            hold_button = QPushButton("Hold")
            hold_button.setStyleSheet("background-color: lightgreen;")
            hold_button.clicked.connect(lambda _, idx=i: self.toggle_hold(idx))
            self.hold_buttons.append(hold_button)

            die_container = QVBoxLayout()
            die_container.addWidget(die_label)
            die_container.addWidget(hold_button)
            self.dice_layout.addLayout(die_container)

        main_layout.addLayout(self.dice_layout)

        # Roll Button
        self.roll_button = QPushButton("Roll")
        self.roll_button.setStyleSheet("font-size: 18px; background-color: orange;")
        self.roll_button.clicked.connect(self.roll_dice)
        main_layout.addWidget(self.roll_button, alignment=Qt.AlignCenter)

        # Rolls Left
        self.rolls_left_label = QLabel(f"Rolls Left: {self.rolls_left}")
        self.rolls_left_label.setAlignment(Qt.AlignCenter)
        self.rolls_left_label.setStyleSheet("font-size: 18px; margin-top: 10px;")
        main_layout.addWidget(self.rolls_left_label)

        # Score Table
        self.score_table = QTableWidget(13, 2)
        self.score_table.setHorizontalHeaderLabels(["Category", "Score"])
        self.score_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.score_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.score_table.setStyleSheet("background-color: lightyellow;")
        categories = [
            "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Three of a Kind", "Four of a Kind", "Full House",
            "Small Straight", "Large Straight", "Yahtzee", "Chance"
        ]

        for i, category in enumerate(categories):
            self.score_table.setItem(i, 0, QTableWidgetItem(category))

        self.score_table.doubleClicked.connect(self.handle_table_click)
        main_layout.addWidget(self.score_table)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def roll_dice(self):
        if self.rolls_left > 0:
            for i in range(5):
                if not self.hold_flags[i]:
                    self.dice[i] = random.randint(1, 6)
                    self.dice_labels[i].setText(str(self.dice[i]))

            self.rolls_left -= 1
            self.rolls_left_label.setText(f"Rolls Left: {self.rolls_left}")

    def toggle_hold(self, idx):
        self.hold_flags[idx] = not self.hold_flags[idx]
        color = "red" if self.hold_flags[idx] else "lightgreen"
        self.hold_buttons[idx].setStyleSheet(f"background-color: {color};")

    def handle_table_click(self):
        selected_row = self.score_table.currentRow()
        category = self.score_table.item(selected_row, 0).text()
        
        # Example scoring logic (to be extended as per rules)
        valid = self.validate_selection(category)

        if valid:
            self.score_table.setItem(selected_row, 1, QTableWidgetItem("Valid"))
            self.reset_roll()
        else:
            self.score_table.setItem(selected_row, 1, QTableWidgetItem("Invalid"))

    def validate_selection(self, category):
        if category == "Ones":
            return any(die == 1 for die in self.dice)
        elif category == "Twos":
            return any(die == 2 for die in self.dice)
        # Add more validation logic for other categories as needed
        return False

    def reset_roll(self):
        self.rolls_left = 3
        self.rolls_left_label.setText(f"Rolls Left: {self.rolls_left}")
        self.dice = [0] * 5
        self.hold_flags = [False] * 5
        for i in range(5):
            self.dice_labels[i].setText("0")
            self.hold_buttons[i].setStyleSheet("background-color: lightgreen;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = YahtzeeGame()
    game.show()
    sys.exit(app.exec())
