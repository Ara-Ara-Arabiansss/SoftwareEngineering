class State:
    __tablename__='state'

    def __init__(self, ranking):
        self.ranking = ranking
  
    def notify(self):
        pass
      
    def update_state(self):
        pass