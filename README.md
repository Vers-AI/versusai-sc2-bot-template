# probots-sc2-bot-template

Use this template to start a new Starcraft 2 bot using the [python-sc2](https://github.com/BurnySc2/python-sc2) framework.  
Then, if you need, follow the tutorial below.  

# Tutorial: Starting a python-sc2 bot

## Preparing your environment

First you will need to prepare your environment.

### Prerequisites

##### Python

This tutorial recommends you use Python version 3.8.X.
However, newer Python versions should also work with this tutorial.
[Python downloads page](https://www.python.org/downloads/)

##### Git

This tutorial will use git for version control.  
[Git downloads page](https://git-scm.com/downloads)

##### Starcraft 2

On Windows SC2 is installed through the Battle.net app.  
Linux users can either download the Blizzard SC2 Linux package [here](https://github.com/Blizzard/s2client-proto#linux-packages) or, alternatively, set up Battle.net via WINE using this [lutris script](https://lutris.net/games/battlenet/).

SC2 should be installed in the default location. Otherwise (and for Linux) you might need to create the SC2PATH environment variable to point to the SC2 install location.

## Environment Setup for Linux (Lutris)

If you've installed StarCraft II using Lutris on Linux, you'll need to set some environment variables so that the `python-sc2` library can correctly interact with the game.

### Setting Environment Variables Temporarily

Open a terminal and enter the following commands, replacing `(username)` with your actual Linux username and `(version of wine)` with the version of Wine that Lutris is using:

```bash
export SC2PF=WineLinux
export SC2PATH="/home/`(username)`/Games/battlenet/drive_c/Program Files (x86)/StarCraft II/"
export WINE="/home/`(username)`/.local/share/lutris/runners/wine/`(version of wine)`/bin/wine" 
```

##### Starcraft 2 Maps

Download the Starcraft 2 Maps from [here](https://github.com/Blizzard/s2client-proto#map-packs).   For this tutorial you will at least need the 'Melee' pack.  
The maps must be copied into the **root** of the Starcraft 2 maps folder - default location: `C:\Program Files (x86)\StarCraft II\Maps`.

## Creating your bot
### Setup
Click the green `Use this template` button above to create your own copy of this bot.  
Now clone your new repository to your local computer using git:
```bash
git clone <your_git_clone_repo_url_here>
```
cd into your bot directory:
```bash
cd <bot_folder_name_here>
```
Create and activate a virtual environment:
```bash
python -m venv venv
# and then...
venv\Scripts\activate # Windows CMD Prompt / PowerShell
source venv/bin/activate # Mac OS / Linux
```
Install our bot's Python requirements:
```bash
pip install -r requirements.txt
```
Test our bot is working by running it:
```bash
python ./run.py
```
If all is well, you should see SC2 load and your bot start mining minerals.  
You can close the SC2 window to stop your bot running. 

## Updating your bot

### Bot name and race

Now you will want to name your bot and select its race.
You can specify both of these in the [bot/bot.py](bot/bot.py) file, in the `CompetitiveBot` class.

### Adding new code

As you add features to your bot make sure all your new code files are in the `bot` folder. This folder is included when creating the ladder.zip for upload to the bot ladders.

## Upgrading to Ares Framework

Ares-sc2 is a library that extends python-sc2, offering advanced tools and functionalities to give you greater control over your bot's strategic decisions. If you want more sophisticated and nuanced gameplay tactics, upgrading to Ares-sc2 is the way to go.

### Running the Upgrade Script

Run the following command:
```bash
python upgrade_to_ares.py
```

### Code Changes

#### Updating the Bot Object

The main bot object should inherit from `ares-sc2` instead of `python-sc2`.

**python-sc2:**
```python
from sc2.bot_ai import BotAI

class MyBot(BotAI):
    pass
```

**ares-sc2:**
```python
from ares import AresBot

class MyBot(AresBot):
    pass
```

#### Adding Super Calls to Hook Methods

For any `python-sc2` hook methods you use, add a `super` call. Only convert the hooks you actually use.

**python-sc2:**
```python
class MyBot(AresBot):
    async def on_step(self, iteration: int) -> None:
        pass

    async def on_start(self, iteration: int) -> None:
        pass

    async def on_end(self, game_result: Result) -> None:
        pass

    async def on_building_construction_complete(self, unit: Unit) -> None:
        pass

    async def on_unit_created(self, unit: Unit) -> None:
        pass

    async def on_unit_destroyed(self, unit_tag: int) -> None:
        pass

    async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float) -> None:
        pass
```

**ares-sc2:**
```python
class MyBot(AresBot):
    async def on_step(self, iteration: int) -> None:
        await super(MyBot, self).on_step(iteration)
        # on_step logic here ...

    async def on_start(self, iteration: int) -> None:
        await super(MyBot, self).on_start(iteration)
        # on_start logic here ...

    async def on_end(self, game_result: Result) -> None:
        await super(MyBot, self).on_end(game_result)
        # custom on_end logic here ...

    async def on_building_construction_complete(self, unit: Unit) -> None:
        await super(MyBot, self).on_building_construction_complete(unit)
        # custom on_building_construction_complete logic here ...

    async def on_unit_created(self, unit: Unit) -> None:
        await super(MyBot, self).on_unit_created(unit)
        # custom on_unit_created logic here ...

    async def on_unit_destroyed(self, unit_tag: int) -> None:
        await super(MyBot, self).on_unit_destroyed(unit_tag)
        # custom on_unit_destroyed logic here ...

    async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float) -> None:
        await super(MyBot, self).on_unit_took_damage(unit, amount_damage_taken)
        # custom on_unit_took_damage logic here ...
```

## Competing with your bot

To compete with your bot, you will first need zip up your bot, ready for distribution.   
You can do this using the `create_ladder_zip.py` script like so:
```
python create_ladder_zip.py
```
This will create the zip file`publish\bot.zip`.
You can then distribute this zip file to competitions.
