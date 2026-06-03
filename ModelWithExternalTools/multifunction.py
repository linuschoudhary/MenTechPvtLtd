import ollama
from tool_schema import tool_schema
from netCalling import search_internet
from datetime import datetime
from dummyFunctions import check_warehouse,apply_discount



available_tools = {
    "search_internet": search_internet,
    "check_warehouse" : check_warehouse,
    "apply_discount" : apply_discount
}



memory = ""

while True:

  # Calling the LLM with tool schema
  def call_model(message):
    global memory

    response = ollama.chat(
        model="qwen3.5:9b",
        messages=message,
        tools=tool_schema
    )

    response_message = response["message"]
    print(f"LLM Response:\n{response_message}")

    if response_message.get("tool_calls"):
        for tool_call in response_message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            print(f"\nCalling tool: {tool_name} with arguments: {[tool_args[args] for args in tool_args]}")

            if tool_name in available_tools:
              result = available_tools[tool_name](**tool_args)
              print(f"{result}\n\n\n\n\n\n")
              
              message.append(response_message)
              message.append(
                  {"role": "tool", "content": str(result)})
            #   message.append(
            #       {"role": "system", "content": """You are an article extraction system.
            #       Task:
            #       - Extract only real article titles and summaries
            #       - Ignore menus, ads, navigation text, and other non-article content
            #       - summarize with main points from available context."""}
            #   )


        # Get final response from LLM after tool calls
        print("\n\nModel is generating final Response.")
        final_response = ollama.chat(
            model="qwen3.5:9b",
            messages=message
        )

        memory += final_response["message"]["content"]
        print(f"Final LLM Response:\n{final_response['message']['content']}")
    else:
        memory += response_message.content

  user_query = input("Enter Your Query:\n")
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
