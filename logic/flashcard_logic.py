class FlashcardLogic:
    def __init__(self) -> None:
        self.cards: list[dict[str, str]] = []
        self.current_index: int = 0

    def add_card(self, term: str, definition: str) -> bool:
        if term.strip() and definition.strip():
            self.cards.append({'term': term, 'definition': definition})
            return True
        return False

    def get_current_card(self) -> dict[str, str] | None:
        if not self.cards:
            return None
        return self.cards[self.current_index]

    def next_card(self) -> None:
        if self.cards:
            self.current_index = (self.current_index + 1) % len(self.cards)