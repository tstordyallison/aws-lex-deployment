import boto3

CLIENT_NAME="lex-models"


def deploy(bot_name, intents, _client=boto3.client):
    client = _client(CLIENT_NAME)

    response = client.put_bot(
        name=bot_name,
        description="Chat Bot",
        locale="en-US",
        childDirected=False,
        intents=[{
            "intentName": i,
            "intentVersion": '$LATEST'
        } for i in intents]
    )

    print(response)
    print("Created/Updated bot %s" % bot_name)


def delete(bot_name, _client=boto3.client):
    client = _client(CLIENT_NAME)

    client.delete_bot(name=bot_name)


def get(bot_name, _client=boto3.client):
    client = _client(CLIENT_NAME)

    return client.get_bot(name=bot_name, versionOrAlias="$LATEST")
