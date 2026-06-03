import ollama
from schema.tool_schema import tool_schema
from datetime import datetime
from tools.tool_calling import call_tools


memory = ""

while True:

  # Calling the LLM with tool schema
  def call_model(message):
    global memory

    response = ollama.chat(
        model="qwen3.5:4b",
        messages=message,
        tools=tool_schema
    )

    response_message = response["message"]
    print(f"LLM Response: {response_message['content']}")

    if response_message.get("tool_calls"):
        message,result = call_tools(response_message,message)

        if result:
        # Get final response from LLM after tool calls
            print("\nModel is generating final Response for you, please wait...")
            final_response = ollama.chat(
                model="qwen3.5:4b",
                messages=message
            )

            memory += final_response["message"]["content"]
            print(f"{final_response['message']['content']}")
        else:
           print("-----------------------------------------------")
    else:
        memory += response_message.content

  user_query = input("\nEnter Your Query: ")
  memory += user_query
  message = [
      {
          "role": "user",
          "content": user_query
      },
      {"role":"system","content": str(datetime.now())},
      {"role":"system","content":memory}
  ]

  call_model(message=message)
