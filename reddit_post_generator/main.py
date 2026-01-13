# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""reddit-post-generator - A Bindu Agent."""

import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reddit import RedditTools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global agent team instance
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


def load_config() -> dict:
    """Load agent configuration from project root."""
    # Try multiple possible locations for agent_config.json
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory as main.py
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except (PermissionError, json.JSONDecodeError) as e:
                print(f"⚠️  Error reading {config_path}: {type(e).__name__}")
                continue
            except Exception as e:
                print(f"⚠️  Unexpected error reading {config_path}: {type(e).__name__}")
                continue

    # If no config found or readable, create a minimal default
    print("⚠️  No agent_config.json found, using default configuration")
    return {
        "name": "reddit-post-generator",
        "description": "Team of agents that research topics on the web and create posts for Reddit",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3776",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {"key": "OPENAI_API_KEY", "description": "OpenAI API key for LLM calls", "required": False},
            {"key": "OPENROUTER_API_KEY", "description": "OpenRouter API key for LLM calls", "required": False},
            {"key": "REDDIT_CLIENT_ID", "description": "Reddit API client ID", "required": True},
            {"key": "REDDIT_CLIENT_SECRET", "description": "Reddit API client secret", "required": True},
            {"key": "REDDIT_USERNAME", "description": "Reddit account username", "required": True},
            {"key": "REDDIT_PASSWORD", "description": "Reddit account password", "required": True},
            {"key": "REDDIT_USER_AGENT", "description": "Reddit API user agent string", "required": True},
        ],
    }


