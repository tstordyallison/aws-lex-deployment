import boto3
import botocore
import json
import os
import io
import zipfile
import time

CLIENT_NAME = "cloudformation"
WAIT_TIME_MAX = 60

def _cf_ready(client, stack_name):
    # TODO: there's probably a nicer way of doing this...
    stacks = client.describe_stacks(StackName=stack_name)["Stacks"]
    for stack in stacks:
        if stack['StackStatus'] not in ( 'CREATE_COMPLETE', 'UPDATE_COMPLETE' ):
            return False
    return True

def _cf_deploy(intent_name, cf_json, client):
    params = {
        "StackName": intent_name + "-Stack",
        "TemplateBody": json.dumps(cf_json),
        "Parameters":[
            {
                'ParameterKey': 'IntentName',
                'ParameterValue': intent_name
            }
        ],
        "OnFailure" : 'DO_NOTHING'
    }

    stack_exists = False
    try:
        stack_exists = len(client.describe_stacks(StackName=intent_name + "-Stack")["Stacks"]) > 0
    except botocore.exceptions.ClientError as err:
        #TODO check the actual error
        print("Stack %s most likely doesn't exist" % intent_name)

    if stack_exists:
        try:
            params.pop('OnFailure')
            _response = client.update_stack(**params)
        except botocore.exceptions.ClientError as err:
            if 'No updates are to be performed' in str(err):
                return params["StackName"], False
            else:
                raise
            
    else:
        client.create_stack(**params)
    
    return params["StackName"], True


def deploy(intents_dir, instance=None):
    client = boto3.client(CLIENT_NAME)
    print("Deploying all lambdas under intents dir %s" % intents_dir)

    intents = os.listdir(intents_dir)
    intents_with_lambdas = [intent_name for intent_name in intents if "lambda.py" in os.listdir(os.path.join(intents_dir, intent_name))]

    updated_stacks = []

    for intent_name in intents_with_lambdas:
        with open(os.path.join("cloudformation", "intent_lambda.json")) as lambda_cfg_f:
            lambda_cfg = lambda_cfg_f.read()

            # Add full support for uploading to S3 and referring back. 
            if False:
                with zipfile.ZipFile(intent_name + '.zip', 'w') as myzip:
                    myzip.write(os.path.join(intents_dir, intent_name, "lambda.py"))

                with open(os.path.join(intents_dir, intent_name, "lambda.py")) as lambda_code:
                    lambda_cfg = lambda_cfg.replace("{ReplaceWithIntentLambdaCode}", io.BytesIO(intent_name + '.zip').getvalue())

            # Embed the lambda source in the cloud formation config.
            with open(os.path.join(intents_dir, intent_name, "lambda.py")) as lambda_code:
                lambda_code_replace = {"ZipFile": {"Fn::Join": ["\n", [l.replace("\n", "") for l in lambda_code.readlines()]]}}

            lambda_cfg_json = json.loads(lambda_cfg)
            lambda_cfg_json["Resources"]["IntentLambda"]["Properties"]["Code"] = lambda_code_replace

        # Add the instance name if we have one. 
        if instance:
            intent_name = instance + intent_name

        cf_name, changed = _cf_deploy(
            intent_name=intent_name,
            cf_json=lambda_cfg_json,
            client=client
        )

        if changed: 
            updated_stacks.append(cf_name)
    
    if updated_stacks:
        start_time = time.time()
        success = False

        while time.time() - start_time < WAIT_TIME_MAX:
            if all( [ _cf_ready( client, cf_name ) for cf_name in updated_stacks ] ):
                success = True
                break
            print('Waiting for stacks to deploy...')
            time.sleep(5)

        if not success:
            raise RuntimeError( 'Timed out waiting for Lambda CF stacks to deploy.')
                
            