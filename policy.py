# TODO implement this class
import random
from abc import ABC, abstractmethod

# player object is the state
class Policy(ABC):
   def get_actions(self, player):
      actions = ["discard"]
      # append swap,index for each card in the hand
      for i in range(len(player.hand)):
         actions.append("swap,{}".format(i))
      return actions

   @abstractmethod
   def select_action(self, state):
      raise NotImplementedError("This method should be overridden by subclasses")

   @abstractmethod
   def update_policy(self, state, action, reward, next_state):
      raise NotImplementedError("This method should be overridden by subclasses")

class RandomPolicy(Policy):
   def select_action(self, player):
      actions = self.get_actions(self, player)
      return random.choice(actions)

   # fixed policy
   def update_policy(self, player, action, reward, next_state):
      pass

class ExpertScoreMinimizer(Policy):
   # doesn't take into account stack probability at all
   def select_action(self, player):
      unknown_cards = [i for i, card in enumerate(player.hand) if player not in card.players_that_know_card]
      if unknown_cards:
         return "swap,{}".format(unknown_cards[0])
      
      if len(player.hand) == 0:
         return "discard"
      
      # if all cards are known, swap with the highest card
      max_card_in_hand = max(player.hand, key=lambda card: card.value)
      if max_card_in_hand.value > player.drawn_card.value:
         max_card_index = player.hand.index(max_card_in_hand)
         return "swap,{}".format(max_card_index)
         
      # if drawn card is higher than all cards in hand, discard
      return "discard"

   # fixed policy
   def update_policy(self, state, action, reward, next_state):
      pass

class Holder(Policy):
   def select_action(self, player):
      unknown_cards = [i for i, card in enumerate(player.hand) if player not in card.players_that_know_card]
      if unknown_cards:
         return "swap,{}".format(unknown_cards[0])
      
      if len(player.hand) == 0:
         return "discard"
      
      # if card is greater than 7 hold it
      bad_card_values = [3, 4, 5, 6]
      if player.drawn_card.value in bad_card_values:
         return "discard"

      swap_idx = None
      for bad_card in bad_card_values:
         for i, card in enumerate(player.hand):
            if card.value == bad_card:
               swap_idx = i
               continue

      if swap_idx:
         return "swap,{}".format(swap_idx)

      # at this point, the drawn card is not a bad card and we don't have any bad cards in system
      # move towards the extremes
      if player.drawn_card.value < 3:
         max_low_card = -1
         for i, card in enumerate(player.hand):
            if card.value < 3 and card.value > max_low_card:
               swap_idx = i

      if player.drawn_card.value > 6:
         min_high_card = 10000
         for i, card in enumerate(player.hand):
            if card.value > 6 and card.value < min_high_card:
               swap_idx = i

      if swap_idx:
         return "swap,{}".format(swap_idx)
      
      return "discard"

   # fixed policy
   def update_policy(self, state, action, reward, next_state):
      pass

class RLPolicy(Policy):
   # TODO: implement this (epsilon greedy?)
   # maybe a neural network  that takes the current state and outputs an action
   def select_action(self, player):
      pass

   # TODO: implement this (epsilon greedy?)
   def update_policy(self, state, action, reward, next_state):
      pass