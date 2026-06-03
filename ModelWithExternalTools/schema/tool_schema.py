# Defining schema for tool calling
tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "check_warehouse",
            "description": "Check the stock and price of an item in the warehouse.",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_name": {"type": "string"}
                },
                "required": ["device_name"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "apply_discount",
            "description": "Apply a discount to an item based on the number of years as a customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_name": {"type": "string"},
                    "years_as_customer": {"type": "integer"}
                },
                "required": ["device_name", "years_as_customer"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "Search the internet for the given query and return relevant information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name":"image_task",
            "description": "This function will take the path of image and prompt to give the response for that image according to users prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path":{"type": "list"},
                    "prompt": {"type": "string"}
                },
                "required": ['image_path','prompt']
            }
        }
    }
]




