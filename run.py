
from bot import CompetitiveBot

import argparse
import asyncio
import logging
import aiohttp
import sc2
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.client import Client
from sc2.player import Bot, Computer
from sc2.protocol import ConnectionAlreadyClosed


# Run ladder game
# This lets python-sc2 connect to a ladder game.
# Based on: https://github.com/Dentosal/python-sc2/blob/master/examples/run_external.py
def run_ladder_game(args, bot):
    if args.LadderServer == None:
        host = "127.0.0.1"
    else:
        host = args.LadderServer

    host_port = args.GamePort
    lan_port = args.StartPort

    # Port config
    ports = [lan_port + p for p in range(1, 6)]

    portconfig = sc2.portconfig.Portconfig()
    portconfig.shared = ports[0]  # Not used
    portconfig.server = [ports[1], ports[2]]
    portconfig.players = [[ports[3], ports[4]]]

    # Join ladder game
    g = join_ladder_game(host=host, port=host_port, players=[bot], realtime=args.Realtime, portconfig=portconfig)

    # Run it
    result = asyncio.get_event_loop().run_until_complete(g)
    return result, args.OpponentId


# Modified version of sc2.main._join_game to allow custom host and port, and to not spawn an additional sc2process (thanks to alkurbatov for fix)
async def join_ladder_game(
        host, port, players, realtime, portconfig, save_replay_as=None, step_time_limit=None, game_time_limit=None
):
    ws_url = "ws://{}:{}/sc2api".format(host, port)
    ws_connection = await aiohttp.ClientSession().ws_connect(ws_url, timeout=120)
    client = Client(ws_connection)
    try:
        result = await sc2.main._play_game(players[0], client, realtime, portconfig, step_time_limit, game_time_limit)
        if save_replay_as is not None:
            await client.save_replay(save_replay_as)
        # await client.leave()
        # await client.quit()
    except ConnectionAlreadyClosed:
        logging.error(f"Connection was closed before the game ended")
        return None
    finally:
        await ws_connection.close()

    return result


def parse_arguments():
    # Load command line arguments
    parser = argparse.ArgumentParser()

    # Ladder play arguments
    parser.add_argument("--GamePort", type=int, help="Game port.")
    parser.add_argument("--StartPort", type=int, help="Start port.")
    parser.add_argument("--LadderServer", type=str, help="Ladder server.")

    # Local play arguments
    parser.add_argument("--Sc2Version", type=str, help="The version of Starcraft 2 to load.")
    parser.add_argument("--ComputerRace", type=str, default="Terran",
                        help="Computer race. One of [Terran, Zerg, Protoss, Random]. Default is Terran. Only for local play.")
    parser.add_argument("--ComputerDifficulty", type=str, default="VeryHard",
                        help=f"Computer difficulty. One of [VeryEasy, Easy, Medium, MediumHard, Hard, Harder, VeryHard, CheatVision, CheatMoney, CheatInsane]. Default is VeryEasy. Only for local play.")
    parser.add_argument("--Map", type=str, default="Simple64",
                        help="The name of the map to use. Default is Simple64. Only for local play.")

    # Both Ladder and Local play arguments
    parser.add_argument("--OpponentId", type=str, help="A unique value identifying opponent.")
    parser.add_argument("--Realtime", action='store_true', help="Whether to use realtime mode. Default is false.")

    args, unknown_args = parser.parse_known_args()

    for unknown_arg in unknown_args:
        print(f"Unknown argument: {unknown_arg}")

    # Set the OpponentId if it's not already set
    if args.OpponentId is None:
        if args.LadderServer:
            args.OpponentId = "None"
        else:
            args.OpponentId = f"{args.ComputerRace}_{args.ComputerDifficulty}"

    return args


def load_bot(args):
    # Load bot
    competitive_bot = CompetitiveBot()
    # Add opponent_id to the bot class (accessed through self.opponent_id)
    competitive_bot.opponent_id = args.OpponentId

    return Bot(CompetitiveBot.RACE, competitive_bot)


def run():
    args = parse_arguments()

    bot = load_bot(args)

    # The presence of a LadderServer argument indicates that this is a ladder game
    if args.LadderServer:
        # Ladder game started by LadderManager
        print("Starting ladder game...")
        result, opponentid = run_ladder_game(args, bot)
        print(result, " against opponent ", opponentid)
    else:
        # Local game
        print("Starting local game...")
        run_game(sc2.maps.get(args.Map),
                     [bot, Computer(Race[args.ComputerRace], Difficulty[args.ComputerDifficulty])],
                     realtime=args.Realtime,
                     sc2_version=args.Sc2Version, )


# Start game
if __name__ == "__main__":
    run()
