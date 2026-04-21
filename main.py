import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.ui_flash import Ui_MainWindow
from logic.flashcard_logic import FlashcardLogic

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic = FlashcardLogic()

        # Connect buttons to functions
        self.button_add.clicked.connect(self.add_card)
        self.button_next.clicked.connect(self.show_next_card)

    def add_card(self):
        term = self.input_term.text()
        definition = self.input_definition.text()
        if self.logic.add_card(term, definition):
            self.input_term.clear()
            self.input_definition.clear()
            print("Card added!")

    def show_next_card(self):
        card = self.logic.get_current_card()
        if card:
            self.label_display.setText(card['term'])
            self.logic.next_card()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())