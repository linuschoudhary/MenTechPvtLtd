from tools.dummyFunctions import check_warehouse,apply_discount
from images.image import image_task
from duckduckgo.ddgsearch import search_internet

available_tools = {
    "search_internet": search_internet,
    "check_warehouse" : check_warehouse,
    "apply_discount" : apply_discount,
    "image_task": image_task
}



def call_tools(response_message,message):
        for tool_call in response_message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            
            print(f"Calling tool: {tool_name} with arguments: {[tool_args[args] for args in tool_args]}\n")

            if tool_name in available_tools:
                result = available_tools[tool_name](**tool_args)
                message.append(response_message)
                message.append(
                    {"role": "tool", "content": str(result)})
                
                # """useful if only want to work with news."""
                # message.append(
                #     {"role": "system", "content": """You are an article extraction system.
                #     Task:
                #     - Extract only real article titles and summaries
                #     - Ignore menus, ads, navigation text, and other non-article content
                #     - summarize with main points from available context."""}
                # )
        return message,result