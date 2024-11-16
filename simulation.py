# TODO make a simulation engine that can run multiple games
class SimulationEngine:
   def __init__(self, policy, game_engine):
      self.policy = policy
      self.game_engine = game_engine

   # TODO definitely need to populate this and get the sarsa pairs or whatever
   def run_simulation(self, num_games):
      for _ in range(num_games):
         game_state = self.game_engine.play()
         # update policy of all players in the game engine
         for player in self.game_engine.players:
            player.policy.update_policy(game_state)