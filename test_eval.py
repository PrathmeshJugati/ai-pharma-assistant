import logging
logging.basicConfig(level=logging.ERROR)
from app.main import agent

def run_tests():
    queries = [
        "What is Glycomet GP?",
        "Give me substitutes for Glycomet GP",
        "Which one is the cheapest among them?"
    ]

    for q in queries:
        print(f"\n{'='*40}")
        print(f"QUERY: {q}")
        print(f"{'='*40}")
        try:
            res = agent.pharma_assistant(q)
            print(res)
        except Exception as e:
            print(f"Error: {e}")
            

if __name__ == "__main__":
    run_tests()
