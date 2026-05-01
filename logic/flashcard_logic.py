import csv
import os

class FlashcardLogic:
    '''
    Handles data management and business logic for flashcards
    Manages loading, saving, and navigating the flashcard collection
    '''
    def __init__(self) -> None:
        '''
        Initializes the logic handler with an empty card list,
        sets the starting index, and attempts to load existing cards from disk
        '''
        self.cards: list[dict[str, str]] = []
        self.current_index: int = 0
        self.filename = 'flashcards.csv'
        self.load_cards


    def save_cards(self) -> None:
        '''
        Writes current list of flashcards to a .csv file
        Uses DictWriter to ensure term and definition keys are mapped correctly
        '''
        with open(self.filename, 'w', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames = ['term', 'definition'])
            writer.writeheader()
            writer.writerows(self.cards)


    def load_cards(self) -> None:
        '''
        Checks if the .csv file exists and reads its contents into the card list
        Each row in the .csv file is converted back into a dictionary for use in the app
        '''
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                self.cards = [row for row in reader]

    
    def add_card(self, term: str, definition: str) -> bool:
        '''
        Verifies and adds a new card to the list
        Deletes extra whitespaces and saves updated list to the .csv file
        Returns: True if card was added, False if inputs were empty
        '''
        clean_term = term.strip()
        clean_def = definition.strip()
        if clean_term and clean_def:
            self.cards.append({'term': clean_term, 'definition': clean_def})
            self.save_cards()
            return True
        return False


    def get_current_card(self) -> dict[str, str] | None:
        '''
        Returns dictionary representing the card at current index
        Returns: None if the card list is empty
        '''
        if not self.cards:
            return None
        return self.cards[self.current_index]


    def next_card(self) -> None:
        '''
        Increments current index to point to the next card
        Goes back to the first card if the user is at the end of the list
        '''
        if self.cards:
            self.current_index = (self.current_index + 1) % len(self.cards)

  
    def get_flipped_text(self, current_display_text: str) -> str | None:
        '''
        Flips the card
        Determines whether to show the term or definition based what is currently on 
        the display label
        '''
        card = self.get_current_card()
        if not card:
            return None
        if current_display_text == card['term']:
            return card['definition']
        else:
            return card['term']

    
    def get_all_cards(self):
        '''
        Returns entire list of flashcard dictionaries
        Used by UI to populate the list view
        '''
        return self.cards