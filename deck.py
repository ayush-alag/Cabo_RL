import random

# let's build out the value known part
class Card:
   def __init__(self, suit, nominal_value):
      self.suit = suit
      self.nominal_value = nominal_value
      self.value = self.get_value()
      self.players_that_know_card = []

   def __str__(self):
      return f"{self.nominal_value} of {self.suit}"
   
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

   def clone(self):
      card = Card(self.suit, self.nominal_value)
      card.value = self.value
      card.players_that_know_card = self.players_that_know_card
      # must set players that know card outside
      return card
      
class Deck:
   def __init__(self, discard_pile):
      self.cards = []
      self.discard_pile = discard_pile
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

   def clone(self, discard_pile):
      cloned_deck = Deck(discard_pile)
      for card in self.cards:
         cloned_deck.cards.append(card.copy())
      return cloned_deck
   
class DiscardPile:
   def __init__(self):
      self.cards = []
      
   def show(self):
      for c in self.cards:
         c.show()
      
   def discard(self, card):
      print("Discarding: {}".format(card))
      self.cards.append(card)
      
   def top_of_discard(self):
      return self.cards[-1]

   def clone(self):
      cloned_pile = DiscardPile()
      for card in self.cards:
         cloned_pile.cards.append(card.copy())
      return cloned_pile