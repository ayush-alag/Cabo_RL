from cabo_game_engine import GameEngine
from player import Player
from policy import RandomPolicy, ExpertScoreMinimizer, RLPolicy

def main():
   # add RL agent here
   players = [Player("random1", RandomPolicy),
              Player("random2", RandomPolicy),
              Player("expert", ExpertScoreMinimizer)]
   
   game = GameEngine(players)
   game.play()

if __name__ == "__main__":
   main()