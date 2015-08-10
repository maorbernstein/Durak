from Classes import *

class FakeDeck:
    def __init__(self):
        self.cards = []
        for i in range(4):
            for j in range(2,15):
                self.cards.append(Card(i,j))
    def remove(self,card):
        self.cards.remove(card)

# Calculates the ideal first card to play
def FirstCard(hand):
    return hand.cards[0]

def NextCard(possibles):
    if(len(possibles) > 1):
        return possibles[1]
    else:
        return possibles[0]

def Defense(possibles):
    if(len(possibles) > 1):
        return possibles[1]
    else:
        return possibles[0]
