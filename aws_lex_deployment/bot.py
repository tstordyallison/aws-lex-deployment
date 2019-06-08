import boto3
import botocore

CLIENT_NAME="lex-models"

def get(bot_name):
    try:
        client = boto3.client(CLIENT_NAME)
        return client.get_bot(name=bot_name, versionOrAlias="$LATEST")
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'NotFoundException':
            return 
        else:
            raise


def deploy(bot_name, intents, instance=None):
    client = boto3.client(CLIENT_NAME)

    if instance:
        bot_name = instance + '_' + bot_name

    bot = dict( name=bot_name,
        description="Chat Bot",
        locale="en-US",
        childDirected=False,
        clarificationPrompt={
            "messages": [ 
                { 
                    "content": "Sorry, can you repeat that?",
                    "contentType": "PlainText"
                }
            ],
            "maxAttempts": 3,
        },
        abortStatement={ 
            "messages": [ 
                { 
                    "content": "Sorry, I couldn't understand. Best contact us directly!",
                    "contentType": "PlainText"
                }
            ]
        },
        intents=[{
            "intentName": i,
            "intentVersion": '$LATEST'
        } for i in intents]
    )

    current_bot = get(bot_name)
    if current_bot:
        bot['checksum'] = current_bot['checksum']

    _response = client.put_bot(**bot)
    print("Created/Updated bot %s." % bot_name)


def remove_intent(bot_name, intent_name_to_remove):
    current_bot = get(bot_name)
    if current_bot:
        intents = []
        for intent in current_bot['intents']:
            if not intent['intentName'] == intent_name_to_remove:
                intents.append(intent)
        current_bot['intents'] = intents

    current_bot.pop('ResponseMetadata')
    current_bot.pop('status')
    current_bot.pop('lastUpdatedDate')
    current_bot.pop('createdDate')
    current_bot.pop('version')    

    client = boto3.client(CLIENT_NAME)
    client.put_bot(**current_bot)


def delete(bot_name):
    client = boto3.client(CLIENT_NAME)
    client.delete_bot(name=bot_name)

