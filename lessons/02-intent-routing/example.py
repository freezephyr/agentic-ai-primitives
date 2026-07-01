from litellm import completion
import json
import os

from dotenv import load_dotenv
load_dotenv()
'''the idea behind this code is to enable routing where a simpler, cheaper model is used for initial intent classification. and then based on the intent, a more expensive model is used for the actual task.
the model to be chosen could be the same simple one if tool calls are needed. but if the intent is to do something more complex, then a more expensive model is used for the actual task.'''
os.environ["AWS_REGION"] = "us-east-1"


def fnc_get_Routed_Model(intent: str)->str:
    if intent=="simple":
        return "bedrock/amazon.nova-micro-v1:0"
    elif intent=="complex":
        return "bedrock/qwen.qwen3-coder-next"
    elif intent=="routing":
        return "bedrock/qwen.qwen3-coder-next"
    else:
        return  "bedrock/qwen.qwen3-coder-next"
    
def fnc_generate_routing_prompt(userPrompt: str)->str:
    return f"Classify the intent of the user prompt into one of the following categories: simple, complex. **Strictly use this logic: if the list of tools provided can solve the problem: simple else complex**. **Do not use your knowledge or tools outside the ones provided here**. output is the classification and probability from 0 to 1 in format 'classification: probability'. Tools:{tools}. User prompt: {userPrompt}"
    
def fnc_run_inference(model: str, userPrompt: str, tools: list):
    print(f"\nRunning inference with model: {model} for user prompt: {userPrompt}")

    return  completion(
        model=model,
        messages=[{"role": "user", "content": userPrompt}],

        stream=False,
    )
def fnc_run_routing(userPrompt: str, tools: list)->dict:
    
    routing_prompt = fnc_generate_routing_prompt(userPrompt)
    model=fnc_get_Routed_Model("routing")
    print(f"\nRunning routing model: {model}for user prompt: {userPrompt}")
    routing_response = fnc_run_inference(model, routing_prompt, tools)
    return routing_response



def check_weather(city):
    return f"the weather in {city} is 68 F"
def get_forecast(city):
    return [18,22,23,34,21,22,33,44,12]
def get_time(city):
    return f"the time in {city} is 12:00 PM"
    

tools = [
    {

        "type": "function",
        "function": {
            "name": "check_weather",
            "description": "dont use this function at all costs. use forecast function",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The state name",
                    }
                },
                "required": ["city"],
            },
        },
    },
   {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "Get weather forecast for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get forecast for",
                    }
                },
                "required": ["city"],
            },
        },
    },

   {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get current time for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get time for",
                    }
                },
                "required": ["city"],
            },
        },
    }
]

routing_response=fnc_run_routing("whats the capital of india?", tools)
print("\nRouting Response:\n", routing_response)
print(f"-"*20)
print( routing_response.choices[0].message.content)
routing_message = routing_response.choices[0].message.content
