def context_generate(context_list):
    final_context = ""
    for page in context_list:
        final_context += page.page_content
    return final_context