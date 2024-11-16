import random

from deck import DiscardPile, Deck

class GameEngine:
   # TODO pass in players?
   def __init__(self, players):
      self.deck = Deck()
      self.discard_pile = DiscardPile()
      self.player_who_called_cabo = None
      self.initializePlayers()
      
   def initializePlayers(self):
      for player in self.players:
         self.addPlayer(player)
      
   def addPlayer(self, player):
      player.game_engine = self
      self.players.append(player)
                  
      for player in self.players:
         player.other_players = [p for p in self.players if p != player]
      
   # start with four cards
   def deal(self):
      for player in self.players:
         for _ in range(4):
            card = self.deck.drawCard()
            # we know this card
            card.player_knows_me(player)
            player.hand.append(card)
            
   def play(self):
      self.deck.shuffle()
      self.deal()
      
      # shuffle ordering of players, stick to this round robin order
      random.shuffle(self.players)

      # TODO: also limit this somewhat? 30 rounds?
      while not self.player_who_called_cabo:
         self.round(self.players[0], self.players[0])
      
      # the player who called cabo just went, do one more round starting with the next player until the player who called cabo
      cabo_index = self.players.index(self.player_who_called_cabo)
      next_player_index = (cabo_index + 1) % len(self.players)
      self.round(next_player_index, cabo_index)
      
      winner, score = self.determineWinner()
      print("Winner: {} with score: {}".format(winner, score))
      
      # TODO: do something with this information, maybe influence reward
   
   def check_and_handle_stack(self, top_card):
      stack_players = []
      for player in self.players:
         if player.canStack(top_card):
            stack_players.append(player)
      
      if len(stack_players) > 0:
         print("Stack!")
         for player in stack_players:
            print(player)
      
      # choose a random player to stack
      player = random.choice(stack_players)
      player.handle_stack(top_card)
   
   # need one more round after cabo is called
   def round(self, start_player, end_player):
      start_index = self.players.index(start_player)
      end_index = self.players.index(end_player)
      current_index = start_index
      
      while current_index != end_index:
         player = self.players[current_index]
         print("Player taking turn: {}".format(player))
         called_cabo = player.check_call_cabo()
         if called_cabo:
            self.player_who_called_cabo = player
            return
         
         player.draw(self.deck)
         player.showHand()
         action = player.decideAction()
         if action == "discard":
            player.discardDrawnCard(self.discard_pile)
         elif action.startswith("swap"):
            index = int(action.split(",")[1])
            player.swapDrawnCard(index)
         else:
            assert False, "Invalid action"
         # TODO: need to add powers maybe not in v1 though?
         
         top_card = self.discard_pile.top_of_discard()
         self.check_and_handle_stack(top_card)
         player.showHand()
         
         current_index = (current_index + 1) % len(self.players)

   # TODO maybe should print value for each player 
   def determineWinner(self):
      # player is the one with the lowest hand value;
      # if there's a tie, the one who called cabo wins
      lowest = float("inf")
      winner = None
      for player in self.players:
         hand_value = sum([card.value for card in player.hand])
         if hand_value < lowest:
            lowest = hand_value
            winner = player
         elif hand_value == lowest and player.called_cabo:
            winner = player
      
      return winner, lowest