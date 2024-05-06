from __future__ import annotations
from typing import *
import random


class Card:
    def __init__(self, faceValue: str, typeValue: str, hidden: bool = False):
        self.faceValue = faceValue # A, 1, 2, ...
        self.typeValue = typeValue  # diamond, club, heart, spade
        self.hidden = hidden

    def hide(self) -> None:
        self.hidden = True

    def reveal(self) -> None:
        self.hidden = False

    @override
    def __str__(self):
        if self.hidden:
            return "?"
        return self.faceValue

class Deck:
    def __init__(self, cards: List[Card] = None) -> None:
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
        self.observers = []

    def addObserver(self, observer: Any) -> None:
        self.observers.append(observer)

    def notifyObservers(self) -> None:
        if self.isEmpty():
            for o in self.observers:
                o.deckEmpty()

    def insertCard(self, card: Card) -> None:
        self.cards.append(card)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def pop(self) -> Card:
        card = self.cards.pop()
        self.notifyObservers()
        return card

    def combine(self, deck: Deck) -> None:
        self.cards += deck.cards

    def insertHand(self, hand: 'Hand'):
        self.cards += hand.cards

    def empty(self) -> None:
        self.cards = []

    def isEmpty(self) -> bool:
        return len(self.cards) == 0

    @classmethod
    def createDecks(cls, numDecks: int) -> List[Card]:
        faceValues = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        typeValues = ['diamond', 'club', 'heart', 'spade']
        cards = []
        # Generate each deck
        for _ in range(numDecks):
            # Generate all cards for one deck
            for typeValue in typeValues:
                for faceValue in faceValues:
                    cards.append(Card(faceValue, typeValue))
        return cards
