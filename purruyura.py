#!/usr/bin/python
"""
Plays a game of blackjack between a single human player and the computer
controlled dealer
"""

from random import shuffle
import cmd

class Card:

    def __init__(self, suit, rank):
        '''
        Creates a card with the given suit and rank.  Ranks are values 
        between 1 and 13, inclusive, where 1 is an ace, 11 is a jack, 12 
        is a queen and 13 is a king.  Setting the rank will cause the 
        value to be set with standard Hearts card values
        
        >>> c = Card("Hearts", 12)
        >>> c.suit
        'Hearts'
        >>> c.rank
        12
        >>> c.value
        10
        >>> c = Card("Spades", 1)
        >>> c.suit
        'Spades'
        >>> c.rank
        1
        >>> c.value
        10
        >>> c = Card("Diamonds", 5)
        >>> c.suit
        'Diamonds'
        >>> c.rank
        5
        >>> c.value
        5
        '''
        self.suit = suit
        self.rank = rank
        if(self.rank > 1 and self.rank < 11):
            self.value = rank
        else:
            self.value = 10
        
    def __str__(self):
        '''
        Return the string representation of the card, substituting text
        for integer rank, where appropriate (for example, 11 maps to 
        Jack, and 1 maps to Ace)
        
        >>> c = Card("Hearts", 5)
        >>> str(c)
        '5 of Hearts'
        >>> c = Card("Spades", 1)
        >>> str(c)
        'Ace of Spades'
        >>> c = Card("Diamonds", 11)
        >>> str(c)
        'Jack of Diamonds'
        '''
        if (self.rank > 1 and self.rank < 11):
            return str(self.rank) + " of " + self.suit
        elif(self.rank == 1):
            return "Ace of " + self.suit
        elif(self.rank == 11):
            return "Jack of " + self.suit
        elif(self.rank == 12):
            return "Queen of " + self.suit
        elif(self.rank == 13):
            return "King of " + self.suit
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

class CardDeck:


    def __init__(self):     
        '''
        Creates an empty deck and discard list
        
        >>> cd = CardDeck()
        >>> cd.deck
        []
        >>> cd.discard
        []
        '''
        self.deck = []
        self.discard = []


    def _append_suit_to_deck(self, suit):
        '''
        Appends a standard western suit of cards (13 total cards, ranks
        1-13, numbers 2-10, trumps are Ace, Jack, Queen and King) to the
        deck.
        
        >>> cd = CardDeck()
        >>> cd._append_suit_to_deck("Spades")
        >>> len(cd.deck)
        13
        >>> cd.deck[0].rank
        1
        >>> cd.deck[12].rank
        13
        >>> cd.deck[7].suit
        'Spades'
        >>> str(cd.deck[7])
        '8 of Spades'
        '''
        for i in range(1,14):
            self.deck.append( Card(suit, i) )   


    def create_unshuffled_deck(self):
        '''
        Creates an unshuffled deck in the order Ace,1,2,...Queen,King 
        and by suit Diamonds, Spades, Hearts, Clubs
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> cd.deck[0].suit
        'Diamonds'
        >>> cd.deck[0].rank
        1
        >>> cd.deck[13].suit
        'Spades'
        >>> cd.deck[13].rank
        1
        >>> cd.deck[26].suit
        'Hearts'
        >>> cd.deck[30].rank
        5
        >>> cd.deck[39].suit
        'Clubs'
        >>> print(cd.deck[51])
        King of Clubs
        '''
        self._append_suit_to_deck("Diamonds")
        self._append_suit_to_deck("Spades")
        self._append_suit_to_deck("Hearts")
        self._append_suit_to_deck("Clubs")
    

    def shuffle_deck(self):
        '''
        Randomly arranges the cards in the deck
        '''
        shuffle(self.deck)

    def deal_card(self):
        '''
        Returns the top card popped off the deck
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> len(cd.deck)
        52
        >>> print(cd.deal_card())
        King of Clubs
        >>> len(cd.deck)
        51
        '''
        return self.deck.pop()
        
    def shuffle_in_discards(self):
        '''             
        Extends the deck with the discards and sets discard to an empty
        list, then suffles the deck
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> len(cd.deck)
        52
        >>> cd.discard.append(cd.deal_card())
        >>> len(cd.deck)
        51
        >>> cd.discard.append(cd.deal_card())
        >>> len(cd.deck)
        50
        >>> len(cd.discard)
        2
        >>> cd.shuffle_in_discards()
        >>> len(cd.deck)
        52
        >>> len(cd.discard)
        0
        '''
        self.deck.extend(self.discard)
        self.discard = []
        self.shuffle_deck()
        
    def __len__(self):
        '''
        Defines the length of a CardDeck as the length of its deck
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> len(cd.deck)
        52
        >>> cd.discard.append(cd.deal_card())
        >>> cd.discard.append(cd.deal_card())
        >>> len(cd.discard)
        2
        >>> len(cd.deck)
        50
        >>> len(cd)
        50
        '''
        return len(self.deck)

