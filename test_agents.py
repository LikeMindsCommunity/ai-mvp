from backend.app.core.agents.agent_registry import AgentRegistry
from backend.app.core.agents.query_understanding_agent import QueryUnderstandingAgent
from backend.app.core.agents.context_retrieval_agent import ContextRetrievalAgent
from backend.app.core.agents.response_generation_agent import ResponseGenerationAgent

def test_agent_registry():
    print("Testing AgentRegistry...")
    
    # Create registry
    registry = AgentRegistry()
    
    # Create agents
    query_agent = registry.create_agent(QueryUnderstandingAgent, name="query_understanding_agent")
    retrieval_agent = registry.create_agent(ContextRetrievalAgent, name="context_retrieval_agent")
    response_agent = registry.create_agent(ResponseGenerationAgent, name="response_generation_agent")
    
    print(f"Created agents: {registry.registered_agents}")
    print("Test completed successfully!")

if __name__ == "__main__":
    test_agent_registry() 