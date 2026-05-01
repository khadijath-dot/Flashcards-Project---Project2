import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QListWidgetItem
from ui.ui_main_window import Ui_MainWindow
from logic.flashcard_logic import FlashcardLogic

class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    Main window class for Flashcard application
    Handles UI interactions and connects user inputs to the back-end logic
    '''

    def __init__(self) -> None:
        '''
        Initializes UI, sets up widget properties like WordWrap,
        connects buttons to their respective functions, and loads existing flashcards
        '''
        super().__init__()
        self.setupUi(self)
        self.label_display.setWordWrap(True)
        self.label_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_list_widget.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.card_list_widget.setWordWrap(True)
        self.button_study.clicked.connect(self.start_study)
        self.button_add.clicked.connect(self.add_card)
        self.button_next.clicked.connect(self.show_next_card)
        self.button_flip.clicked.connect(self.flip_card)
        self.label_term.setText('Term')
        self.statusBar().showMessage("Ready")
        self.logic = FlashcardLogic()
        self.update_list_view()


    def add_card(self) -> None:
        '''
        Gets text from term and definition input fields, sends to logic handler,
        for saving, and updates list view
        '''
        term = self.input_term.text()
        definition = self.input_definition.text()
        if self.logic.add_card(term, definition):
            self.input_term.clear()
            self.input_definition.clear()
            self.statusBar().showMessage("Card added successfully", 2000)
            self.update_list_view()


    def start_study(self) -> None:
        '''
        Starts study sessions by getting the current flashcard from logic
        and showing the term on the main display label
        '''
        card = self.logic.get_current_card()
        if card:
            self.label_display.setText(card['term'])
            self.statusBar().showMessage("Study started")
        else:
            self.statusBar().showMessage("Please add a card first.")


    def show_next_card(self) -> None:
        '''
        Advances flashcard index in the logic handler and updates the display label
        to show the next term in the set
        '''
        card = self.logic.get_current_card()
        if card:
            self.label_display.setText(card['term'])
            self.logic.next_card()


    def flip_card(self) -> None:
        '''
        Toggles display between the current card's term and definition
        by asking for the 'flipped' text from the logic handler
        '''
        current_text = self.label_display.text()
        new_text = self.logic.get_flipped_text(current_text)
        
        if new_text:
            self.label_display.setText(new_text)


    def update_list_view(self) -> None:
        '''
        Clears side list widget and repopulates with all currently saved cards,
        sorted alphabetically by term
        Enables editing flags for each item
        '''
        self.card_list_widget.clear()
        all_cards = self.logic.get_all_cards()
        sorted_cards = sorted(all_cards, key = lambda x: x['term'].lower())
        for card in sorted_cards:
            display_text = f"{card['term']} : {card['definition']}"
            item = QListWidgetItem(display_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.card_list_widget.addItem(item)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())