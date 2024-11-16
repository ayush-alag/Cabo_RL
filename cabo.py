import random

from deck import DiscardPile, Deck

class GameEngine:
   # TODO pass in players?
   def __init__(self):
      self.deck = Deck()
      self.discard_pile = DiscardPile()
      self.players = []
      self.player_who_called_cabo = None
      
   def addPlayer(self, player):
      self.players.append(player)
      
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
            
      for player in self.players:
         player.other_players = [p for p in self.players if p != player]
      
      # shuffle ordering of players, stick to this round robin order
      random.shuffle(self.players)

      # TODO: also limit this somewhat? 30 rounds?
      while not self.player_who_called_cabo:
         self.round()
      
      # TODO one more round
      self.round()
      winner, score = self.determineWinner()
      # TODO: do something with this information, maybe influence reward
   
   def handle_stack(self, player):
      # a) Discard all cards that are ours that match the discarded card
      for card in player.hand:
         if self in card.players_that_know_card and card.value == player.drawn_card.value:
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
   
   def check_and_handle_stack(self):
      stack_players = []
      for player in self.players:
         if player.canStack():
            stack_players.append(player)
      
      if len(stack_players) > 0:
         print("Stack!")
         for player in stack_players:
            print(player)
      
      # choose a random player to stack
      player = random.choice(stack_players)
      self.handle_stack(player)
   
   # need one more round after cabo is called
   def round(self):
      for player in self.players:
         called_cabo = player.check_call_cabo()
         if called_cabo:
            self.player_who_called_cabo = player
            return True
         
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
         
         self.check_and_handle_stack()
         player.showHand()
                 
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