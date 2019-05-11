import sys

def delete(bot_name):
    print("Deleted bot and intents for %s" % bot_name)

if __name__ == "__main__"
    args = sys.argv[1:]

    if len(args) != 2:
        raise AssertionError("Expecting 1 argument, usage:python ./deployment_scripts/delete.py <bot_name>")

    delete(
        bot_name=bot_name
    )
