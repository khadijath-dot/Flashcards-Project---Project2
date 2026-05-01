import csv
import os

class FlashcardLogic:
    def __init__(self) -> None:
        self.cards: list[dict[str, str]] = []
        self.current_index: int = 0
        self.filename = 'flashcards.csv'
        self.load_cards


    def save_cards(self):
        with open(self.filename, 'w', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames = ['term', 'definition'])
            writer.writeheader()
            writer.writerows(self.cards)


    def load_cards(self) -> None:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                self.cards = [row for row in reader]

    
    def add_card(self, term: str, definition: str) -> bool:
        clean_term = term.strip()
        clean_def = definition.strip()
        if clean_term and clean_def:
            self.cards.append({'term': clean_term, 'definition': clean_def})
            self.save_cards()
            return True
        return False


    def get_current_card(self) -> dict[str, str] | None:
        if not self.cards:
            return None
        return self.cards[self.current_index]


    def next_card(self) -> None:
        if self.cards:
            self.current_index = (self.current_index + 1) % len(self.cards)

  
    def get_flipped_text(self, current_display_text: str) -> str | None:
        card = self.get_current_card()
        if not card:
            return None
        if current_display_text == card['term']:
            return card['definition']
        else:
            return card['term']

    
    def get_all_cards(self):
        return self.cards