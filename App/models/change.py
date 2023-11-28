from App.models import state
from .state import *

class Change(State):
    __tablename__='change'

    def __init__(self, ranking):
        self.ranking = ranking
  
    def notify(self):
        return("Change State")

    def update_state(self):
        self.ranking.state = self.ranking.no_change_state
        return self.ranking.state