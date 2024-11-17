import random

from deck import DiscardPile, Deck

class GameEngine:
   # TODO pass in players?
   def __init__(self, players):
      self.discard_pile = DiscardPile()
      self.deck = Deck(self.discard_pile)
      self.player_who_called_cabo = None
      self.initializePlayers(players)
      
   def initializePlayers(self, players):
      self.players = []
      for player in players:
         self.players.append(player)
         player.game_engine = self

      for player in self.players:
         player.other_players = [p for p in self.players if p != player]
      
   # start with four cards
   def deal(self):
      for player in self.players:
         for i in range(4):
            card = self.deck.drawCard()
            player.hand.append(card)
            # we know two out of four cards
            if i < 2:
               card.player_knows_me(player)
            
   def play(self):
      self.deck.shuffle()
      self.deal()
               
      random.shuffle(self.players)
      
      # shuffle ordering of players, stick to this round robin order
      print("Ordering of players: " + ", ".join([player.name for player in self.players]))

      # TODO: also limit this somewhat? 30 rounds?
      round_idx = 1
      while not self.player_who_called_cabo:
         print("\nRound: {}".format(round_idx))
         self.round(0, len(self.players) - 1)
         round_idx += 1
         
      print("\nCABO CALLED BY {}!\n".format(self.player_who_called_cabo))
      
      # the player who called cabo just went, do one more round starting with the next player until the player who called cabo
      cabo_index = self.players.index(self.player_who_called_cabo)
      next_player_index = (cabo_index + 1) % len(self.players)
      previous_cabo_player = (cabo_index - 1) % len(self.players)
      self.round(next_player_index, previous_cabo_player)
      
      return self.players
   
   def check_and_handle_stack(self, top_card):
      stack_players = []
      for player in self.players:
         if player.canStack(top_card):
            stack_players.append(player)
      
      if len(stack_players) > 0:
         print("Stack! Contesting players: " + " ".join([player.name for player in stack_players]))
         
         # choose a random player to stack
         player = random.choice(stack_players)
         player.handle_stack(top_card)
   
   def playerTurn(self, player):
      print("Player taking turn: {}".format(player))
      called_cabo = player.check_call_cabo()
      if called_cabo:
         self.player_who_called_cabo = player
         return True
         
      player.draw()
      player.showHand(player)
      action = player.decideAction()
      if action == "discard":
         print("Discarding drawn card")
         player.discardDrawnCard()
      elif action.startswith("swap"):
         index = int(action.split(",")[1])
         print("Swapping card at index: {}".format(index))
         player.swapDrawnCard(index)
      else:
         assert False, "Invalid action"
      player.showHand(player)
      
      # handle stack
      top_card = self.discard_pile.top_of_discard()
      self.check_and_handle_stack(top_card)
      
      return False
   
   # start to end player (inclusive)
   def round(self, start_index, end_index):
      current_index = start_index
      while current_index != end_index:
         called_cabo = self.playerTurn(self.players[current_index])
         if called_cabo:
            return
         
         current_index = (current_index + 1) % len(self.players)
      
      # once more for end index
      self.playerTurn(self.players[current_index])