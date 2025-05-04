from ai_agent.agent import ScientificAgent

def test_query():
    agent = ScientificAgent()
    response = agent.query("Spiegami il transformer architecture")
    assert isinstance(response, str)
    print("Test superato:", response)