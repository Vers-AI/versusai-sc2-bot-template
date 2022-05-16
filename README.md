# python-sc2-bot-template

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

## Competing with your bot

To compete with your bot, you will first need zip up your bot, ready for distribution.   
You can do this using the `create_ladder_zip.py` script like so:
```
python create_ladder_zip.py
```
This will create the zip file`publish\bot.zip`.
You can then distribute this zip file to competitions.
