# MyChatBot

Welcome to the repository for MyChatBot! This repository contains the code for building your very own custom chatbot using ChatGPT with a custom knowledge base. The setup instructions provided here will guide you through the process of running the chatbot and the chat API.

## Setup for Chatbot

### Running with Poetry (Recommended)

To run the chatbot using Poetry, follow these steps:

1. Make sure you have Poetry installed. If not, you can follow [these instructions](https://www.notion.so/whereismytransporthq/Poetry-9e463bdb97504b0d99a919ec5072eaf7) to install it.

2. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/mychatbot.git
```

3. Navigate to the `/mychatbot/slack_bot` directory in your terminal:

```bash
cd mychatbot/slack_bot
```

4. Activate the virtual environment using Poetry:

```bash
poetry shell
```

5. Install the required dependencies:

```bash
poetry install
```

6. Run the chatbot application:

```bash
python src/app.py
```


## Setup for ChatAPI

To set up the ChatAPI, follow these steps:

1. Open the `app.py` file in the `/mychatbot/slack_bot/src` directory.

2. Locate the `launch_slackapp` function inside the `app.py` file.

3. Replace the `SLACK_APP_TOKEN` value with your Slack app token.

```python
SLACK_APP_TOKEN = "your-slack-app-token"
```

4. Save the changes to the `app.py` file.

5. Run the chat API:

```bash
python src/app.py
```
---


Feel free to explore and customize this repository to create your own custom chatbot with a knowledge base. For more detailed instructions and additional features, you can refer to the [original article](https://betterprogramming.pub/how-to-build-your-own-custom-chatgpt-with-custom-knowledge-base-4e61ad82427e).

If you encounter any issues or have questions, please don't hesitate to reach out to [your-email@example.com](mailto:your-email@example.com).

Happy bot-building!
 