import boto3
import botocore
import json
import os
import io
import zipfile
import time

CLIENT_NAME = "cloudformation"

def cf_deploy(intent_name, cf_json, client):
    params = {
        "StackName": intent_name + "-Stack",
        "TemplateBody": json.dumps(cf_json),
        "Parameters":[
            {
                'ParameterKey': 'IntentName',
                'ParameterValue': intent_name
            }
        ]
    }

    stack_exists = False
    try:
        stack_exists = len(client.describe_stacks(StackName=intent_name + "-Stack")["Stacks"]) > 0
    except botocore.exceptions.ClientError as err:
        #TODO check the actual error
        print("Stack %s most likely doesn't exist" % intent_name + "-Stack")

    if stack_exists:
        try:
            response = client.update_stack(**params)
            print(response)
        except botocore.exceptions.ClientError as err:
            #TODO check the actual error for lambda not needing to change
            print("Lambda %s most likely doesn't need updating" % intent_name + "-Lambda")
            print(cf_json)
            print(err)

    else:
        client.create_stack(**params)


def deploy(intents_dir, _client=boto3.client):
    client = _client(CLIENT_NAME)
    print("Deploying all lambdas under intents dir %s" % intents_dir)

    intents = os.listdir(intents_dir)
    intents_with_lambdas = [i for i in intents if "lambda.py" in os.listdir(os.path.join(intents_dir, i))]

    for i in intents_with_lambdas:
        with open(os.path.join("cloudformation", "intent_lambda.json")) as lambda_cfg_f:
            lambda_cfg = lambda_cfg_f.read()

            # with zipfile.ZipFile(i + '.zip', 'w') as myzip:
            #     myzip.write(os.path.join(intents_dir, i, "lambda.py"))

            # with open(os.path.join(intents_dir, i, "lambda.py")) as lambda_code:
            #     lambda_cfg = lambda_cfg.replace("{ReplaceWithIntentLambdaCode}", io.BytesIO(i + '.zip').getvalue())
            #     print(lambda_cfg)

            with open(os.path.join(intents_dir, i, "lambda.py")) as lambda_code:
                lambda_code_replace = {"ZipFile": {"Fn::Join": ["\n", [l.replace("\n", "") for l in lambda_code.readlines()]]}}
                print(lambda_code_replace)

            lambda_cfg_json = json.loads(lambda_cfg)
            lambda_cfg_json["Resources"]["IntentLambda"]["Properties"]["Code"] = lambda_code_replace

        cf_deploy(
            intent_name=i,
            cf_json=lambda_cfg_json,
            client=client
        )

    time.sleep(30)

if __name__ == "__main__":
    deploy("./intents")
