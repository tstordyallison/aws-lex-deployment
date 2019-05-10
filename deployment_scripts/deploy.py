import sys
import deploy_bot

def deploy(bot_name):
    deploy_bot.deploy(bot_name=bot_name)

if __name__ == "__main__":
    args = sys.argv[1:]
    deploy(
        bot_name=args[0]
    )
