# Travel Bot Documentation
The Travel Bot is a Python application that utilizes the ChatGPT language model to provide users with information and assistance related to travel. It is designed to engage in natural language conversations and help users with various travel-related queries, such as finding destinations, providing travel tips, suggesting itineraries, and more. This documentation outlines how to set up, configure, and use the Travel Bot.

## Table of Contents
### 1. [Introduction](#introduction)
### 2. [Installation](#installation)
### 3. [Configuration](#configuration)
### 4. [Usage](#usage)
### 5. [Contributions](#contributions)
## Introduction
 The Travel Bot is a conversational AI application built using the ChatGPT language model developed by OpenAI. Its primary purpose is to assist users with travel-related inquiries and engage in meaningful conversations to provide travel recommendations, tips, and information.
### Features
- Natural Language Understanding: The bot is trained to understand and respond to a wide range of travel-related queries in natural language.

- Destination Recommendations: The bot can suggest popular travel destinations based on user preferences.

- Travel Tips and Advice: Users can ask for travel tips, packing advice, best times to visit specific places, and more.

- Itinerary Suggestions: The bot can help users create travel itineraries by suggesting places to visit, activities to do, and the ideal duration for each location.

- Cultural and Local Information: Users can inquire about local customs, traditions, and cultural information for various destinations.

- Hotel Recommendations to stay based on input.
## Installation
### Prerequisites
- Python 3.6 or later
- OpenAI GPT-3 API Key (Sign up on the OpenAI website to obtain an API key)
- Textbase - Textbase is a framework for building chatbots using NLP and ML.
- Poetry

### Installation Steps

#### 1. Clone the repository from GitHub:
```
git clone https://github.com/deveshXm/TravelBot
poetry shell
poetry install
```

#### 2. Navigate to the project directory:
```
cd travel-bot
```

#### 3. Install Dependencies
```
poetry shell
poetry install
```
## Configuration

Before running the Travel Bot, you need to configure the API key for the OpenAI GPT-3 API, Airtable Key, Rapid API Key

Replace the following with API Keys in .env

```
OPENAI_API_KEY="openai_api_key"
AIRTABLE_API_KEY="airtable_api_key"
RAPID_API_KEY="rapid_api_key"
```

## Usage

### Running the Bot:
```
poetry run python textbase/textbase_cli.py test main.py
```
 Now go to http://localhost:4000 and start chatting with your bot! The bot will automatically reload when you change the code.

### User Interactions
Engage in natural language conversations with the bot. For example:

- "Can you suggest some popular travel destinations in New Delhi?"
- "Tell me about the best places to visit in Paris."
- "Help me plan a 5-day trip to Tokyo."

## Contributions
Contributions are welcome! Please open an issue or a pull request.


