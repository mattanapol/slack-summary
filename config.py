import yaml

class SlackConf:
    def __init__(self, raw):
        self.token = raw['token']
        self.channels = raw['channels']

class OpenAIConf:
    def __init__(self, raw):
        self.api_key = raw['api-key']

class Config:
    def __init__(self, raw):
        self.slack = SlackConf(raw['slack'])
        self.open_ai = OpenAIConf(raw['open-ai'])

def load_conf(path: str):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    return Config(config)