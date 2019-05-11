import boto3

def deploy(bot_name, intents, _client=boto3.client):
    client = _client("lex-models")

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
