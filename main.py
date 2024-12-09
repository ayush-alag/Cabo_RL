from collections import defaultdict
from cabo_game_engine import GameEngine
from player import Player
from policy import MCTSPolicy, RandomPolicy, ExpertScoreMinimizer, Holder
from deck import Card

def full_game_sim():# Example setup
   # add RL agent here
   # players = [Player("random1", RandomPolicy),
   #            Player("random2", RandomPolicy),
   #            Player("expert", ExpertScoreMinimizer)]
   # players = [Player("high latency", ExpertScoreMinimizer, stack_level=2),
   #            Player("medium latency", ExpertScoreMinimizer, stack_level=5),
   #            Player("low latency", ExpertScoreMinimizer, stack_level=8),
   #            Player("very low latency", ExpertScoreMinimizer, stack_level=11)]
   # players = [Player("first_player", ExpertScoreMinimizer),
   #            Player("second_player", ExpertScoreMinimizer),
   #            Player("third_player", ExpertScoreMinimizer),
   #            Player("fourth_player", ExpertScoreMinimizer),
   #            Player("fifth_player", ExpertScoreMinimizer),
   #            Player("sixth_player", ExpertScoreMinimizer),
   #            Player("seventh_player", ExpertScoreMinimizer),
   #            Player("eighth_player", ExpertScoreMinimizer)]
   players = [Player("first_player", RandomPolicy()),
              Player("second_player", RandomPolicy()),
              Player("third_player", RandomPolicy()),
              Player("mcts", MCTSPolicy())]
   # players = [Player("first_player", RandomPolicy),
   #            Player("second_player", Holder),
   #            Player("third_player", Holder),
   #            Player("fourth_player", Holder)]
   
   game = GameEngine(players)
   end_state_players = game.play()
            
   print("\nGame Over!\n")
   # TODO: do something with this information, maybe influence reward
   winner, score = determineWinner(end_state_players)
   print_scores(winner, score, end_state_players)
   player_to_score = {player: sum([card.value for card in player.hand]) for player in end_state_players}
   return winner, player_to_score

def run_simulations(num_simulations=1):
   winner_counts = defaultdict(int)
   total_score = defaultdict(int)
   
   for _ in range(num_simulations):
      winner, player_to_score = full_game_sim()
      winner_counts[winner.name] += 1
      for player, score in player_to_score.items():
         total_score[player.name] += score
   
   average_score = {player: score / num_simulations for player, score in total_score.items()}
   print("\nAverage Score: {}".format(average_score))
   print("Winner Counts: {}".format(winner_counts))

def print_scores(winner, score, end_state_players):
   print("Winner: {} with score: {}".format(winner.name, score))
   winner.showHand(winner)
   for player in end_state_players:
      if player != winner:
         score = sum([card.value for card in player.hand])
         print("Player: {} with score: {}".format(player.name, score))
         player.showHand(player)
   
# TODO maybe should print value for each player 
def determineWinner(end_state_players):
   # player is the one with the lowest hand value;
   # if there's a tie, the one who called cabo wins
   lowest = float("inf")
   winner = None
   for player in end_state_players:
      hand_value = sum([card.value for card in player.hand])
      if hand_value < lowest:
         lowest = hand_value
         winner = player
      elif hand_value == lowest and player.called_cabo:
         winner = player
   
   return winner, lowest

if __name__ == "__main__":
   run_simulations()