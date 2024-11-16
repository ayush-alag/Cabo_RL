import random

# let's build out the value known part
class Card:
   def __init__(self, suit, nominal_value):
      self.suit = suit
      self.nominal_value = nominal_value
      self.value = self.get_value()
      self.players_that_know_card = []

   def show(self):
      print("{} of {}".format(self.value, self.suit))
   
   def get_king_value(self):
      # if its a black king, it is worth 13, otherwise -1
      if self.nominal_value == "King" and self.suit in ["Spades", "Clubs"]:
         return 13
      else:
         return -1
      
   def get_value(self):
      # convert face cards to values
      if self.nominal_value == "Jack":
         return 11
      elif self.nominal_value == "Queen":
         return 12
      elif self.nominal_value == "King":
         return self.get_king_value()
      elif self.nominal_value == "Ace":
         return 1
      else:
         return self.nominal_value
   
   def player_knows_me(self, player):
      self.players_that_know_card.append(player)
      
class Deck:
   def __init__(self):
      self.cards = []
      self.build()

   def build(self):
      for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
         self.cards.append(Card(s, "Ace"))
         for v in range(2, 10):
            self.cards.append(Card(s, v))
         for v in ["Jack", "Queen", "King"]:
            self.cards.append(Card(s, v))

   def show(self):
      for c in self.cards:
         c.show()

   def shuffle(self):
      for i in range(len(self.cards) - 1, 0, -1):
         r = random.randint(0, i)
         self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

   def drawCard(self):
      # if the deck is empty, we need to reshuffle the discard pile
      if len(self.cards) == 0:
         top = self.discard_pile.top_of_discard()
         self.cards = self.discard_pile.cards[:-1]
         self.discard_pile.cards = [top]
         self.shuffle()
         
      return self.cards.pop()
   
class DiscardPile:
   def __init__(self):
      self.cards = []
      
   def show(self):
      for c in self.cards:
         c.show()
      
   def discard(self, card):
      self.cards.append(card)
      
   def top_of_discard(self):
      return self.cards[-1]