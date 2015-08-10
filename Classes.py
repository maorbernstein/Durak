import random
class Card:
    suits = ["Clubs","Diamonds","Hearts","Spades"]
    ranks = [None,None,"2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.ranks[self.rank] + " of " + self.suits[self.suit]

    def __cmp__(self,other):
        return cmp(self.rank,other.rank)

class Deck:
    def __init__(self):
        self.cards = []
        for i in range(4):
            for j in range(2,15):
                self.cards.append(Card(i,j))
    def __str__(self):
        string = ""
        for card in self.cards:
            string += str(card) + "\n"
        return string
    def pop(self):
        return self.cards.pop()
    def trump(self):
        card = self.cards.pop()
        self.cards.insert(0,card)
        return card

    def shuffle(self):
        random.shuffle(self.cards)

class Hand:
    def __init__(self):
        self.cards = []
        self.skip = False
    # Assumes deck is already shuffled
    def __str__(self):
        string = ""
        i = 1
        for card in self.cards:
            string += "Card " + str(i) + ":" + str(card) + "\n"
            i += 1
        return string
    def draw(self,deck,num):
        num_in_hand = len(self.cards)
        for i in range(num - num_in_hand):
            if(len(deck.cards) > 0):
                self.cards.append(deck.pop())
            else:
                break
    def sort(self):
        self.cards.sort()

class Discard:
    def __init__(self):
        self.cards = []

class InPlay:
    def __init__(self):
        self.attacks = []
        self.defenses = []
    def clean(self):
        self.attacks = []
        self.defenses = []

class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.shuffle()
        self.discard = Discard()
        self.inplay = InPlay()
        self.user_hand = Hand()
        self.user_hand.draw(self.deck,6)
        self.user_hand.sort()
        self.ai_hand = Hand()
        self.ai_hand.draw(self.deck,6)
        self.ai_hand.sort()
        card = self.deck.trump()
        self.trump = card.suit
        print "The trump is " + card.suits[self.trump]
        ai_lowest = 100
        for card in self.ai_hand.cards:
            if(card.suit == self.trump):
                ai_lowest = min(ai_lowest,card.rank)
        user_lowest = 100
        for card in self.user_hand.cards:
            if(card.suit == self.trump):
                user_lowest = min(user_lowest,card.rank)
        self.First = user_lowest > ai_lowest
