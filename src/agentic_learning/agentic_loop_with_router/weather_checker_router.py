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
#        tools=tools,
#        tool_choice="auto",
       
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

'''
messages=[{"role": "user", "content": "whats the weather in new delhi and new york?"}]
response = completion(
    model="bedrock/qwen.qwen3-coder-next",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    stream=False,
)



print("\nLLM Response1:\n", response)

response_message=response["choices"][0]["message"]
tool_calls=response_message.get("tool_calls", [])
for tool_call in tool_calls:
    tool_name=tool_call.function.name
    print (f"\nTool Call: {tool_name}")
    messages.append(
{"role": "tool", "name": tool_name, "content": json.dumps(tool_call.function.arguments)}
    )


response2 = completion(
    model="bedrock/qwen.qwen3-coder-next",
    messages=messages)
print("\nLLM Response2:\n", response2)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls

print("\nLength of tool calls", len(tool_calls))

if tool_calls:
    # Step 3: call the function and append the tool result to the conversation.
    available_functions = {
        "check_weather": check_weather,
    }
    messages.append(response_message)

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        function_to_call = available_functions.get(function_name)
        if function_to_call is None:
            raise ValueError(f"Unknown function: {function_name}")

        function_output = function_to_call(**function_args)
        messages.append(
            {
                "role": "tool",
                "name": function_name,
                "tool_call_id": tool_call.id,
                "content": function_output,
            }
        )

    second_response = completion(
        model="bedrock/qwen.qwen3-coder-next",
        messages=messages,
        tools=tools,
    )
    print("\nSecond LLM response:\n", second_response)
    print("Second response message:\n", second_response.choices[0].message.content)

messages=[{"role": "user", "content": "whats the weather in new delhi and new york? and what is the time in those cities?"}]

messages.append(
    {"role": "user", "content": "whats 2+2?"
    }
)

third_response = completion(
model="bedrock/qwen.qwen3-coder-next",
messages=messages,
tools=tools,
)
print("\nThird LLM response:\n", third_response)
print("Third response message:\n", third_response.choices[0].message.content)
'''