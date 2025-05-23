from sc2.bot_ai import BotAI
from sc2.data import Result

class CompetitiveBot(BotAI):
    """Main bot class that handles the game logic."""
    
    def __init__(self):
        super().__init__()

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
        
        pass

    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
