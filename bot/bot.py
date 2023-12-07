from sc2.bot_ai import BotAI, Race
from sc2.data import Result
from sc2.ids.unit_typeid import UnitTypeId

class CompetitiveBot(BotAI):
    NAME: str = "Zippy"
    """This bot's name"""

    RACE: Race = Race.Terran
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """

    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")

    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        Populate this function with whatever your bot should do!
        """
        for loop_cc in self.workers:
            cc_list = self.townhalls(UnitTypeId.COMMANDCENTER).ready.idle
            if self.can_afford(UnitTypeId.SCV) and self.workers.amount <= 15 and cc_list.exists:
                self.townhalls.ready.random.train(UnitTypeId.SCV)
            elif self.workers.amount == 15:
                for worker in self.workers:
                    worker.attack(self.enemy_start_locations[0])
                    
    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")


    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
