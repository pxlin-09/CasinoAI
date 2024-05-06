import random
from typing import *

from CasinoGame import BlackjackGame
from Deck import Deck, Card
from Constants import Game, Action
import numpy as np

DEALER_SOFT_PUSH = 17

ACTIONS = [Action.HIT, Action.STAND, Action.HIT_DOUBLE]
HIT = 0
STAND = 1
HIT_DOUBLE = 2


class Player:
    def __init__(self, cash: int, isDealer: bool, isAgent: bool) -> None:
        self.bjActions = [HIT, STAND, HIT_DOUBLE]
        self.cash = cash
        self.isDealer = isDealer
        self.isAgent = isAgent
        self.hands = []
        self.playing = None
        self.currentBet = 0
        self.winnings = 0
        self.wins = 0
        self.draws = 0
        self.loss = 0

    def notifyStart(self, dealerCard: Card):
        pass

    def notifyAction(self, action: Action):
        pass

    def notifyEnd(self):
        pass
    def setBet(self, bet: int) -> None:
        self.currentBet = bet

    def play(self, gameCode: Game) -> Action:
        self.playing = gameCode
        if gameCode == Game.BLACKJACK:
            return self.playBlackjack()

    def playBlackjack(self) -> Action:
        if self.isDealer:
            h = self.hands[0]
            if h.value() < DEALER_SOFT_PUSH:
                return Action.HIT
            else:
                return Action.STAND

        elif not self.isAgent:
            while 1:
                act = input("h for Hit, s for stand: ")
                if act.lower() == 'h':
                    return Action.HIT
                if act.lower() == 's':
                    return Action.STAND


class BJPlayerAI(Player):
    def __init__(self) -> None:
        super().__init__(0, False, True)
        # ai stuff
        self.alpha = 0
        self.alpha_i = 0
        self.alpha_f = 0
        self.num_ep = 0
        self.epsilon = 0
        self.discount = 0
        self.q_vals = np.zeros((11, 21, 31, 3))
        self.dealerCards = []
        self.old_state = ()
        self.old_action = ()
        self.cur_state = ()

    def configAgent(self, alpha_i: float, alpha_f: float, num_ep: int, epsilon: float,
                    discount: float):
        self.alpha = alpha_i
        self.alpha_i = alpha_i
        self.alpha_f = alpha_f
        self.num_ep = num_ep
        self.epsilon = epsilon
        self.discount = discount
        self.isAgent = True

    def BJState(self):
        def getValue():
            face = ['A', 'J', 'Q', 'K']
            faceValue = self.dealerCards[0].faceValue
            if faceValue not in face:
                v = int(faceValue)
            elif faceValue == 'A':
                v = 1
            else:
                v = 10
            return v

        dealerValue = getValue()
        aces = self.hands[0].countAce()
        handValue = self.hands[0].value()
        return (dealerValue, aces, handValue)

    @override
    def notifyStart(self, dealerCard: Card):
        self.dealerCards = [dealerCard]
        self.cur_state = self.BJState()

    @override
    def notifyAction(self, action: Action):
        self.old_state = self.cur_state
        self.old_action = ACTIONS.index(action)
        self.update_q(self.old_state, self.cur_state, self.old_action, 0)

    @override
    def notifyEnd(self):
        if self.winnings > 0:
            self.wins += 1
        elif self.winnings < 0:
            self.loss += 1
        else:
            self.draws += 1

    def select_action(self, state) -> int:
        if random.random() < self.epsilon:
            return random.choice(self.bjActions)
        else:  # randomly break ties
            max_val = np.max(self.q_vals[state])
            max_idx = np.where(self.q_vals[state] == max_val)[0]
            return random.choice(max_idx)

    def update_q(self, old_state, new_state, action, reward):
        self.q_vals[old_state][action] = ((1 - self.alpha) * self.q_vals[old_state][action] + self.alpha * (
                reward + self.discount * np.max(self.q_vals[new_state])))

    def trainBJ(self):
        self.loss = 0

        self.wins = 0
        self.draws = 0

        dealer1 = Player(0, True, False)
        cards = Deck.createDecks(8)
        deck = Deck(cards)
        BJ = BlackjackGame([self], deck, dealer1)
        BJ.isDisplay = False
        for i in range(self.num_ep):
            self.winnings = 0
            BJ.playGame()
            reward = self.winnings * self.discount ** i
            self.update_q(self.old_state, self.cur_state, self.old_action, reward)
            self.alpha -= (self.alpha_i - self.alpha_f) / self.num_ep
        print(f'won:{self.wins}, lost:{self.loss}, tied:{self.draws}')
        np.save('q_val.npy', self.q_vals)

    @override
    def playBlackjack(self) -> Action:
        return ACTIONS[self.select_action(self.cur_state)]
