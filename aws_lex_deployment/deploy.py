import aws_lex_deployment.bot as bot
import aws_lex_deployment.intents as intents
import aws_lex_deployment.intent_lambda as intent_lambda
import sys
import os
import argparse

#TODO Add support for version
#TODO Add bot metadata upload

def deploy(bot_dir, instance=None):
    _, bot_name = os.path.split(os.path.normpath(bot_dir))
    intent_lambda.deploy(intents_dir=bot_dir, instance=instance)
    deployed_intent_names = intents.deploy(intents_dir=bot_dir, instance=instance)
    bot.deploy(bot_name=bot_name, intents=deployed_intent_names, instance=instance)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Deploy bot to Lex.')

    parser.add_argument('bot_dir', help='directory containing your bot intents + lambdas')
    parser.add_argument('--instance', dest='instance', default=None, help="add an 'instance' name to your bot, intents and lambdas")

    args = parser.parse_args()

    deploy(bot_dir=args.bot_dir, instance=args.instance)
