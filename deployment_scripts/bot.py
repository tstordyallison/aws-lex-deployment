from amazon_lex_bot_deploy import amazon_lex_bot_deploy
import boto3
import json
import os
import tempfile


class Bot:
    CLIENT_NAME="lex-models"
    CONFIG_FILE_NAME="config.json"

    def __init__(self, client=None, region=None, account=None):
        self.client = client or boto3.client
        self.region = region or os.environ["AWS_DEFAULT_REGION"]
        self.account = account or self.client("sts").get_caller_identity()["Account"]

    def _parse_intents_file(self, intent_name, path):
        with open(path) as cfg_file:
            cfg_file_content = cfg_file.read() \
                .replace("{ReplaceWithAWSRegion}", self.region) \
                .replace("{ReplaceWithAWSAccountId}", self.account) \
                .replace("{ReplaceWithIntentName}", intent_name)

            config = json.loads(cfg_file_content)

        return config

    def _get_all_intents(self, intents_dir):
        intents = os.listdir(intents_dir)

        intent_configs = []
        for i in intents:
            intent_config_path=os.path.join(intents_dir, i, self.CONFIG_FILE_NAME)

            #TODO Do you want to fail on a missing config file for an Intent dir?
            if os.path.isfile(intent_config_path):
                intent_configs.append(self._parse_intents_file(intent_name=i, path=intent_config_path))

        return intent_configs

    def _lex_deploy(self, bot_name, bot_config_file, all_intents):
        with open(bot_config_file) as bot_config_file:
            cfg_file_content = bot_config_file.read() \
                .replace("{ReplaceWithBotName}", bot_name)

            bot_config = json.loads(cfg_file_content)

        #Set the intents of the bot with all of our combined intent files
        bot_config["resource"]["intents"] = all_intents

        #lex_deploy takes a file so create a temporary file to deploy with
        fd, temp_path = tempfile.mkstemp()
        with open(temp_path, 'w') as tmp_f:
            tmp_f.write(json.dumps(bot_config))
            tmp_f.seek(0)

        amazon_lex_bot_deploy.lex_deploy(lex_schema_file=temp_path)

        #Clean up temp file
        os.close(fd)
        os.remove(temp_path)

        print("Deployed Bot %s into region %s" % (bot_name, self.region))

    def deploy(self, bot_name, bot_config_file, intents_dir):
        all_intents = self._get_all_intents(intents_dir)
        self._lex_deploy(
            bot_name=bot_name,
            bot_config_file=bot_config_file,
            all_intents=all_intents
        )
