# TODO implement this class
class Policy:
   def __init__(self, actions):
      self.actions = actions

   def select_action(self, state):
      raise NotImplementedError("This method should be overridden by subclasses")

   def update_policy(self, state, action, reward, next_state):
      raise NotImplementedError("This method should be overridden by subclasses")