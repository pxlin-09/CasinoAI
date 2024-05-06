from __future__ import annotations
from abc import ABC, abstractmethod
from typing import *

from Deck import Card


class Hand(ABC):
    def __init__(self, cards: List[Card] = None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    @abstractmethod
    def value(self):
        pass

    def insertCard(self, card: Card) -> None:
        self.cards.append(card)

    def empty(self) -> None:
        self.cards = []

    def isEmpty(self) -> bool:
        return len(self.cards) == 0

    def revealCards(self) -> None:
        for c in self.cards:
            c.reveal()

    def display(self):
        for c in self.cards:
            print(c, end=' ')


class BlackjackHand(Hand):
    def __init__(self, cards: List[Card] = None) -> None:
        super().__init__(cards)

    def countAce(self):
        i = 0
        for c in self.cards:
            if c.faceValue == 'A':
                i+=1
        return i

    def value(self) -> int:
        total = 0
        aces = 0

        # Calculate the total, treating each Ace as 1 initially
        for card in self.cards:
            if card.faceValue in ['J', 'Q', 'K']:
                total += 10
            elif card.faceValue == 'A':
                aces += 1
                total += 1  # Assume Ace is 1 for now
            else:
                total += int(card.faceValue)

        # Adjust if we have Aces and it would be beneficial to treat them as 11
        # Only one Ace can be counted as 11 without busting (total over 21)
        while aces > 0 and total + 10 <= 21:
            total += 10  # Change one Ace from 1 to 11
            aces -= 1

        return total
