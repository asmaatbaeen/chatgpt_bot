# mychatbot

<!-- ref https://betterprogramming.pub/how-to-build-your-own-custom-chatgpt-with-custom-knowledge-base-4e61ad82427e -->

## Setup for chatbot
### Running with Poetry (recommended)
To run with Poetry:
1. Ensure you have Poetry installed. Follow [these intructions](https://www.notion.so/whereismytransporthq/Poetry-9e463bdb97504b0d99a919ec5072eaf7) if needed.
2. Execure the following
```
cd /slack_bot
poetry shell
poetry install
python src/app.py
```
(Still need to add a start script, couldn't get it working)

### Running in docker
To run in docker:
1. Ensure you have docker installed
2. Go to the slack bot directory and run:
```
cd /slack_bot
docker build -t slackgpt_bot .
docker run slackgpt_bot
```


## Setup for chatAPI

TODO: add info here, not yet implemented