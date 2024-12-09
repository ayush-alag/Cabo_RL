# TODO implement this class
import random
from abc import ABC, abstractmethod
from mcts import mcts

# player object is the state
class Policy(ABC):
   @abstractmethod
   def select_action(self, state):
      raise NotImplementedError("This method should be overridden by subclasses")

   @abstractmethod
   def update_policy(self, state, action, reward, next_state):
      raise NotImplementedError("This method should be overridden by subclasses")

class RandomPolicy(Policy):
   def select_action(self, player):
      actions = player.get_actions()
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

class MCTSPolicy(Policy):
   class GameState:
      def __init__(self, game_engine, current_player):
         self.game_engine = game_engine
         self.current_player = current_player

      def isTerminal(self):
         # return bool(self.game_engine.player_who_called_cabo)
         return self.game_engine.game_over

      def getReward(self):
         # Example: Reward is based on the final score of the current player
         return -self.current_player.expected_value(self.current_player)

      def getPossibleActions(self):
         # Get actions for the current player
         return self.current_player.get_actions()

      def takeAction(self, action):
         # Clone the game state
         current_player_index = None
         for i, player in enumerate(self.game_engine.players):
            if player == self.current_player:
               current_player_index = i

         # clones players, engine, discard pile, and then deck
         cloned_engine = self.game_engine.clone()
         cloned_current_player = cloned_engine.players[current_player_index]

         # Perform the action for the current player
         for player in cloned_engine.players:
            player.showHand(player)
         cloned_engine.handleAction(cloned_current_player, action)
         cloned_engine.check_and_handle_stack()

         # Simulate other players' turns
         next_player_index = (current_player_index + 1) % len(cloned_engine.players)
         while next_player_index != current_player_index:
            opponent = cloned_engine.players[next_player_index]
            cloned_engine.playerTurn(opponent)
            next_player_index = (next_player_index + 1) % len(cloned_engine.players)
         
         called_cabo = cloned_current_player.check_call_cabo()
         if called_cabo:
            self.game_engine.player_who_called_cabo = cloned_current_player
         if self.game_engine.player_who_called_cabo:
            cloned_engine.game_over = True
         cloned_current_player.draw()

         # Return the next game state
         return MCTSPolicy.GameState(cloned_engine, cloned_engine.players[next_player_index])

   def __init__(self, simulation_time=1000):
      self.simulation_time = simulation_time  # Time for MCTS simulations in milliseconds

   def select_action(self, player):
      initial_state = MCTSPolicy.GameState(player.game_engine, player)
      searcher = mcts(timeLimit=self.simulation_time)
      best_action = searcher.search(initial_state)
      return best_action

   def update_policy(self, state, action, reward, next_state):
      # MCTS is generally static
      pass