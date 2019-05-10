import boto3

def deploy(bot_name, _client=boto3.client):
    client = _client("lex-models")
    
    response = client.put_bot(
        name=bot_name,
        description="Chat Bot",
        locale="en-US",
        childDirected=False
    )
    print(response)
    print("Created/Updated %s" % bot_name)
