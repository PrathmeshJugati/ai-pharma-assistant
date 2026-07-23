import sys
import asyncio
import logging
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.ERROR)
from app.main import agent

async def run_stream_test():
    query = "Give me substitutes for Glycomet GP"
    session_id = "test-stream-session"

    print("="*60)
    print(f"STREAMING TEST QUERY: '{query}'")
    print("="*60)

    try:
        print("\nStreaming tokens:\n")
        async for chunk in agent.pharma_assistant_stream(query, session_id):
            print(chunk, end="", flush=True)
        print("\n\nStream finished successfully!")
    except Exception as e:
        print(f"\nStream test error: {e}")

if __name__ == "__main__":
    asyncio.run(run_stream_test())
