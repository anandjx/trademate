
print("DEBUG: Script Start")
import asyncio
import os
import sys

print("DEBUG: Loading dotenv...")
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="app/.env")

print("DEBUG: Importing google.adk...")
from google.adk import Runner
from google.adk.agents import LlmAgent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.tools import google_search
from google.genai import types 
from app.sub_agents.market_analyst import prompt

from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService

print("DEBUG: Imports Complete")

# Force using the user's preferred model
MODEL = "gemini-2.0-flash"

async def run_debug():
    print(f"DEBUG: Initializing Market Analyst with {MODEL}...")
    
    agent = LlmAgent(
        model=MODEL,
        name="market_analyst_agent",
        instruction=prompt.MARKET_ANALYST_PROMPT,
        tools=[google_search],
        output_key="market_analyst_report",
    )

    print("DEBUG: Creating Runner and Services...")
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name="trademate_debug",
        session_service=session_service,
        artifact_service=InMemoryArtifactService(),
        memory_service=InMemoryMemoryService(),
        credential_service=InMemoryCredentialService(),
    )

    # Create Session
    session_id = "debug_session_001"
    user_id = "debug_user"
    app_name = "trademate_debug"
    
    # Ensure session exists (InMemorySessionService handles get_or_create logic via get_or_create_session usually, but we can just assume session_id is accepted generally or create it)
    # Actually InMemorySessionService needs creation maybe?
    # Runner handles it internally? No, adk_agent passes session_id.
    
    # We will try to rely on Runner/Service handling it or pre-create if needed.
    # But Runner.run_async likely manages the session via service if we provided one.
    # Explicitly creating session:
    try:
         await session_service.create_session(session_id=session_id, app_name=app_name, user_id=user_id)
    except:
         pass # Already exists

    # Prepare input
    # adk_agent passes: user_id, session_id, new_message, run_config
    
    new_message = types.Content(
        role="user",
        parts=[types.Part(text="Analyze AAPL stock. Provide detailed report.")]
    )
    
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    print("DEBUG: Calling runner.run_async...")
    try:
        run_kwargs = {
            "user_id": user_id,
            "session_id": session_id,
            "new_message": new_message,
            "run_config": run_config
        }
        
        async for event in runner.run_async(**run_kwargs):
            # Inspect event type
            # print(f"Event: {type(event)}")
            
            # Check for content
            if hasattr(event, 'content') and event.content:
                 if hasattr(event.content, 'parts'):
                     for part in event.content.parts:
                         if hasattr(part, 'text') and part.text:
                             print(f"DEBUG: Content Part: {part.text[:200]}...") 
                         if hasattr(part, 'function_call') and part.function_call:
                             print(f"DEBUG: Tool Call: {part.function_call.name}")
            
    except Exception as e:
        print(f"\nERROR: Agent Failed during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_debug())
