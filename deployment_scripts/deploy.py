import bot
import sys

#TODO Add support for version
def deploy(bot_name, bot_config_file, intents_dir):
    bot.Bot().deploy(
        bot_name=bot_name,
        bot_config_file=bot_config_file,
        intents_dir=intents_dir
    )

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 3:
        raise AssertionError("Expecting 2 arguments, usage:python ./deployment_scripts/deploy.py <bot_name> <bot_config_file> <intents_dir>")

    #TODO Use https://docs.python.org/3/library/argparse.html rather than just arg position
    deploy(
        bot_name=args[0],
        bot_config_file=args[1],
        intents_dir=args[2]
    )
