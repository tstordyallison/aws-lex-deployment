import bot
import intents
import sys
import time

#TODO Add support for version
def delete(bot_name, what_to_delete):
    intents_to_delete = []

    '''
        TODO Rather than delete bot before intents, remove intents from bot.
        Otherwise you could be in a state where intents could fail to delete and you don't know which
        intents were associated to which bot.
    '''
    if "intent" in what_to_delete:
        bot_desc = bot.get(bot_name=bot_name)
        intents_to_delete = [i["intentName"] for i in bot_desc["intents"]]

    if "bot" in what_to_delete:
        bot.delete(bot_name=bot_name)

    if intents_to_delete:
        #Wait while intents get detached from bot
        time.sleep(15)
        intents.delete(intent_names=intents_to_delete)

    print("Deleted resources %s for %s" % (str(what_to_delete), bot_name))

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 2:
        raise AssertionError("Expecting 1 argument, usage:python ./deployment_scripts/delete.py <bot_name> <what_do_delete>")

    delete(
        bot_name=args[0],
        what_to_delete=args[1].split(",")
    )
