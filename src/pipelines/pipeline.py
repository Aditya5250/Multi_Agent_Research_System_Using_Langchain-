# We will Now Connect the Agents and the tools (we will make pipeline)
from src.agents.agent import (
    build_search_agent,
    build_reader_agent,
    build_writer_chain,
    build_critic_chain,
    writer_chain,
    critic_chain,
)

def _extract_text(content) -> str:
    """Helper to guarantee agent message content is always parsed into clean readable string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(content)

def run_research_pipeline(topic: str, step_callback=None, model=None) -> dict:
    state = {}

    # Step 1: Search agent working
    print("\n" + "="*50)
    print("step 1 - search agent is working....")
    print("="*50)
    if step_callback:
        step_callback("search", "started", "Searching the web for recent and reliable information...")

    search_agent = build_search_agent(model=model)
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    tool_outputs = []
    for msg in search_result.get("messages", []):
        msg_type = type(msg).__name__
        if msg_type == "ToolMessage" or getattr(msg, "name", None) == "web_search":
            tool_outputs.append(_extract_text(msg.content))
        elif hasattr(msg, "tool_call_id") or "tool" in getattr(msg, "type", ""):
            tool_outputs.append(_extract_text(msg.content))

    ai_summary = _extract_text(search_result["messages"][-1].content)

    if tool_outputs:
        state["search_result"] = "\n\n".join(tool_outputs) + "\n\nAGENT SUMMARY:\n" + ai_summary
    else:
        state["search_result"] = ai_summary

    print("\n search result ", state['search_result'])
    if step_callback:
        step_callback("search", "completed", state["search_result"])

    # Step 2: Reader agent working
    print("\n"+"="*50)
    print("step 2 - reader agent is working....")
    print("="*50)
    if step_callback:
        step_callback("reader", "started", "Selecting the most relevant URL and scraping deeper content...")

    reader_agent = build_reader_agent(model=model)
    reader_result = reader_agent.invoke({
        "messages": [("user", 
                      f"Based on the following search results about: '{topic}', "
                      f"pick the most relevant URL and scrape it for deeper content.\n\n"
                      f"Search Results:\n{state['search_result'][:1200]}"
                     )]
    })

    raw_scraped = reader_result["messages"][-1].content
    state["scraped_content"] = _extract_text(raw_scraped)

    print("\nscraped content: \n", state["scraped_content"])
    if step_callback:
        step_callback("reader", "completed", state["scraped_content"])

    # Step 3: Writer agent drafting report
    print("\n"+"="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)
    if step_callback:
        step_callback("writer", "started", "Synthesizing gathered intelligence and composing the report...")

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    
    current_writer = build_writer_chain(model=model) if model else writer_chain
    state["report"] = current_writer.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report\n", state["report"])
    if step_callback:
        step_callback("writer", "completed", state["report"])

    # Step 4: Critic reviewing report
    print("\n"+"="*50)
    print("step 4 - Critic is reviewing the report ...")
    print("="*50)
    if step_callback:
        step_callback("critic", "started", "Critically auditing research accuracy, structure, and depth...")

    current_critic = build_critic_chain(model=model) if model else critic_chain
    state["feedback"] = current_critic.invoke({
        "report": state["report"]
    })

    print("\n critic report \n", state["feedback"])
    if step_callback:
        step_callback("critic", "completed", state["feedback"])

    return state