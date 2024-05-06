from __future__ import annotations
import time
from abc import ABC, abstractmethod
from typing import *

from Hand import BlackjackHand, Hand
from Deck import Deck
from Constants import Game, Action


BLACKJACK = 21
class CasinoGame(ABC):
    def __init__(self, players: List['Player'], deck: Deck, dealer: 'Player') -> None:
        self.players = players
        self.deck = deck
        deck.addObserver(self)
        self.dealer = dealer
        self.archiveDeck = Deck()
        self.isDisplay = True

    @abstractmethod
    def playGame(self):
        pass

    @abstractmethod
    def display(self):
        pass


class BlackjackGame(CasinoGame):
    def __init__(self, players: List['Player'], deck: Deck, dealer: 'Player') -> None:
        super().__init__(players, deck, dealer)
        self.gameCode = Game.BLACKJACK
        self.minBet = 25
        self.dealerCard = 0

    def playGame(self) -> None:
        self.startGame()

        # players make move
        for p in self.players:
            for h in p.hands:
                if h.value() >= BLACKJACK:
                    pass
                else:
                    self.playHand(p, h)

        dealerPlay = False
        for p in self.players:
            for h in p.hands:
                if h.value() < BLACKJACK:
                    dealerPlay = True

        # dealer make move
        for h in self.dealer.hands:
            h.revealCards()
        self.display()
        if dealerPlay:
            self.playHand(self.dealer, self.dealer.hands[0])
        dealerScore = self.dealer.hands[0].value()



        playerWin = False
        isDraw = False
        if dealerScore > BLACKJACK:
            playerWin = True
            for p in self.players:
                p.winnings = p.currentBet
        else:
            for p in self.players:
                for h in p.hands:
                    if h.value() == BLACKJACK:
                        playerWin = True
                        p.winnings = p.currentBet
                    elif BLACKJACK > h.value() > dealerScore:
                        playerWin = True
                        p.winnings = p.currentBet
                    elif h.value() == dealerScore:
                        isDraw = True
                        p.winnings = 0
                    else:
                        p.winnings = -p.currentBet

        if self.isDisplay:
            if not playerWin and not isDraw:
                print('dealer wins!')
            if playerWin:
                print('player wins!')
            if isDraw:
                print('draws!')

        self.endGame()


    def playHand(self, player: 'Player', hand: Hand):
        action = None
        while action != Action.STAND and hand.value() < 21:
            action = player.play(self.gameCode)
            if action is Action.HIT or action is Action.HIT_DOUBLE:
                hand.insertCard(self.deck.pop())
                self.display()
                if Action.HIT_DOUBLE:
                    if player.isAgent and self.isDisplay:
                        print("DOUBLE!")
                    player.currentBet *= 2
            if player == self.dealer:
                if self.isDisplay:
                    time.sleep(0.5)
            player.notifyAction(action)

    def resetDeck(self) -> None:
        self.deck.combine(self.archiveDeck)
        self.deck.shuffle()
        self.archiveDeck.empty()

    def startCountDown(self, countdown: int) -> None:
        if self.isDisplay:
            t = countdown
            for i in range(t):
                print(f'Starting in {countdown}')
                time.sleep(0.5)
                countdown -= 1

    def startGame(self) -> None:
        self.startCountDown(3)

        startingHand = 2
        self.dealer.hands = [BlackjackHand()]
        firstCard = 0
        for h in self.dealer.hands:
            firstCard = self.deck.pop()
            h.insertCard(firstCard)
            secondCard = self.deck.pop()
            secondCard.hide()
            h.insertCard(secondCard)

        for p in self.players:
            p.currentBet = self.minBet
            p.hands = [BlackjackHand()]
            for h in p.hands:
                for i in range(startingHand):
                    h.insertCard(self.deck.pop())

        for p in self.players:
            p.notifyStart(firstCard)

        if self.isDisplay:
            print("Starting Game")
        self.display()

    def endGame(self) -> None:
        for h in self.dealer.hands:
            self.archiveDeck.insertHand(h)
            h.empty()

        for p in self.players:
            for h in p.hands:
                self.archiveDeck.insertHand(h)
                h.empty()
            p.notifyEnd()

        if self.isDisplay:
            print("Game Ended")

    def deckEmpty(self) -> None:
        self.resetDeck()

    def display(self) -> None:
        if self.isDisplay:
            print('dealer: ', end='')
            for h in self.dealer.hands:
                h.display()
            print("")

            for p in self.players:
                if p.isAgent:
                    print('agent: ', end='')
                else:
                    print('player: ', end='')
                for h in p.hands:
                    print("(", end="")
                    h.display()
                    print(") ", end="")
                print("\t", end="")
            print("\n")



