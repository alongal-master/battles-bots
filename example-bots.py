

class AttackTheMininal(SpaceBotInterface):
    """
    This bot attacks a the weakest opponent, always with 75% of available ammo.
    """

    def attack(self, other_bots):
        # Select the bot with the lowest health.
        target = min(other_bots, key=lambda bot: bot.get_health())

        # Attack with 25% of my ammo
        attack_ammo = int(self._ammo * 0.75)

        return target, attack_ammo




class AttackTheStrongest(SpaceBotInterface):
    """
    This bot attacks a the strongest opponent, always with 50% of available ammo.
    """

    def attack(self, other_bots):
        # Select the bot with the lowest health.
        target = max(other_bots, key=lambda bot: bot.get_health())

        # Attack with 50% of my ammo
        attack_ammo = int(self._ammo * 0.5)

        return target, attack_ammo


class SuperSmart(SpaceBotInterface):
    """
    This bot attacks by this order:
    1 - If I can destroy someone in this turn -
        -> If he is able to destroy me - DESROY HIM.
        -> If not, destroy someone I'm able to destroy.
    2 - If didn't find, skip the turn (return None).
    """

    def attack(self, other_bots):
        # List all bots we can destroy in one turn
        able_to_destroy = [bot for bot in other_bots if bot.get_health() <= self.get_ammo()]
        # Look for a bot can destroy me next turn, attack him with the minimal ammo needed
        for bot in able_to_destroy:
            if bot.get_ammo() > self.get_health():
                return bot, bot.get_health()
        # Else, attack the first bot that I am able to destroy
        if able_to_destroy:
            target = able_to_destroy[0]
            return target, target.get_health()
        # Didn't find anyone i'm able to destroy, so skip the turn.
        return None, 0



# def main():
#     # Instantiate some SpaceBots (use your own SpaceBot class here)
#     bot1 = bots.AttackTheMininal("AttackMinimal")
#     bot2 = bots.RandomAttacker("Randomizied")
#     bot3 = bots.AttackTheStrongest("AttackStrong")
#     bot4 = bots.SuperSmart("SuperSmart")
#     bot_list = [bot1, bot2, bot3, bot4]
#
#     new_game = game.BattleGame(bot_list)
#     new_game.start()
#
#
# if __name__ == "__main__":
#     main()
#
