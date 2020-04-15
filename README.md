# python-sc2-bot-template

Use this template to start a new python-sc2 bot - just click the green `Use this template` button above.  
Then, if you need, follow the tutorial below.  

# Tutorial: Starting a python-sc2 bot

## Preparing your environment

First you will need to prepare your environment.

### Prerequisites

##### Python

This tutorial recommends you use Python version 3.7.X because that's what most bot authoring tools use.
However, Python 3.8 should also work with this tutorial.

##### Git

This tutorial will use git for version control.

##### Starcraft 2

On Windows SC2 is installed through the Battle.net app.  
Linux users can download SC2 [here](https://github.com/Blizzard/s2client-proto#downloads).

SC2 needs to be installed in the default location. Otherwise (and for Linux) you will need to create the SC2PATH env var to point to the SC2 install location.

##### Starcraft 2 Maps

Download the Starcraft 2 Maps from [here](https://github.com/Blizzard/s2client-proto#downloads).  
The maps must be copied into the **root** of the Starcraft 2 maps folder - default location: `C:\Program Files (x86)\StarCraft II\Maps`.

## Creating your bot
### Setup
Clone your new repository using git:
```bash
git clone --recursive <your_git_clone_repo_url_here>
```
cd into your bot directory:
```bash
cd <bot_folder_name_here>
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


### Bot name and race

Now you will want to name your bot and select its race.
You can specify both of these in the [bot/bot.py](bot/bot.py) file, in the `CompetitiveBot` class.

### Updating your bot

As you add features to your bot make sure all your new code files are in the `bot` folder. This folder is included when creating the ladder.zip for upload to the bot ladders.

# Working with submodules

If you cloned the repo without specifying `--recursive` you can initialize and checkout
the required submodules with the following git command:

```bash
git submodule update --init --recursive
```