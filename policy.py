# TODO implement this class
import random
from abc import ABC, abstractmethod
import typing

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

# TODO maybe should make the random policy instead of random player?
# The player object is the state
class RandomPolicy(Policy):
   def __init__(self, player):
      super().__init__(player)

   @typing.override
   def select_action(self):
      return random.choice(self.actions)

   @typing.override
   def update_policy(self, player, action, reward, next_state):
      pass

class RLPolicy(Policy):
   def __init__(self, player):
      super().__init__(player)

   # TODO: implement this (epsilon greedy?)
   # maybe a neural network
   def select_action(self, state):
      pass

   # TODO: implement this (epsilon greedy?)
   def update_policy(self, state, action, reward, next_state):
      pass