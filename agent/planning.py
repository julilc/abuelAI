from config import openai_client, OPENAI_MODEL
from tools import netflix_search_tool, hbo_max_search_tool, prime_search_tool
from memory import store_chat_message, retrieve_session_history
import json

def tool_selector(user_input, session_history=None):
    messages = [
        {
            "role": "system",
            "content": (
                "Select the appropriate tool from the options below. Consider the full context of the conversation before deciding.\n\n"
                "Tools available:\n"
                "- netflix_search_tool: Retrieve context about Netflix.\n"
                "- hbo_max_search_tool: Retrieve context about HBO/MAX.\n"
                "- prime_search_tool: Retrieve context about Amazon Prime Video.\n"
                "- none: For general questions.\n\n"
                "Return only JSON: {\"tool\": \"selected_tool\", \"input\": \"your_query\"}"
            )
        }
    ]

    if session_history:
        messages.extend(session_history)

    messages.append({"role": "user", "content": user_input})

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages
    ).choices[0].message.content

    try:
        tool_call = json.loads(response)
    except json.JSONDecodeError:
        return "none", user_input

    tool = tool_call.get("tool", "none")
    tool_input = tool_call.get("input", user_input)

    return tool, tool_input


def generate_response(session_id: str, user_input: str) -> str:
    store_chat_message(session_id, "user", user_input)

    llm_input = []
    session_history = retrieve_session_history(session_id)
    llm_input.extend(session_history)

    user_message = {"role": "user", "content": user_input}
    llm_input.append(user_message)

    tool, tool_input = tool_selector(user_input, session_history)

    if tool in ['netflix_search_tool', 'hbo_max_search_tool', 'prime_search_tool']:
        if tool == 'netflix_search_tool':
            context = netflix_search_tool(tool_input)
        if tool == 'hbo_max_search_tool':
            context = hbo_max_search_tool(tool_input)
        if tool == 'prime_search_tool':
            context = prime_search_tool(tool_input)

        system_message_content = (
            f"Answer the user's question based on the retrieved context and conversation history.\n"
            f"Do not make up information. Use plain language. Ask for more information if needed.\n"
            f"Always ask which platform (Max/HBO, Netflix, Amazon Prime Video) the user is using.\n"
            f"If the user refers to a platform not supported by tools, say you cannot help.\n"
            f"Only state facts from context. If information is missing, say 'I DON'T KNOW'.\n\n"
            f"Context:\n{context}"
        )
        response = get_llm_response(llm_input, system_message_content)

    else:
        system_message_content = (
            "You are a helpful assistant for HBO/MAX, Netflix, and Amazon Prime Video. "
            "Use plain language. Ask for more information if needed. "
            "If the user refers to other platforms, say you cannot help."
        )
        response = get_llm_response(llm_input, system_message_content)

    store_chat_message(session_id, "system", response)
    return response


def get_llm_response(messages, system_message_content):
    system_message = {"role": "system", "content": system_message_content}

    if any(msg.get("role") == "system" for msg in messages):
        messages.append(system_message)
    else:
        messages = [system_message] + messages

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages
    ).choices[0].message.content

    return response
