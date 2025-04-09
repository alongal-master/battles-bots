import random
import bots
import gui

class BattleGame:

    bonus_for_destroy = 20

    def __init__(self, bots):
        self._bots = bots
        self.gui = gui.SpaceBattleUI(self, self._bots)
        self.round = 1
        self.current_round_active = False
        self.current_round_queue = None
    
    def log(self, text):
        self.gui.log_message(text)

    def print_health(self):
        """"
        Prints the health charts for all players
        """
        for bot in self._bots:
            print(f"{bot.get_name().ljust(20)} |{'*' * bot.get_health()}| {bot.get_health()} (Ammo: {bot.get_ammo()})")
        print("\n")

    def check_attack(self, attacker, target, ammo):
        """"
        Gets params of an attack, Checks that they are valid and returns True.
        If not, returns False.
        """
        # Check that ammo level used actually exists
        if ammo > attacker.get_ammo():
            self.log(f"ERROR! Illegal attack from {attacker.get_name()}, ammo {ammo} is too high")
            return False

        # Checks type of target object
        if target is None:
            self.log(f"Attacker {attacker.get_name()} decided to attack None")
            return False

        # Checks type of target object
        if not isinstance(target, bots.SpaceBotInterface):
            self.log(f"ERROR! Attacker {attacker.get_name()} returned wrong type for attack target: {type(target)}, expected SpaceBotInterface")
            return False

        # Checks that the ammo is int or something that converts to int
        try:
            ammo = int(ammo)
        except:
            self.log(f"ERROR! Attacker {attacker.get_name()} returned wrong type for attack ammo: {type(ammo)}, expected int")
            return False
        return True

    def battle_round(self):
        """"
        Creates a new round or continues existing round of a battle.
        """
        # If it's a new round (last round is over)
        if not self.current_round_active:
            # Create a randomized list of the bots for turn order
            random_ordered_bots = [bot for bot in self._bots if bot.is_alive()]
            random.shuffle(random_ordered_bots)
            self.current_round_queue = random_ordered_bots
            self.current_round_active = True
            self.log(f"Next up is {self.current_round_queue[0].get_name()}")


        # No more players for this round, so it's over
        if not self.current_round_queue:
            self.current_round_active = False
            self.round += 1
            self.gui.update_round_display(self.round)
            self.log(f"Round {self.round-1} is over.")
            self.log(f"Starting round {self.round}! Randomizing the order of bots.")


        # If it's an existing round, pick the player to play for
        else:
            bot = self.current_round_queue.pop(0)
            not_played = True
            if bot.is_alive():  # Bot can only attack if it's alive
                # Create list of available opponents
                opponents = [opponent for opponent in self._bots if opponent is not bot and opponent.is_alive()]
                if opponents:  # only attack if there are opponents left
                    self.log("")
                    self.perform_attack(bot, opponents)
                    self.print_health()
                    self.gui.update()

        # Remove dead players from the queue
        new_queue = []
        for bot in self.current_round_queue:
            if bot.is_alive():
                new_queue.append(bot)
        self.current_round_queue = new_queue
        if len(self.current_round_queue) > 0:
            self.log(f"Next up is {self.current_round_queue[0].get_name()}")
    def perform_attack(self, bot, opponents):
        """"
        Performs a single attack of the given bot, with the available opponents.
        """
        try:
            target, ammo = bot.attack(opponents)
        except Exception as e:
            # If attacker function raised an error
            self.log(f"ERROR! Attacker {bot.get_name()} function crashed ({e})")
            attack_is_legal = False
        else:
            # If didn't crash, check that attack is legal
            attack_is_legal = self.check_attack(bot, target, ammo)

        # Perform the attack.
        if attack_is_legal:
            self.log(f"{bot.get_name()} is attacking {target.get_name()} with {ammo} ammo!")
            self.gui.shoot(bot, target, ammo)
            target.take_attack(int(ammo))
            bot.deduct_ammo(int(ammo))
            if not target.is_alive():
                bot.add_ammo(BattleGame.bonus_for_destroy)
                bot.add_health(BattleGame.bonus_for_destroy)
                self.gui.remove_bot(target)
                self.log(f"{target.get_name()} was destroyed! {bot.get_name()} awarded with {BattleGame.bonus_for_destroy} bonus ammo and health!")
        else:
            self.log(f"Skipping {bot.get_name()}..")

    def game_is_over(self):
        """"
        Checks is game is over, returns True or False.
        """
        alive_bots = [bot for bot in self._bots if bot.is_alive()]
        # If all dead but one, or all dead

        if len(alive_bots) <= 1:
            self.log("Only one bot is remained alive!")
            return True

        # If all the ammos combined is less than the lowest bots' health, game is over
        min_health = min([bot.get_health() for bot in alive_bots])
        total_ammos = sum([bot.get_ammo() for bot in alive_bots])
        if total_ammos < min_health:
            self.log("No one has enough ammo to kill another bot")
            return True

        return False

    def the_winners(self):
        """"
        Returns a list of the winner(s) of the game (The bots with most health).
        If few have the same health, they all win!
        """
        max_health = max([bot.get_health() for bot in self._bots])
        winners = [bot for bot in self._bots if bot.get_health() == max_health]
        return winners

    def start(self):
        """"
        Plays all rounds of the game, until it ends
        """
        # Initial health display
        self.log("Welcome to a new battle of the bots!")
        self.print_health()
        self.gui.show()


    def play_next_turn(self):
        if not self.game_is_over():
            self.gui.disable_next_move_button()
            self.battle_round()

            # Update gui
            self.gui.update()
            self.gui.enable_next_move_button()
        else:
            self.log("Game is over!")
            self.gui.disable_next_move_button()
            # Announce the winner
            winners = self.the_winners()
            if len(winners) == 1:
                self.log(f"The winner is {winners[0].get_name()}!")
            else:
                for i, bot in enumerate(winners, 1):
                    self.log(f"Winner #{i} is {bot.get_name()}!")
