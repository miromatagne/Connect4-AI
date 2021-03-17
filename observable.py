class Observable:

    def __init__(self):
        self._observers = []

    def notify(self, event, *argv):
        for obs in self._observers:
            obs.update(self, event, *argv)

    def add_observer(self, obs):
        self._observers.append(obs)

    def remove_observer(self, obs):
        if obs in self._observers:
            self._observers.remove(obs)
