import sys
import deploy_bot
import deploy_intents

def deploy(bot_name, intents_dir):
    deployed_intent_names = deploy_intents.deploy(intents_dir=intents_dir)
    deploy_bot.deploy(bot_name=bot_name, intents=deployed_intent_names)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 2:
        raise AssertionError("Expecting 2 arguments, usage:python ./deployment_scripts/deploy.py <bot_name> <intents_dir>")

    deploy(
        bot_name=args[0],
        intents_dir=args[1]
    )
