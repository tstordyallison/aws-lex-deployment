import aws_lex_deployment.bot as bot
import aws_lex_deployment.intents as intents
import aws_lex_deployment.intent_lambda as intent_lambda
import sys

#TODO Add support for version
def deploy(bot_name, intents_dir):
    intent_lambda.deploy(intents_dir=intents_dir)
    deployed_intent_names = intents.deploy(intents_dir=intents_dir)
    bot.deploy(bot_name=bot_name, intents=deployed_intent_names)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 2:
        raise AssertionError("Expecting 2 arguments, usage:python ./aws_lex_deployment/deploy.py <bot_name> <intents_dir>")

    deploy(
        bot_name=args[0],
        intents_dir=args[1]
    )
