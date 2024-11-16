import random

# let's build out the value known part
class Card:
   def __init__(self, suit, value):
      self.suit = suit
      self.value = value
      self.is_value_known = True

   def show(self):
      print("{} of {}".format(self.value, self.suit))
      
class Deck:
   def __init__(self):
      self.cards = []
      self.build()

   def build(self):
      for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
         for v in range(1, 14):
            self.cards.append(Card(s, v))

   def show(self):
      for c in self.cards:
         c.show()

   def shuffle(self):
      for i in range(len(self.cards) - 1, 0, -1):
         r = random.randint(0, i)
         self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

   def drawCard(self):
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

# todo: this player needs a policy
class Player:
   def __init__(self, name):
      self.name = name
      self.hand = []
      self.drawn_card = None
      self.called_cabo = False
      # tuples of (player, card)
      self.known_player_cards = []
   
   def __str__(self):
      return self.name
      
   def draw(self, deck):
      self.drawn_card = deck.drawCard()
      return self
      
   def showHand(self):
      for card in self.hand:
         # only show value if it is known
         if card.is_value_known:
            card.show()
         else:
            print("Unknown")
   
   def swapDrawnCard(self, index):
      self.hand.append(self.drawn_card)
      self.drawn_card = None
      discard_card = self.hand.pop(index)
      self.discardDrawnCard(discard_card)
         
   def discardDrawnCard(self, discard_pile):
      discard_pile.discard(self.drawn_card)
      self.drawn_card = None
      
   # TODO: fill this out
   def should_call_cabo(self):
      pass
      
   # TODO fill this out
   def decideAction(self):
      pass
      
   # probably need to do more here
   def callCabo(self):
      self.called_cabo = True
   
   def score(self):
      # sum up cards in hand
      total = 0
      for card in self.hand:
         total += card.value
      return total
   
   # TODO: better way of representing player
   def checkStack(self):
      # check if the top of the discard pile is a card in the hand
      top = self.discard_pile.top_of_discard()
      for card in self.hand:
         if card.value == top.value:
            return True, "me"

      # also check other players cards
      for player, card in self.known_player_cards:
         if card.value == top.value:
            return True, player
      return False

class GameEngine:
   def __init__(self):
      self.deck = Deck()
      self.discard_pile = DiscardPile()
      self.players = []
      
   def addPlayer(self, player):
      self.players.append(player)
      
   # start with four cards
   def deal(self):
      for player in self.players:
         for i in range(4):
            player.hand.append(self.deck.drawCard())
            
   def play(self):
      self.deck.shuffle()
      self.deal()
      cabo_called = False
      while not cabo_called:
         cabo_called = self.round()
   
   def handle_stack(self, player):
      # a) Discard all cards that are ours that match the discarded card
      for card in player.hand:
         if card.is_value_known and card.value == player.drawn_card.value:
            player.hand.remove(card)
            player.discardDrawnCard(self.discard_pile)

      # b) Discard all cards that are other players' cards and give them one card from the deck in return + one of our cards
      for known_player, known_card in player.known_player_cards:
         if known_card.value == player.drawn_card.value:
            player.known_player_cards.remove((known_player, known_card))
            new_card = self.deck.drawCard()
            known_player.hand.append(new_card)
            # choose a random card from our hand and give it to the player
            random_card = random.choice(player.hand)
            player.hand.remove(random_card)
            known_player.hand.append(random_card)
            # add this to the known cards
            if random_card.is_value_known:
               player.known_player_cards.append((known_player, random_card))
   
   # need one more round after cabo is called
   def round(self):
      for player in self.players:
         should_call_cabo = player.should_call_cabo()
         if should_call_cabo:
            player.callCabo()
            return True
         
         player.draw(self.deck)
         player.showHand()
         action = player.decideAction()
         if action == "discard":
            player.discardDrawnCard(self.discard_pile)
         elif action.startswith("swap"):
            index = int(action.split(",")[1])
            player.swapDrawnCard(index)
         
         stack_players = []
         for player in self.players:
            stack, player = player.checkStack()
            if stack:
               stack_players.append(player)
         
         if len(stack_players) > 0:
            print("Stack!!")
            for player in stack_players:
               print(player)
            break
         
         # choose a random player to stack
         player = random.choice(self.players)
         self.handle_stack(player)
         
         player.swapDrawnCard(0)
         player.showHand()