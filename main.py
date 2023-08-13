import os
import hmac
import json
import openai
import hashlib
import textbase
import requests

from typing import List
from pyairtable import Api
from textbase.message import Message
from pyairtable.formulas import match

# Load your OpenAI API key
# or from environment variable:
openai.api_key = os.getenv("OPENAI_API_KEY")
airtable_api_key = os.getenv("AIRTABLE_API_KEY")
rapid_api_key = os.getenv("RAPID_API_KEY")
api = Api(airtable_api_key)
table = api.table("app1NxrJuXvS9wYxm", "travelBotTable")

SYSTEM_PROMPT = """You are ChatGPT, a professional Travel Bot designed to help you plan your perfect trip. To assist you effectively, I'll need some information. Please provide the details one at a time:

Prompt:
I am your dedicated Travel Bot, here to make your trip unforgettable! Let's start by selecting your destination. Where are you planning to travel? Whether it's the bustling streets of a city, a serene beach, or a scenic mountain getaway, I've got you covered. Just let me know where you're headed!
User Input: [Destination]

Prompt:
Great choice! Now, could you please specify the starting date of your trip? Knowing when you'll be embarking on your adventure will help me curate the best recommendations for you.
User Input: [Start Date]

Prompt:
Thank you! How about the duration of your trip? Please provide me with the end date. This will help me suggest activities and places to visit based on the length of your stay.
User Input: [End Date]

Prompt:
Perfect. To ensure I suggest activities that align with your preferences, could you please specify your budget range for this trip? Whether you're looking for a luxurious experience or aiming to keep things budget-friendly, I'll tailor my recommendations accordingly.
User Input: [Budget Range]

Prompt:
Got it! What type of trip are you planning? Whether it's a romantic getaway, a family vacation, an adventurous solo expedition, or anything in between, knowing your travel style will help me provide you with the most suitable suggestions.
User Input: [Type of Trip]

Prompt:
Last but not least, let's talk about the number of travelers. How many people will be joining you on this exciting journey? Knowing the group size will help me suggest accommodations and activities that can comfortably accommodate everyone.
User Input: [Number of Travelers]

Now that I have all the necessary details, I'll use this information to craft personalized recommendations for places to visit, modes of transportation, and much more. Let's make this trip extraordinary!"""

# Hash Creating Function
def generate_hash(input_data):
    hmac_object = hmac.new(
        "most secret key ever".encode("utf-8"),
        input_data.encode("utf-8"),
        hashlib.sha256,
    )
    return hmac_object.hexdigest()


# Get Hotels Details
def get_hotel_details(city, startDate, endDate, guestQty):
    url = "https://best-booking-com-hotel.p.rapidapi.com/booking/best-accommodation"
    querystring = {"cityName":city,"countryName":"India"}
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "best-booking-com-hotel.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()
    # data = '{"name":"EastSeven Berlin","link":"https://www.booking.com/hotel/de/eastseven-berlin-hostel-berlin1.de.html?aid=1938431","rating":9.1}'
    # return json.loads(data)


@textbase.chatbot("health-bot")
def on_message(message_history: List[Message], state: dict = None):
    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    functions = [
        {
            "name": "get_trip_details",
            "description": "Get Trip Details for the user based on inputs",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "city in which trip ends",
                    },
                    "trip start date": {
                        "type": "string",
                        "description": "Date on which trip starts",
                    },
                    "trip end date": {
                        "type": "string",
                        "description": "Date on which trip ends",
                    },
                    "trip budget": {
                        "type": "string",
                        "description": "Budget of the trip",
                    },
                    "trip type": {
                        "type": "string",
                        "description": "Type of the trip eg Business, Family or Friends.",
                    },
                    "number of travelers": {
                        "type": "string",
                        "description": "Number of people that will travel",
                    },
                },
                "required": [
                    "destination",
                    "trip start date",
                    "trip end date",
                    "trip budget",
                    "number of travelers",
                ],
            },
        }
    ]

    # Generate Response use Chat Completion
    response = openai.ChatCompletion.create(
        temperature=0.7,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *map(dict, message_history),
        ],
        functions=functions,
        function_call="auto",
        model="gpt-3.5-turbo",
    )

    if response["choices"][0]["finish_reason"] == "function_call":
        # generate second response if all the necessary details are fetched from user
        data = json.loads(
            response["choices"][0]["message"]["function_call"]["arguments"]
        )
        city = data["destination"]
        startDate = data["trip start date"]
        endDate = data["trip end date"]
        guestQty = data["number of travelers"]
        
        # Generating Unique has for each response
        hash = generate_hash(city + startDate + endDate + guestQty)
        
        # If the prompt was used before then fetch the Record from Database otherwise create new Record
        try:
            isPromptPresent = table.first(formula=match({"id": hash}))
            return isPromptPresent["fields"]["message"]
        except:
            hotels = get_hotel_details(city, startDate, endDate, guestQty)
            second_response = openai.ChatCompletion.create(
                temperature=0.7,
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *map(dict, message_history),
                ],
                model="gpt-3.5-turbo",
            )

            final_response = (
                second_response["choices"][0]["message"]["content"]
                + "\n \n"
                + "Suggested Hotels for you to Book : "
                + "\n \n"
                + "Name : "
                + hotels["name"]
                + "\n \n"
                + "Link : "
                + hotels["link"]
                + "\n \n"
                + "Rating : "
                + str(hotels["rating"])
            )
            table.create({"id": hash, "message": str(final_response)})
            return final_response
    else:
        return response["choices"][0]["message"]["content"]