class Player:

    def __init__(self, deck):
        '''
        Creates a player with an empty hand, a score of zero and a 
        reference to a deck
        '''
        self.hand = []
        self.deck = deck
        self.score = 0

    
    def total_hand(self):
        '''
        Returns the total value of this player's hand, reducing the 
        value of Aces to 1, if the total value is over 21 until the 
        total value is less than or equal to 21
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> p = Player(cd)
        >>> p.hit()
        >>> p.hit()
        >>> p.total_hand()
        20
        '''
        result = 0      
        for card in self.hand:
            result += card.value
        if(result > 21):
            for card in self.hand:
                if card.rank == 1:
                    result -= 9
        return result   
    
    def hit(self):
        '''
        Deals the top card from this player's deck to this player's hand
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> p = Player(cd)
        >>> len(p.deck.deck)
        52
        >>> len(p.hand)
        0
        >>> p.hit()
        >>> len(p.hand)
        1
        >>> p.hit()
        >>> len(p.hand)
        2
        >>> len(p.deck.deck)
        50
        '''
        if len(self.deck)>0:
            self.hand.append(self.deck.deal_card())
        else:
            self.deck.shuffle_in_discards()
            self.hand.append(self.deck.deal_card())
            
    def discard(self):
        '''
        Adds this player's hand to the deck's discard list and sets this
        player's hand to an empty list
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> p = Player(cd)
        >>> p.hit()
        >>> p.hit()
        >>> len(p.hand)
        2
        >>> len(p.deck.discard)
        0
        >>> p.discard()
        >>> len(p.hand)
        0
        >>> len(p.deck.discard)
        2
        '''
        self.deck.discard.extend(self.hand)
        self.hand = []
    
    def print_friendly_hand(self):
        '''
        Returns a represenation of this player's hand that is pretty 
        printed
        
        >>> cd = CardDeck()
        >>> cd.create_unshuffled_deck()
        >>> p = Player(cd)
        >>> p.hit()
        >>> p.hit()
        >>> print(p.print_friendly_hand())
        King of Clubs, Queen of Clubs
        '''
        result = ""
        for card in self.hand:
            result += str(card) + ", " 
        return result[:-2]

