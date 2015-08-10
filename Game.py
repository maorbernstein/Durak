import random
import AI
from Classes import *

def FindDefensePossibles(card_played,hand,trump):
    possibles = [Card(0,0)]
    if(card_played.suit == trump):
        for card in hand.cards:
            if((card.suit == trump) and (card.rank > card_played.rank)):
                possibles.append(card)
        return possibles
    else:
        for card in hand.cards:
            if(card.suit == trump):
                possibles.append(card)
            elif( (card.suit == card_played.suit) and (card.rank > card_played.rank)):
                possibles.append(card)
        return possibles

def FindAttackPossibles(inplay, hand):
    possibles = [Card(0,0)]
    ranks = []
    for card in inplay.attacks:
        if card.rank not in ranks:
            ranks.append(card.rank)
    for card in inplay.defenses:
        if card.rank not in ranks:
            ranks.append(card.rank)
    for card in hand.cards:
        if card.rank in ranks:
            possibles.append(card)
    return possibles

def Cleanup(game):
    game.discard.cards.extend(game.inplay.attacks)
    game.discard.cards.extend(game.inplay.defenses)
    game.inplay.clean()


def UserTurn(game):
    game.user_hand.skip = False
    print "User hand is:\n" + str(game.user_hand)
    num = input("Enter card number to play: ")
    card_played = game.user_hand.cards[num - 1]
    game.inplay.attacks.append(card_played)
    game.user_hand.cards.remove(card_played)
    print "Playing card " + str(card_played)

    while(True):
        # AI Defense Phase
        card_played = AI.Defense(FindDefensePossibles(card_played, game.ai_hand, game.trump))
        # Check if computer has given up. If so, they take all cards in the attack pile
        if(card_played == Card(0,0)):
            game.ai_hand.cards.extend(game.inplay.attacks)
            game.ai_hand.cards.extend(game.inplay.defenses)
            game.ai_hand.sort()
            game.inplay.clean()
            print "Computer takes cards"
            game.ai_hand.skip = True
            break
        game.inplay.defenses.append(card_played)
        game.ai_hand.cards.remove(card_played)
        print "Computer played " + str(card_played)
        # User Attack Phase
        if(len(game.inplay.attacks) == 6):
            game.ai_hand.skip = False
            break
        possibles = FindAttackPossibles(game.inplay, game.user_hand)
        i = 1
        for possible in possibles:
            string = "Option " + str(i) + ": "
            if(possible == Card(0,0)):
                string += "End turn"
            else:
                string += "Play " + str(possible)
            print string
        option = input("Select Option: ")
        card_played =  possibles[option - 1]
        if(card_played == Card(0,0)):
            "You chose to end this turn"
            game.ai_hand.skip = False
            break
        game.inplay.attacks.append(card_played)
        game.user_hand.cards.remove(card_played)
        print "You chose to play " + str(card_played)
    Cleanup(game)
    if(game.user_hand.skip == False):
        game.ai_hand.draw(game.deck,6)
    if(game.ai_hand.skip == False):
        game.ai_hand.draw(game.deck,6)


def AITurn(game):
    game.ai_hand.skip = False
    card_played = AI.FirstCard(game.ai_hand)
    game.ai_hand.cards.remove(card_played)
    game.inplay.attacks.append(card_played)
    print "Computer plays " + str(card_played)
    while(True):
        possibles = FindDefensePossibles(card_played,game.user_hand,game.trump)
        print "Options are:"
        i = 1
        for possible in possibles:
            string = "Option " + str(i)
            if(possible == Card(0,0)):
                string += "Take cards"
            else:
                string += "Play " + str(possible)
        option = input("Select Option")
        card_played = possibles[option]
        if(card_played == Card(0,0)):
            game.user_hand.cards.extend(game.inplay.attacks)
            game.user_hand.cards.extend(game.inplay.defenses)
            game.user_hand.sort()
            game.inplay.clean()
            game.user_hand.skip = True
            print "You took the cards"
            break
        game.inplay.defenses.append(card_played)
        game.user_hand.cards.remove(card_played)
        if(len(game.inplay.attacks) == 6):
            print "Reached maximum number of attacks"
            game.user_hand.skip = False
            break
        card_played = AI.NextCard(FindAttackPossibles(game.inplay,game.ai_hand))
        if(card_played == Card(0,0)):
            print "Computer chose to end the turn"
            game.user_hand.skip = False
            break
        print "Computer plays " + str(card_played)
    Cleanup(game)
    if(game.ai_hand.skip == False):
        game.ai_hand.draw(game.deck,6)
    if(game.user_hand.skip == False):
        game.ai_hand.draw(game.deck,6)


if __name__ == "__main__":
    game = Game()
    if(game.First):
        UserTurn(game)
    while(True):
        AITurn(game)
        UserTurn(game)
