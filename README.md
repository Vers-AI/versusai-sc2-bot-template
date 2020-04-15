# python-sc2-bot-template

Use this template to start a new python-sc2 bot - just click the green `Use this template` button above.  
Then, if you need, follow the instructions below.  

## Preparing your environment

First you will need to prepare your environment.

### Prerequisites

##### Python 3.7.X

You will need to install and use Python 3.7.  
If you use another version of python, you will likely run into errors while using the python-sc2 framework.  

##### Git

This tutorial will use git for version control.

##### Starcraft 2

On Windows SC2 is installed through the Battle.net app.  
Linux users can download SC2 [here](https://github.com/Blizzard/s2client-proto#downloads).

SC2 needs to be installed in the default location. Otherwise (and for Linux) you will need to create the SC2PATH env var to point to the SC2 install location.

##### Starcraft 2 Maps

Download the Starcraft 2 Maps from [here](https://github.com/Blizzard/s2client-proto#downloads).  
The maps must be present in the **root** of the Starcraft 2 maps folder for the purposes of this tutorial.

## Creating your bot
### Setup
Clone the repository:
```bash
git clone --recursive <your_git_clone_repo_url_here>
```
cd into your bot directory:
```bash
cd <bot_folder_name_here>
```
Install our bot's requirements:
```bash
pip install -r requirements.txt
```
Test our bot is working by running it:
```bash
python ./run.py
```
If all is well, you should see SC2 load and your bot start playing - although it will do nothing at the moment.


### Bot name and race

Go to the [bot/bot.py](bot/bot.py) and specify your bot's name and race.

### Adding to your bot

Put all your new code files in the `bot` folder. This folder is included when creating the ladder.zip for upload to the bot ladders.

# Working with submodules

If you cloned the repo without specifying `--recursive` you can initialize and checkout
the required submodules with the following git command:

```bash
git submodule update --init --recursive
```