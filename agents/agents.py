
class Survivor():
    """Survivors are people of the population.
    """

    def __repr__(self):
        return 'Survivor'

    def __init__(self):

        self.speed = None
        self.sex = None
        self.age = None
        self.latitude = None
        self.longitude = None
        self.path = []


class Removed():
    """Removed are those who have been killed.
    They can be in two possible states based
    on whether they can resuscitate or not:
    1) Susceptibles; 2) Terminated
    """

    def __repr__(self):
        return 'Removed'

    def __init__(self):

        self.sex = None
        self.age = None
        self.latitude = None
        self.longitude = None


class Zombie():
    """Zombies that have not been terminated yet"""

    def __repr__(self):
        return 'Zombie'

    def __init__(self):

        self.speed = None
        self.latitude = None
        self.longitude = None
        self.path = []
        self.age = None
        self.old_path = []
