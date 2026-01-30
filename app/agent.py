"""Financial coordinator: provide reasonable investment strategies."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from datetime import datetime, timezone

import google.genai.types as genai_types

from google.adk.planners import BuiltInPlanner

from app.config import config

from . import prompt
from .sub_agents.data_analyst import data_analyst_agent
from .sub_agents.execution_analyst import execution_analyst_agent
from .sub_agents.risk_analyst import risk_analyst_agent
from .sub_agents.trading_analyst import trading_analyst_agent


MODEL = "gemini-2.0-flash"


financial_coordinator = LlmAgent(
    name=config.internal_agent_name,
    model=config.model,
    # planner=BuiltInPlanner(
    #     thinking_config=genai_types.ThinkingConfig(include_thoughts=True)
    # ),
    description=(
        "An intelligent multiagent system that guide users through a structured process to receive financial "
        "advice by orchestrating a series of expert subagents. help them "
        "analyze a market ticker, develop trading strategies, define "
        "execution plans, and evaluate the overall risk."
    ),
    instruction=prompt.FINANCIAL_COORDINATOR_PROMPT,
    output_key="financial_coordinator_output",
    tools=[        
        AgentTool(agent=data_analyst_agent),
        AgentTool(agent=trading_analyst_agent),
        AgentTool(agent=execution_analyst_agent),
        AgentTool(agent=risk_analyst_agent),
    ],
)

root_agent = financial_coordinator