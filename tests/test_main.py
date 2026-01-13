"""Tests for the Reddit Post Generator Agent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from reddit_post_generator.main import handler


@pytest.mark.asyncio
async def test_handler_returns_response():
    """Test that handler accepts messages and returns a response."""
    messages = [{"role": "user", "content": "Create a Reddit post about AI"}]

    # Mock the run_agent function to return a mock response
    mock_response = MagicMock()
    mock_response.run_id = "test-run-id"
    mock_response.status = "COMPLETED"
    mock_response.content = "Reddit post created successfully"

    # Mock _initialized to skip initialization and run_agent to return our mock
    with (
        patch("reddit_post_generator.main._initialized", True),
        patch(
            "reddit_post_generator.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        result = await handler(messages)

    # Verify we get a result back
    assert result is not None
    assert result.run_id == "test-run-id"
    assert result.status == "COMPLETED"
    assert result.content == "Reddit post created successfully"


@pytest.mark.asyncio
async def test_handler_with_multiple_messages():
    """Test that handler processes multiple messages correctly."""
    messages = [
        {"role": "system", "content": "You are a Reddit post generator."},
        {"role": "user", "content": "Create a post about web development for r/webdev"},
    ]

    mock_response = MagicMock()
    mock_response.run_id = "test-run-id-2"
    mock_response.content = "Web development post generated"

    with (
        patch("reddit_post_generator.main._initialized", True),
        patch(
            "reddit_post_generator.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_run,
    ):
        result = await handler(messages)

    # Verify run_agent was called
    mock_run.assert_called_once_with(messages)
    assert result is not None
    assert result.run_id == "test-run-id-2"
    assert result.content == "Web development post generated"


@pytest.mark.asyncio
async def test_handler_initialization():
    """Test that handler initializes on first call."""
    messages = [{"role": "user", "content": "Test Reddit post creation"}]

    mock_response = MagicMock()
    mock_response.run_id = "init-run-id"
    mock_response.status = "COMPLETED"

    # Start with _initialized as False to test initialization path
    with (
        patch("reddit_post_generator.main._initialized", False),
        patch("reddit_post_generator.main.initialize_agent", new_callable=AsyncMock) as mock_init,
        patch(
            "reddit_post_generator.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_run,
        patch("reddit_post_generator.main._init_lock", new_callable=MagicMock()) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        result = await handler(messages)

        # Verify initialization was called
        mock_init.assert_called_once()
        # Verify run_agent was called
        mock_run.assert_called_once_with(messages)
        # Verify we got a result
        assert result is not None
        assert result.run_id == "init-run-id"


@pytest.mark.asyncio
async def test_handler_race_condition_prevention():
    """Test that handler prevents race conditions with initialization lock."""
    messages = [{"role": "user", "content": "Test race condition"}]

    mock_response = MagicMock()
    mock_response.run_id = "race-run-id"

    # Test with multiple concurrent calls
    with (
        patch("reddit_post_generator.main._initialized", False),
        patch("reddit_post_generator.main.initialize_agent", new_callable=AsyncMock) as mock_init,
        patch(
            "reddit_post_generator.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
        patch("reddit_post_generator.main._init_lock", new_callable=MagicMock()) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        # Call handler twice to ensure lock is used
        await handler(messages)
        await handler(messages)

        # Verify initialize_agent was called only once (due to lock)
        mock_init.assert_called_once()


@pytest.mark.asyncio
async def test_handler_with_reddit_post_creation():
    """Test that handler can process a Reddit post creation query."""
    messages = [
        {
            "role": "user",
            "content": "Create a post on web technologies and frameworks to focus in 2025 on the subreddit r/webdev",
        }
    ]

    mock_response = MagicMock()
    mock_response.run_id = "reddit-run-id"
    mock_response.content = "Reddit post created for r/webdev"
    mock_response.post_details = {
        "subreddit": "webdev",
        "title": "Web Technologies to Focus on in 2025",
        "status": "submitted",
    }

    with (
        patch("reddit_post_generator.main._initialized", True),
        patch(
            "reddit_post_generator.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        result = await handler(messages)

    assert result is not None
    assert result.run_id == "reddit-run-id"
    assert result.content == "Reddit post created for r/webdev"
    assert result.post_details == {
        "subreddit": "webdev",
        "title": "Web Technologies to Focus on in 2025",
        "status": "submitted",
    }


@pytest.mark.asyncio
async def test_handler_with_research_and_post_query():
    """Test that handler can process a combined research and post query."""
    messages = [
        {
            "role": "user",
            "content": "Research AI ethics and create a discussion post for r/Futurology",
        }
    ]

    mock_response = MagicMock()
    mock_response.run_id = "research-post-run-id"
    mock_response.content = "AI ethics research completed and post created"
    mock_response.research_summary = {
        "sources_used": 6,
        "key_findings": ["ethical_frameworks", "regulation_challenges", "future_implications"],
    }
    mock_response.post_details = {
        "subreddit": "Futurology",
        "title": "The Ethical Implications of Advanced AI Systems",
        "engagement_prediction": {"estimated_upvotes": 300, "expected_comments": 75},
    }

    with (
        patch("reddit_post_generator.main._initialized", True),
        patch(
            "reddit_post_generator.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        result = await handler(messages)

    assert result is not None
    assert result.run_id == "research-post-run-id"
    assert result.content == "AI ethics research completed and post created"
    assert result.research_summary == {
        "sources_used": 6,
        "key_findings": ["ethical_frameworks", "regulation_challenges", "future_implications"],
    }
    assert result.post_details == {
        "subreddit": "Futurology",
        "title": "The Ethical Implications of Advanced AI Systems",
        "engagement_prediction": {"estimated_upvotes": 300, "expected_comments": 75},
    }
