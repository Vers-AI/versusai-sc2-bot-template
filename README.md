# versusai-sc2-bot-template

A template for creating Starcraft 2 AI bots using the [python-sc2](https://github.com/BurnySc2/python-sc2) framework. This template includes a basic bot setup with a clean configuration system.

🚀 **New to StarCraft 2 AI?** 

Check out our [Zerg Rush Bot Step](https://subscribe.versusai.net/zerg-rush) for a quick boost on getting started!

## Features

- Simple configuration via `config.py`
- Easy setup for local development
- Support for custom maps and AI opponents
- Ready-to-use bot structure
- Upgradable to ARES framework

# Quick Start

## Prerequisites

- [Python](https://www.python.org/downloads/) 3.8 or newer
- [Git](https://git-scm.com/downloads)
- [StarCraft II](https://battle.net/account/download/)

### StarCraft II Installation

- **Windows**: Install through the Battle.net app
- **Linux**: 
  - Option 1: Use the [Blizzard SC2 Linux package](https://github.com/Blizzard/s2client-proto#linux-packages)
  - Option 2: Set up Battle.net via WINE using [Lutris](https://lutris.net/games/battlenet/)

### Required Maps

Download the Melee StarCraft 2 Maps from [here](https://blzdistsc2-a.akamaihd.net/MapPacks/Melee.zip). Unzip the file and place the maps in the `Maps` folder in your StarCraft 2 installation directory. If one doesn't exist, create it.

By default, the bot will look for maps in the standard installation location. If your maps are in a different location, update the `MAP_PATH` in `config.py`.

## Linux (Lutris) Setup

If you're using Lutris on Linux, set these environment variables (replace placeholders with your actual paths):

```bash
export SC2PF=WineLinux
export SC2PATH="/home/YOUR_USERNAME/Games/battlenet/drive_c/Program Files (x86)/StarCraft II/"
export WINE="/home/YOUR_USERNAME/.local/share/lutris/runners/wine/YOUR_WINE_VERSION/bin/wine"
```

## Configuration

Edit `config.py` to customize your bot's behavior. The configuration file includes options for:

- **Bot Settings**: Name and race (Terran/Protoss/Zerg/Random)
- **Game Settings**: Map paths and map pool selection
- **Opponent Settings**: AI difficulty and race selection
- **Game Mode**: Toggle between realtime and faster simulation

For advanced configuration, refer to the comments in `config.py`.

## Getting Started

1. **Create your repository**
   - Click the `Use this template` button above to create your own copy

2. **Clone your repository**
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

3. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the bot**
   ```bash
   python run.py
   ```
   The bot should start and begin playing against the AI opponent.

## Customizing Your Bot

### Basic Configuration
Edit `config.py` to change:
- Bot name and race
- Game settings and map pool
- Opponent difficulty and race
- Game mode (realtime or faster simulation)

### Adding Logic
Modify `bot/bot.py` to implement your bot's behavior. The `on_step` method is where you'll add most of your bot's logic.

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

# Competing with your bot

Place your bot on the AI Arena ladder at [here](https://aiarena.net/).

To compete with your bot, you will first need zip up your bot, ready for distribution.   
You can do this using the `create_ladder_zip.py` script like so:
```
python create_ladder_zip.py
```
This will create the zip file`publish\bot.zip`.
You can then distribute this zip file to competitions.
