# This is a sample Python script.
from CasinoGame import BlackjackGame
from Deck import Deck
from Player import Player, BJPlayerAI


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    discount = 1
    epsilon = 0.3
    ep = 1000000
    alpha_init = 0.9
    alpha_final = 0.01

    dealer1 = Player(0, True, False)
    a1 = BJPlayerAI()
    a1.configAgent(alpha_init, alpha_final, ep, epsilon, discount)
    cards = Deck.createDecks(8)
    deck = Deck(cards)
    a1.trainBJ()
    ep=1000
    a1.configAgent(0, 0, ep, 0, 0)
    a1.trainBJ()
    p1 = Player(100, False, False)
    BJ = BlackjackGame([a1], deck, dealer1)


    for i in range(15):
        BJ.playGame()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
