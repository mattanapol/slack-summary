# Slack direct message summary with AI
## Requirement
- python3
- slack app user token (https://api.slack.com/start/quickstart)
- One of
  - ollama for local LLM (https://ollama.com/)
  - OpenAi api key

## Install requirements
```bash
pip install -r requirements.txt
```

## Create personal configuration file
Create a configuration file name `config.yaml` with template from `config-template.yaml`
```yaml
slack:
  token: "<your_slack_token>"
  channels:
    any-channel: "any-channel-id"
    any-channel2: "any-channel-id2"

open-ai:
  api-key: "<your_openai_api_key>"
```

