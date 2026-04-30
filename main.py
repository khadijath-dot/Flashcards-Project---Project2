import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from ui.ui_main_window import Ui_MainWindow
from logic.flashcard_logic import FlashcardLogic

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.card_list_widget.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.logic = FlashcardLogic()
        self.button_study.clicked.connect(self.start_study)
        self.button_add.clicked.connect(self.add_card)
        self.button_next.clicked.connect(self.show_next_card)
        self.button_flip.clicked.connect(self.flip_card)
        self.label_term.setText('Term')
        self.statusBar().showMessage("Ready")

    def add_card(self):
        term = self.input_term.text()
        definition = self.input_definition.text()
        if self.logic.add_card(term, definition):
            self.input_term.clear()
            self.input_definition.clear()
            self.statusBar().showMessage("Card added successfully", 2000)
            self.update_list_view()

    def start_study(self):
        card = self.logic.get_current_card()
        if card:
            self.label_display.setText(card['term'])
            self.statusBar().showMessage("Study started")
        else:
            self.statusBar().showMessage("Please add a card first.")

    def show_next_card(self):
        card = self.logic.get_current_card()
        if card:
            self.label_display.setText(card['term'])
            self.logic.next_card()

    def flip_card(self):
        card = self.logic.get_current_card()
        if not card:
            return
        if self.label_display.text() == card['term']:
            self.label_display.setText(card['definition'])
        else:
            self.label_display.setText(card['term'])

    def update_list_view(self):
        self.card_list_widget.clear()
        all_cards = self.logic.get_all_cards()
        for card in all_cards:
            display_text = f"{card['term']} : {card['definition']}"
            self.card_list_widget.addItem(display_text)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())