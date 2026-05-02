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
        # Open file in write mode; newline = '' prevents extra blank rows in .csv file
        with open(self.filename, 'w', newline = '') as f:
            
            # Map dictionary keys to .csv column headers
            writer = csv.DictWriter(f, fieldnames = ['term', 'definition'])
            writer.writeheader()
            writer.writerows(self.cards)


    def load_cards(self) -> None:
        '''
        Checks if the .csv file exists and reads its contents into the card list
        Each row in the .csv file is converted back into a dictionary for use in the app
        '''
        # Check if file exists to avoid errors on first run
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
              
                # Convert csv rows back into a list of dictionaries
                self.cards = [row for row in reader]

    
    def add_card(self, term: str, definition: str) -> bool:
        '''
        Verifies and adds a new card to the list
        Deletes extra whitespaces and saves updated list to the .csv file
        Returns: True if card was added, False if inputs were empty
        '''
        # Removing leading and trailing whitespaces
        clean_term = term.strip()
        clean_def = definition.strip()
        
        # Only save if both fields contain text
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
        # Check if list has any cards to prevent IndexError
        if not self.cards:
            return None
        # Return dictionary (term/definition) at current session index
        return self.cards[self.current_index]


    def next_card(self) -> None:
        '''
        Increments current index to point to the next card
        Goes back to the first card if the user is at the end of the list
        '''
        if self.cards:
            # Use modulo (%) to wrap index back to 0 when at the end
            # Allows for infinite cycle through card deck
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
        
        # If UI shows term, return definition and vice versa
        if current_display_text == card['term']:
            return card['definition']
        else:
            return card['term']
        

    def reset_session(self) -> None:
        '''
        Resets study index back to the beginning
        '''
        self.current_index = 0

    
    def get_all_cards(self) -> list[dict[str, str]]:
        '''
        Returns entire list of flashcard dictionaries
        Used by UI to populate the list view
        '''
        return self.cards