import random
import pygame
from Dictionaries import *
import os

image_library = {}

def get_image(path):
    global image_library
    image = image_library.get(path)
    if(image == None):
        clean_path = path.replace('/',os.sep).replace('\\',os.sep)
        image = pygame.image.load(clean_path)
        image_library[path] = image
    return image

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

class GameView:
    def __init__(self, trump):
        pygame.init()
        self.blank_path = "Card_gifs/b2fv.gif"
        self.start_button_path = "Card_gifs/start_button.jpg"
        self.start_button_mo_path = "Card_gifs/start_button_mo.jpg"
        self.trump = trump
        self.cardwidth = 71
        self.cardheight = 96
        self.width = 1024/3*2
        self.height = 768/3*2
        self.margin = 25
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0,0,0))
        self.screen.blit(get_image(self.start_button_path), (self.width/2, self.height/2))

    def Update(self, hand, inplay):
        global image_library
        self.screen.fill((0,0,0))

        i = 0
        for card in hand.cards:
            path = Card_to_Path[ (card.suit, card.rank) ]
            self.screen.blit(get_image(path), (self.margin*(1 + i) + self.cardwidth*i ,self.height - self.margin - self.cardheight) )
            i += 1

        i = 0
        for card in inplay.attacks:
            path = Card_to_Path[(card.suit, card.rank)]
            self.screen.blit(get_image(path), (self.margin*(1 + i) + self.cardwidth*i, self.margin) )
            i += 1

        i = 0
        for card in inplay.defenses:
            path = Card_to_Path[ (card.suit, card.rank) ]
            self.screen.blit(get_image(path) , (self.margin*(1 + i) + self.cardwidth*(i + .5), self.cardwidth*i + .5*self.cardheight ) )
            i += 1

        path = Card_to_Path[ (self.trump.suit, self.trump.rank) ]
        image = pygame.transform.rotate( get_image(path), -90)
        self.screen.blit(image, (self.width - self.cardheight - self.margin, self.cardwidth + self.margin))
        image = get_image(self.blank_path)
        self.screen.blit(image, (self.width - self.cardheight - self.cardwidth/4 - self.margin - 10,  -10 + self.cardwidth + self.margin))
        pygame.display.flip()

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
        trump_card = self.deck.trump()
        self.gameview = GameView(trump_card)
        self.trump_suit = trump_card.suit
        self.gameview.Update(self.user_hand, self.inplay)
        ai_lowest = 100
        for card in self.ai_hand.cards:
            if(card.suit == self.trump_suit):
                ai_lowest = min(ai_lowest,card.rank)
        user_lowest = 100
        for card in self.user_hand.cards:
            if(card.suit == self.trump_suit):
                user_lowest = min(user_lowest,card.rank)
        self.First = user_lowest > ai_lowest