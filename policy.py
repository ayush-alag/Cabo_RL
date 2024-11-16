# TODO implement this class
import random
from abc import ABC, abstractmethod
import typing

# player object is the state
class Policy(ABC):
   def __init__(self, player):
      self.player = player
      self.actions = self.get_actions()
   
   def get_actions(self):
      actions = ["discard"]
      # append swap,index for each card in the hand
      for i in range(len(self.player.hand)):
         actions.append("swap,{}".format(i))
      return actions

   @abstractmethod
   def select_action(self, state):
      raise NotImplementedError("This method should be overridden by subclasses")

   @abstractmethod
   def update_policy(self, state, action, reward, next_state):
      raise NotImplementedError("This method should be overridden by subclasses")

class RandomPolicy(Policy):
   def __init__(self, player):
      super().__init__(player)

   @typing.override
   def select_action(self):
      return random.choice(self.actions)

   @typing.override
   # fixed policy
   def update_policy(self, player, action, reward, next_state):
      pass

class ExpertScoreMinimizer(Policy):
   def __init__(self, player):
      super().__init__(player)

   # doesn't take into account stack probability at all
   @typing.override
   def select_action(self):
      unknown_cards = [i for i, card in enumerate(self.player.hand) if self not in card.players_that_know_card]
      if unknown_cards:
         return "swap,{}".format(unknown_cards[0])
      
      # if all cards are known, swap with the lowest card
      max_card_in_hand = max(self.player.hand)
      if max_card_in_hand.value > self.drawn_card.value:
         max_card_index = self.player.hand.index(max(self.player.hand))
         return "swap,{}".format(max_card_index)
         
      # if drawn card is higher than all cards in hand, discard
      return "discard"

   # fixed policy
   @typing.override
   def update_policy(self, state, action, reward, next_state):
      pass

class RLPolicy(Policy):
   def __init__(self, player):
      super().__init__(player)

   # TODO: implement this (epsilon greedy?)
   # maybe a neural network  that takes the current state and outputs an action
   def select_action(self):
      pass

   # TODO: implement this (epsilon greedy?)
   def update_policy(self, state, action, reward, next_state):
      pass