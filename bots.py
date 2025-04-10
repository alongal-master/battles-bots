from abc import ABC, abstractmethod
import random


class SpaceBotInterface(ABC):
    initial_health = 100
    initial_ammo = 80

    def __init__(self, name):
        """"
        Initialises the bot with the initial health and ammo, and the given name.
        """
        self._name = str(name)
        self._health = SpaceBotInterface.initial_health
        self._ammo = SpaceBotInterface.initial_ammo

    def get_name(self):
        """"
        Returns the name of the bot.
        """
        return self._name

    def get_health(self):
        """"
        Returns the health level of the bot.
        """
        return self._health

    def add_health(self, points):
        """"
        Adds the given points to the instance helath points
        """
        try:
            assert points > 0
            self._health += points
        except Exception:
            return

    def is_alive(self):
        """"
        Returns True if bot is alive (health more than 0), False if it's dead.
        """
        return self._health > 0

    def get_ammo(self):
        """"
        Returns the ammo of the bot.
        """
        return self._ammo

    def add_ammo(self, points):
        """"
        Adds the given points to the instance ammo points
        """
        try:
            assert points > 0
            self._ammo += points
        except Exception:
            return

    def deduct_ammo(self, points):
        """"
        Deducts the given points to the instance ammo points
        """
        try:
            assert points > 0
            self._ammo -= points
        except Exception:
            return

    def take_attack(self, amount):
        """"
        Takes the attack, if health is below 0, it should be set to 0
        """
        try:
            assert amount > 0
            self._health = max([self._health - amount, 0])
        except Exception:
            return

    @abstractmethod
    def attack(self, other_bots):
        """"
        This will be implemented in the child objects. This function gets a list of SpaceBots,
        It should return the selected target for attack (SpaceBot object), and the amount of ammo to use (int).
        Note:
           - If the function raises exception, you will use your turn!
           - If you use more ammo than you have, you will use your turn!
           - If you return values of the wrong type, you will use your turn!
        """
        pass


class RandomAttacker(SpaceBotInterface):

    def attack(self, other_bots):
        """"
        This attack will select a random target, and attack it with 20 ammo.
        """
        target = random.choice(other_bots)
        return target, 20

