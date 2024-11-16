import random
from abc import ABC, abstractmethod
import typing

class Player(ABC):
   def __init__(self, name):
      self.name = name
      self.hand = []
      self.drawn_card = None
      self.called_cabo = False
      self.other_players = []
   
   def __str__(self):
      return self.name
      
   def draw(self, deck):
      self.drawn_card = deck.drawCard()
   
   def showPlayerInfo(self):
      def showHand(self, player):
         for card in player.hand:
            # only show value if it is known
            if self in card.players_that_know_card:
               card.show()
            else:
               print("Unknown")
               
      print("Player: {}".format(self.name))
      print("Hand:")
      showHand(self)
      print("Drawn Card:")
      if self.drawn_card:
         self.drawn_card.show()
      else:
         print("None")
      print("Called Cabo: {}".format(self.called_cabo))
      print("Other Players:")
      for player in self.other_players:
         showHand(player)
   
   def swapDrawnCard(self, index):
      self.hand.append(self.drawn_card)
      self.drawn_card = None
      discard_card = self.hand.pop(index)
      self.discardDrawnCard(discard_card)
         
   def discardDrawnCard(self, discard_pile):
      discard_pile.discard(self.drawn_card)
      self.drawn_card = None
   
   # hardcoding this for simplicity
   def check_call_cabo(self):
      def expected_value(player):
         ev = 0
         for card in player.hand:
            if self in card.players_that_know_card:
               ev += card.value
            else:
               # doesn't take into account known cards' probabilities but that's fine for now
               ev += 6.5
               
         return ev
      
      my_ev = expected_value(self)
      for player in self.other_players:   
         if expected_value(player) < my_ev:
            return False
         
      # can only call cabo if have less than 2 cards or score <= 3
      # prevents calling cabo too early (JZ move)
      if len(self.hand) > 2 or my_ev > 3:
         return False

      self.called_cabo = True
      return True
      
   @abstractmethod
   def decideAction(self):
      raise NotImplementedError("This method should be overridden by subclasses")

   def canStack(self):
      def checkStackPlayer(player, topCard):
         for card in player.hand:
            # if the value is known, we can stack
            if self in card.players_that_know_card:
               if card.value == topCard.value:
                  return True
               
      # check all players including ourselves
      top = self.discard_pile.top_of_discard()
      for player in self.other_players + [self]:
         if checkStackPlayer(player, top):
            return True
      return False
   
# player should be an abstract class. make RandomPlayer and PolicyPlayer subclasses
class RandomPlayer(Player):
   @typing.override
   def decideAction(self):
      actions = ["discard"]
      # append swap,index for each card in the hand
      for i in range(len(self.hand)):
         actions.append("swap,{}".format(i))
      return random.choice(actions)

# TODO define policy
class PolicyPlayer(Player):
   def __init__(self, name, policy):
      super().__init__(name)
      self.policy = policy

   @typing.override
   def decideAction(self):
      return self.policy.decideAction(self)