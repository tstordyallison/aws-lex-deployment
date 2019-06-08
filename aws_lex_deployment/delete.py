import aws_lex_deployment.bot as bot
import aws_lex_deployment.intents as intents
import sys
import time
import argparse
import botocore

#TODO Add support for version
def delete(bot_name, bot_only):
    ''' Delete the bot. If requested, also delete the intents associated. '''

    bot_desc = bot.get(bot_name=bot_name)
    bot.delete(bot_name=bot_name)

    deleted_intents  = []
    if not bot_only:
        for intent in bot_desc["intents"]:
            intent_name = intent["intentName"]
            deleted_intents.append(intent_name)

            for _ in range(3):
                try:
                    intents.delete(intent_name)
                    break
                except botocore.exceptions.ClientError as err:
                    if err.response['Error']['Code'] == 'ConflictException':
                         time.sleep(1)
                    else:
                        raise

    print(f"Deleted bot {bot_name} and {deleted_intents} intents.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete a bot from Lex.')

    parser.add_argument('bot_name', help='The name of the bot to delete.')
    parser.add_argument('--bot_only', dest='bot_only', action="store_true", default=False, help="Only remobve the bot, leave the intents.")

    args = parser.parse_args()

    delete(
        bot_name=args.bot_name,
        bot_only=args.bot_only
    )
