import requests
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_exchange(amount, currency_from, currency_to):
    response = requests.get("https://open.er-api.com/v6/latest/" + currency_from)
    exchange_rate = response.json()["rates"][currency_to]
    return amount*exchange_rate

functions = [
    {
        "name": "get_currency_exchange",
        "description": "Calculate the exchange by given currencies",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "The amount of the currency",
                },
                "currency_from": {"type": "string", "enum": ["USD", "EUR", "GBP"]},
                "currency_to": {"type": "string", "enum": ["USD", "EUR", "GBP"]}
            },
            "required": ["amount", "currency_from", "currency_to"],
        },
    }
]

messages = [{"role": "user", "content": "How much is 100 usd in euro?"}]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=functions,
    function_call="auto"
)

response_message = response["choices"][0]["message"]

if response_message.get("function_call"):
    available_functions = {
        "get_currency_exchange": get_currency_exchange,
    }
    function_name = response_message["function_call"]["name"]
    function_to_call = available_functions[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])
    function_response = function_to_call(
        amount=function_args.get("amount"),
        currency_from=function_args.get("currency_from"),
        currency_to=function_args.get("currency_to")
    )
    print(function_response)
