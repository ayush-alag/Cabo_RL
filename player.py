import random

class Player():
   def __init__(self, name, policy):
      self.name = name
      self.hand = []
      self.policy = policy
      
      self.drawn_card = None
      self.called_cabo = False
      self.other_players = []
   
   def __str__(self):
      return self.name
      
   def draw(self):
      self.drawn_card = self.game_engine.deck.drawCard()
   
   def showHand(self, player):
      print(player)
      for card in player.hand:
         # only show value if it is known
         if self in card.players_that_know_card:
            card.show()
         else:
            print("Unknown")
   
   def showPlayerInfo(self):
      print("Player: {}".format(self.name))
      print("Hand:")
      self.showHand(self)
      print("Drawn Card:")
      if self.drawn_card:
         self.drawn_card.show()
      else:
         print("None")
      print("Called Cabo: {}".format(self.called_cabo))
      print("Other Players:")
      for player in self.other_players:
         self.showHand(player)
   
   def swapDrawnCard(self, index):
      self.hand.append(self.drawn_card)
      self.drawn_card = None
      discard_card = self.hand.pop(index)
      self.discardDrawnCard(discard_card)
         
   def discardDrawnCard(self):
      self.game_engine.discard_pile.discard(self.drawn_card)
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
      
   def decideAction(self):
      return self.policy.select_action()

   def canStack(self, top_card):
      if self.called_cabo:
         return False

      def checkStackPlayer(player):
         if player.called_cabo:
            return False
         for card in player.hand:
            # if the value is known, we can stack
            if self in card.players_that_know_card:
               if card.value == top_card.value:
                  return True
               
      # check all players including ourselves
      for player in self.other_players + [self]:
         if checkStackPlayer(player):
            return True
      return False
   
   def discardHandCard(self, card):
      assert card in self.hand
      self.hand.remove(card)
      self.game_engine.discard_pile.discard(card)
   
   def getPenaltyCard(self):
      self.hand.append(self.game_engine.deck.drawCard())
   
   def giveRandomCard(self, player):
      card = random.choice(self.hand)
      self.hand.remove(card)
      player.hand.append(card)
   
   # we get to stack
   def handle_stack(self, top_card):
      if self.called_cabo:
         return

      # a) Discard all cards that are ours that match the discarded card
      for card in self.hand:
         if self in card.players_that_know_card and card.value == top_card.value:
            self.hand.remove(card)
            self.discardHandCard(card)
            self.showHand(self)

      # b) Discard all cards that are other players' cards and 
      # give them one card from the deck in return + one of our cards
      for player in self.other_players:
         if player.called_cabo:
            continue

         for card in player.hand:
            if self in card.players_that_know_card and card.value == top_card.value:
               player.discardHandCard(card)
               player.getPenaltyCard()
               
               # TODO: should normally be able to decide which to give here but let's just do random
               self.giveRandomCard(player)
               self.showHand(self)
               self.showHand(player)
