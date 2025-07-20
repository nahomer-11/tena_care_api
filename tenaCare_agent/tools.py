from langchain.tools import tool
from tenaCare_agent.retriver import rag_chain

@tool
def get_weather(Location: str) -> str:
    """
    Get the current weather for a given location.
    
    Args:
        Location (str): The name of the location to get the weather for.
    
    Returns:
        str: A string describing the current weather in the specified location.
    """
    # Placeholder implementation
    return f"The current weather in {Location} is sunny with a temperature of 25°C."

@tool
def find_nearby_healthcare(Location: str) -> str:
    """
    Find nearby healthcare facilities for a given location.
    
    Args:
        Location (str): The name of the location to search for healthcare facilities.
    
    Returns:
        str: A string listing nearby healthcare facilities in the specified location.
    """
    # Placeholder implementation
    return f"Nearby healthcare facilities in {Location} include Hospital, Pharmacy and Clinic."

@tool
def web_search(query: str) -> str:
    """
    Perform a web search for a given query.
    
    Args:
        query (str): The search query.
    
    Returns:
        str: A string containing the search results for the query.
    """
    # Placeholder implementation
    return f"Search results for '{query}': [Result 1, Result 2, Result 3]"

@tool 
def search_remedies_in_database(symptom: str) -> str:
    """
    Search for remedies in the database based on a symptom.
    
    Args:
        symptom (str): The symptom to search remedies for.
    
    Returns:
        str: A string listing remedies for the specified symptom.
    """
    # Placeholder implementation
    return f"Remedies for {symptom} include Rest, Hydration, and Over-the-counter medication."

@tool
def health_news(dummy: str) -> str:
    """
    Get the latest health news. This tool accepts a dummy input to comply with agent requirements.

    Args:
        dummy (str): Ignored input.

    Returns:
        str: A string containing the latest health news.
    """
    return "Latest health news: New vaccine approved for widespread use, breakthrough in cancer research."


@tool
def rag_search(query: str) -> str:
    """
    Perform a RAG (Retrieval-Augmented Generation) search for a given query.
    
    Args:
        query (str): The search query.
    
    Returns:
        str: A string containing the RAG search results for the query.
    """
    # Placeholder implementation
    return rag_chain.run(query)
    


def get_tools():
    return [
        get_weather,
        find_nearby_healthcare,
        web_search,
        search_remedies_in_database,
        health_news,
        rag_search,  # For now, this is mocked. Later real RAG.
    ]