async def initialize_agent() -> None:
    """Initialize the Reddit post generator team with proper model and tools."""
    global agent

    # Get API keys from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")
    
    # Get Reddit API credentials
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    reddit_username = os.getenv("REDDIT_USERNAME")
    reddit_password = os.getenv("REDDIT_PASSWORD")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "RedditPostGenerator/1.0 by ParasChamoli")

    # Model selection logic (supports both OpenAI and OpenRouter)
    if openai_api_key:
        model = OpenAIChat(id="gpt-4o", api_key=openai_api_key)
        print("✅ Using OpenAI GPT-4o")
    elif openrouter_api_key:
        model = OpenRouter(
            id=model_name,
            api_key=openrouter_api_key,
            cache_response=True,
            supports_native_structured_outputs=True,
        )
        print(f"✅ Using OpenRouter model: {model_name}")
    else:
        error_msg = (
            "No API key provided. Set OPENAI_API_KEY or OPENROUTER_API_KEY environment variable.\n"
            "For OpenRouter: https://openrouter.ai/keys\n"
            "For OpenAI: https://platform.openai.com/api-keys"
        )
        raise ValueError(error_msg)

    # Check Reddit API credentials
    if not all([reddit_client_id, reddit_client_secret, reddit_username, reddit_password]):
        error_msg = (
            "Reddit API credentials missing. Set all required environment variables:\n"
            "REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD\n"
            "Get credentials from: https://www.reddit.com/prefs/apps"
        )
        raise ValueError(error_msg)

    # Create the main agent with both tools
    agent = Agent(
        name="Reddit Post Generator",
        model=model,
        tools=[
            DuckDuckGoTools(),
            RedditTools(
                client_id=reddit_client_id,
                client_secret=reddit_client_secret,
                username=reddit_username,
                password=reddit_password,
                user_agent=reddit_user_agent,
            ),
        ],
        description=dedent("""\
            A specialized agent that researches topics on the web and creates
            high-quality Reddit posts. Combines web research capabilities with
            Reddit posting expertise to deliver informative and engaging content
            tailored to specific subreddits.\
        """),
        instructions=dedent("""\
            You are a Reddit Post Generator with access to web search tools and
            Reddit posting capabilities. Follow this workflow:

            1. RESEARCH PHASE (Use DuckDuckGoTools):
               - Perform focused web searches using relevant keywords
               - Filter results for credibility and recency
               - Extract key information and main points
               - Verify facts from multiple sources when possible
               - Focus on authoritative and reliable sources

            2. CONTENT CREATION PHASE:
               - Organize researched information in a logical structure
               - Create attention-grabbing yet accurate titles
               - Format posts using proper Reddit markdown
               - Structure content for maximum readability
               - Add appropriate tags and flairs if required

            3. REDDIT POSTING PHASE (Use RedditTools):
               - Get information regarding the target subreddit
               - Follow subreddit-specific rules and guidelines
               - Ensure posts comply with Reddit's content policy
               - Avoid including links in the main post (use comments if needed)
               - Submit the post to the specified subreddit

            4. QUALITY ASSURANCE:
               - Verify all information is accurate and up-to-date
               - Ensure posts are informative, engaging, and add value to the community
               - Follow Reddit guidelines and community standards
               - Format the post for maximum readability and engagement

            Always coordinate between research and posting phases to ensure
            high-quality, community-focused content that follows all platform rules.\
        """),
        expected_output=dedent("""\
            # Reddit Post Generated Successfully

            ## Post Details
            - **Subreddit:** {subreddit_name}
            - **Title:** {post_title}
            - **Status:** {post_status}

            ## Post Content Preview
            {post_content_preview}

            ## Research Summary
            - **Sources Researched:** {source_count}
            - **Key Topics Covered:** {key_topics}
            - **Post Length:** {post_length} characters

            ## Next Steps
            1. Post has been submitted to r/{subreddit_name}
            2. Monitor post engagement and comments
            3. Be prepared to respond to community feedback

            ---
            Generated by Reddit Post Generator
            Post Created: {current_date}\
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
    print("✅ Reddit Post Generator initialized")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent
    if not agent:
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    # Run the agent and get response
    response = await agent.arun(messages)
    return response


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    # Lazy initialization on first call
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Reddit Post Generator...")
            await initialize_agent()
            _initialized = True

    # Run the async agent
    result = await run_agent(messages)
    return result


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Reddit Post Generator resources...")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="Bindu Reddit Post Generator Agent")
    
    parser.add_argument(
        "--openai-api-key",
        type=str,
        default=os.getenv("OPENAI_API_KEY"),
        help="OpenAI API key (env: OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-4o"),
        help="Model ID for OpenRouter (env: MODEL_NAME)",
    )
    parser.add_argument(
        "--reddit-client-id",
        type=str,
        default=os.getenv("REDDIT_CLIENT_ID"),
        help="Reddit API client ID (env: REDDIT_CLIENT_ID)",
    )
    parser.add_argument(
        "--reddit-client-secret",
        type=str,
        default=os.getenv("REDDIT_CLIENT_SECRET"),
        help="Reddit API client secret (env: REDDIT_CLIENT_SECRET)",
    )
    parser.add_argument(
        "--reddit-username",
        type=str,
        default=os.getenv("REDDIT_USERNAME"),
        help="Reddit account username (env: REDDIT_USERNAME)",
    )
    parser.add_argument(
        "--reddit-password",
        type=str,
        default=os.getenv("REDDIT_PASSWORD"),
        help="Reddit account password (env: REDDIT_PASSWORD)",
    )
    parser.add_argument(
        "--reddit-user-agent",
        type=str,
        default=os.getenv("REDDIT_USER_AGENT", "RedditPostGenerator/1.0 by ParasChamoli"),
        help="Reddit API user agent (env: REDDIT_USER_AGENT)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to agent_config.json (optional)",
    )
    
    return parser


def set_environment_variables(args) -> None:
    """Set environment variables from command-line arguments."""
    env_vars = {
        "OPENAI_API_KEY": args.openai_api_key,
        "OPENROUTER_API_KEY": args.openrouter_api_key,
        "MODEL_NAME": args.model,
        "REDDIT_CLIENT_ID": args.reddit_client_id,
        "REDDIT_CLIENT_SECRET": args.reddit_client_secret,
        "REDDIT_USERNAME": args.reddit_username,
        "REDDIT_PASSWORD": args.reddit_password,
        "REDDIT_USER_AGENT": args.reddit_user_agent,
    }
    
    for key, value in env_vars.items():
        if value:
            os.environ[key] = value


def run_agent_server(config: dict) -> None:
    """Run the agent server with the given configuration."""
    try:
        # Bindufy and start the agent server
        print("🚀 Starting Bindu Reddit Post Generator server...")
        print(f"🌐 Server will run on: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3776')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Reddit Post Generator stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup on exit
        asyncio.run(cleanup())


def main():
    """Run the main entry point for the Reddit Post Generator Agent."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Set environment variables from CLI args
    set_environment_variables(args)
    
    print("🤖 Reddit Post Generator - Web Research and Reddit Posting Agent")
    print("📝 Capabilities: Topic research, web search, Reddit post creation, community engagement")
    
    # Load configuration
    config = load_config()
    
    # Run the agent server
    run_agent_server(config)


if __name__ == "__main__":
    main()