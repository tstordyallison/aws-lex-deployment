import aws_lex_deployment.bot as bot
import aws_lex_deployment.intents as intents
import aws_lex_deployment.intent_lambda as intent_lambda
import sys
import os
import argparse

#TODO: Add support for version
#TODO: Add bot metadata download
#TODO: Support some sort of diff to delete intents that are gone remotely

def download(bot_dir, instance=None):
    ''' Download an bot from Lex, or update a local one after making changes online.'''
    os.makedirs(bot_dir, exist_ok=True)

    _, bot_name = os.path.split(os.path.normpath(bot_dir))
    current_bot = bot.get(bot_name, instance=instance)
    
    intent_names = [ intent['intentName' ] for intent in current_bot['intents'] ]
    for intent_name in intent_names:
        print(f'Downloading intent {intent_name}')
        intents.download(intent_name, bot_dir, instance=instance)
        #intent_lambda.download(intent_name, bot_dir)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download an existing bot from Lex/Lambda.')

    parser.add_argument('bot_dir', help='directory containing your bot intents + lambdas')
    parser.add_argument('--instance', dest='instance', default=None, help="add an 'instance' name to your bot, intents and lambdas")

    args = parser.parse_args()

    download(bot_dir=args.bot_dir, instance=args.instance)