class _BlackJackGame(cmd.Cmd):

    def __init__(self, **kwargs):
        '''
        Initiates a black jack game with one player and one dealer, 
        deals cards to both, displays the cards, and hands control to 
        the player.
        '''
        super(_BlackJackGame, self).__init__(**kwargs)
        self.cd = CardDeck()

        self.cd.create_unshuffled_deck()
        self.cd.shuffle_deck()

        self.p1 = Player(self.cd)
        self.p2 = Player(self.cd)
        self.start_game()
    
    def start_game(self):
        '''
        Starts a fresh game of blackjack
        '''
        self.p1.hit()
        self.p2.hit()
        self.p1.hit()
        self.p2.hit()
        
        print( "Dealer's hand")
        print( self.p1.print_friendly_hand() )
        print( "Total Val: " + str(self.p1.total_hand()) )
        print( "Player's hand")
        print( self.p2.print_friendly_hand() )
        print( "Total Val: " + str(self.p2.total_hand()) )

        self.playing = True
        self.quitting = False

    def do_hit(self, *args):
        '''
        Deals a card to player, re-totals player's hand
        '''
        self.quitting = False
        if(self.playing):
            self.p2.hit()
            if self.p2.total_hand() <=21:
                print("Player Hand: ")
                print( self.p2.print_friendly_hand() )
                print( "Total val: " + str(self.p2.total_hand()) )
            else:
                print("Player Hand: ")
                print( self.p2.print_friendly_hand() )
                print( "Total val: " + str(self.p2.total_hand()) )
                print("Player busted, another round?")
                self.p1.score += 1
                self.playing = False
        else:
            print("Start another game, yes/no?")

    def do_pass(self, line):
        '''
        Passes to the dealer, who will then play out their hand
        '''
        self.quitting = False
        while self.p1.total_hand() < 18:
            self.p1.hand.append(self.cd.deal_card())
        print( "Dealer's hand" )
        print( self.p1.print_friendly_hand())
        print( str(self.p1.total_hand()))
        print( "" )
        if self.p1.total_hand() > 21:
            if self.p2.total_hand() > 21:
                print( "Tie, both busted")
            else:
                print( "Player wins, dealer busted")
                self.p2.score += 1
        else:
            if self.p1.total_hand() >= self.p2.total_hand():
                print( "Dealer wins" )
                self.p1.score += 1
            elif self.p2.total_hand() <= 21:
                print( "Player wins" )
                self.p2.score += 1
            else:
                print( "Dealer Wins" )
                self.p1.score += 1
        self.playing = False
                
    def do_stand(self, line):
        '''
        Passes to the dealer, who will then play out their hand
        '''
        self.do_pass(line)
        
    def do_yes(self, line):
        '''
        Play another round of blackjack after being prompted, otherwise 
        do nothing
        '''
        self.quitting = False
        if not self.playing:
            self.playing = True
            self.p1.discard()
            self.p2.discard()
            self.p1.hand = []
            self.p2.hand = []
            self.start_game()
        else:
            print("\xbfQue?")
    def do_newHand(self, line):
        '''
        Play a fresh hand of blackjack, if you aren't in the middle of 
        one already
        '''
        return self.do_yes(line)
        
    def do_another(self, line):
        '''
        Play a fresh hand of blackjack, if you aren't in the middle of 
        one already
        '''
        return self.do_yes(line)
    
    def do_no(self, line):
        '''
        Exit, instead of playing another round of blackjack after being 
        prompted
        '''
        if not self.playing:
            print("Dealer score: " )
            print(str(self.p1.score))
            print("Player score: " )
            print(str(self.p2.score))
            return True
        elif self.quitting:
            print("Dealer score: " )
            print(str(self.p1.score))
            print("Player score: " )
            print(str(self.p2.score))
            return True
        else:
            self.quitting = True
            print("\xbfQue? Just one hand")
            
    def do_EOF(self, line):
        '''
        Quits this blackjack session
        '''
        return self.do_no(line)
        
    def do_quit(self, line):
        '''
        Quits this blackjack session
        '''
        return self.do_no(line)
        
    def do_exit(self, line):
        '''
        Quits this blackjack session
        '''
        return self.do_no(line)

    def postloop(self):
        '''
        Quits this blackjack session
        '''
        print( "" )

if __name__ == '__main__':
    _BlackJackGame().cmdloop() #actually plays the game
    
    #runs doctest, probably should comment out the game loop
    #import doctest
    #doctest.testmod() 
'''
Copyright (c) 2013 Gunnar Gissel <ggissel@alumni.cmu.edu>

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
