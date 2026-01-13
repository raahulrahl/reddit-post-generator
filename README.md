<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Reddit Post Generator</h1>
<h3 align="center">AI Team for Web Research and Reddit Content Creation</h3>

<p align="center">
  <strong>Specialized agent team that researches topics and creates engaging Reddit posts</strong><br/>
  Combines web research capabilities with Reddit posting expertise for high-quality, community-focused content
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/reddit-post-generator/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/ParasChamoli/reddit-post-generator/main.yml?branch=main" alt="Build Status">
  </a>
  <a href="https://pypi.org/project/reddit-post-generator/">
    <img src="https://img.shields.io/pypi/v/reddit-post-generator" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version">
  <a href="https://github.com/ParasChamoli/reddit-post-generator/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ParasChamoli/reddit-post-generator" alt="License">
  </a>
</p>

---

## 🎯 What is Reddit Post Generator?

A team of specialized agents that work together to research topics on the web and create high-quality Reddit posts. Combines web research capabilities with Reddit posting expertise to deliver informative, engaging, and community-focused content tailored to specific subreddits.

### Key Features
*   **🔍 Web Research Team** - Comprehensive topic research using DuckDuckGo search
*   **📝 Reddit Posting Agent** - Specialized in crafting engaging Reddit content
*   **📊 Team Collaboration** - Coordinated workflow between research and posting agents
*   **⚖️ Rule Compliance** - Automated subreddit rule checking and compliance
*   **🎯 Community Focus** - Tailored content for specific subreddit communities
*   **📈 Engagement Optimization** - Posts designed for maximum community interaction
*   **⚡ Lazy Initialization** - Fast boot times, initializes on first request
*   **🔐 Secure API Handling** - No API keys required at startup

---

## 🛠️ Tools & Capabilities

### Built-in Tools
*   **DuckDuckGoTools** - Web search for comprehensive topic research
*   **RedditTools** - Reddit API integration for posting and community interaction
*   **Team Coordination** - Multi-agent collaboration for optimal results

### Team Workflow
1.  **Research Phase** - Web Searcher agent researches topic using multiple sources
2.  **Content Creation** - Information organized into logical structure
3.  **Rule Compliance** - Verify subreddit rules and Reddit content policy
4.  **Post Optimization** - Craft engaging titles and formatted content
5.  **Submission** - Reddit Agent posts to specified subreddit
6.  **Quality Assurance** - Post verification and engagement prediction

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. It takes 2 minutes and unlocks the full potential of your agent.

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ParasChamoli/reddit-post-generator.git
cd reddit-post-generator

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# Choose ONE LLM provider:
# OPENAI_API_KEY=sk-...      # For OpenAI GPT-4o
# OPENROUTER_API_KEY=sk-...  # For OpenRouter (cheaper alternative)

# REQUIRED: Add Reddit API credentials
# Get credentials from: https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=your_user_agent_string  # Format: "app_name/version by your_username"
```

### 3. Run Locally

```bash
# Start the Reddit post generator
python reddit_post_generator/main.py

# Or using uv
uv run python reddit_post_generator/main.py
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3776
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```env
# Choose ONE provider (both can be set, OpenAI takes priority)
OPENAI_API_KEY=sk-...      # OpenAI API key
OPENROUTER_API_KEY=sk-...  # OpenRouter API key (alternative)

# REQUIRED: Reddit API credentials
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=your_user_agent_string

# Optional
DEBUG=true                # Enable debug logging
MODEL_NAME=openai/gpt-4o  # Model selection (OpenRouter only)
```

### Port Configuration
Default port: `3776` (can be changed in `agent_config.json`)

---

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3776/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a post on web technologies and frameworks to focus in 2025 on the subreddit r/webdev"
      }
    ]
  }'
```

### Sample Generation Queries
*   "Research AI ethics and create a discussion post for r/Futurology"
*   "Generate an informative post about climate change for r/science"
*   "Create a programming tutorial post for r/learnprogramming"
*   "Research and post about gaming industry trends in r/gaming"
*   "Generate a discussion prompt about healthy habits for r/GetMotivated"

### Expected Output Format

```markdown
# Reddit Post Generated Successfully

## Post Details
- **Subreddit:** webdev
- **Title:** The Most Promising Web Technologies to Master in 2025
- **Status:** submitted

## Post Content Preview
After researching the latest trends and industry forecasts for 2025, here are the key web technologies worth focusing on...

## Research Summary
- **Sources Researched:** 8
- **Key Topics Covered:** frontend frameworks, backend technologies, devops tools
- **Post Length:** 1800 characters

## Compliance Check
✅ Subreddit rules passed
✅ Reddit content policy passed
✅ Community guidelines passed

## Engagement Prediction
- **Estimated upvotes:** 250
- **Expected comments:** 45
- **Controversy score:** 0.2/10
- **Discussion potential:** High

---

Generated by Reddit Post Generator Team
Post Created: 2026-01-13 14:30:00
Team Members: Web Searcher, Reddit Agent
```

---

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t reddit-post-generator .

# Run container
docker run -d \
  -p 3776:3776 \
  -e OPENAI_API_KEY=your_key_here \
  -e REDDIT_CLIENT_ID=your_client_id \
  -e REDDIT_CLIENT_SECRET=your_client_secret \
  -e REDDIT_USERNAME=your_reddit_username \
  -e REDDIT_PASSWORD=your_reddit_password \
  -e REDDIT_USER_AGENT=your_user_agent_string \
  --name reddit-post-generator \
  reddit-post-generator

# Check logs
docker logs -f reddit-post-generator
```

### Docker Compose (Recommended)
`docker-compose.yml`

```yaml
version: '3.8'
services:
  reddit-post-generator:
    build: .
    ports:
      - "3776:3776"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDDIT_CLIENT_ID=${REDDIT_CLIENT_ID}
      - REDDIT_CLIENT_SECRET=${REDDIT_CLIENT_SECRET}
      - REDDIT_USERNAME=${REDDIT_USERNAME}
      - REDDIT_PASSWORD=${REDDIT_PASSWORD}
      - REDDIT_USER_AGENT=${REDDIT_USER_AGENT}
    restart: unless-stopped
```

Run with Compose:
```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
reddit-post-generator/
├── reddit_post_generator/
│   ├── skills/
│   │   └── reddit-post-generator/
│   │       └── skill.yaml          # Skill configuration
│   ├── __init__.py                 # Package initialization
│   ├── __version__.py              # Version information
│   └── main.py                     # Main agent implementation
├── agent_config.json               # Bindu agent configuration
├── pyproject.toml                  # Python dependencies
├── Dockerfile.agent                # Multi-stage Docker build
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This documentation
├── .env.example                    # Environment template
└── tests/                          # Test files
    └── test_main.py
```

---

## 🔌 API Reference

### Health Check
```bash
GET http://localhost:3776/health
```
Response:
```json
{"status": "healthy", "agent": "Reddit Post Generator"}
```

### Chat Endpoint
```bash
POST http://localhost:3776/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your Reddit post generation query here"}
  ]
}
```

---

## 🧪 Testing

### Local Testing

```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with specific API key
OPENAI_API_KEY=test_key python -m pytest
```

### Integration Test

```bash
# Start agent
python reddit_post_generator/main.py &

# Test API endpoint
curl -X POST http://localhost:3776/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Create a post about AI for r/technology"}]}'
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

**"ModuleNotFoundError"**
```bash
uv sync --force
```

**"Port 3776 already in use"**
Change port in `agent_config.json` or kill the process:
```bash
lsof -ti:3776 | xargs kill -9
```

**"No API key provided"**
Check if `.env` exists and variable names match. Or set directly:
```bash
export OPENAI_API_KEY=your_key
```

**"Reddit API credentials missing"**
Ensure all 5 Reddit credentials are set in `.env`:
```bash
REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_USER_AGENT
```

**"Reddit API rate limit exceeded"**
The agent implements exponential backoff. Wait and try again.

**"Subreddit not found or private"**
Verify the subreddit exists and is public.

**"Authentication failed"**
Check Reddit credentials and ensure app is properly configured.

**Docker build fails**
```bash
docker system prune -a
docker-compose build --no-cache
```

---

## 📊 Dependencies

### Core Packages
*   **bindu** - Agent deployment framework
*   **agno** - AI agent framework
*   **openai** - OpenAI client
*   **praw** - Reddit API client
*   **ddgs** - DuckDuckGo search
*   **requests** - HTTP requests
*   **rich** - Console output
*   **python-dotenv** - Environment management

### Development Packages
*   **pytest** - Testing framework
*   **ruff** - Code formatting/linting
*   **pre-commit** - Git hooks

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository
2.  Create a feature branch: `git checkout -b feature/improvement`
3.  Make your changes following the code style
4.  Add tests for new functionality
5.  Commit with descriptive messages
6.  Push to your fork
7.  Open a Pull Request

**Code Style:**
*   Follow PEP 8 conventions
*   Use type hints where possible
*   Add docstrings for public functions
*   Keep functions focused and small

---

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Acknowledgments
*   **Developer:** Paras Chamoli
*   **Framework:** Bindu - Agent deployment platform
*   **Agent Framework:** Agno - AI agent toolkit
*   **Reddit API:** PRAW (Python Reddit API Wrapper)
*   **Search API:** DuckDuckGo Search

### 🔗 Useful Links
*   🌐 **Bindu Directory:** [bindus.directory](https://bindus.directory)
*   📚 **Bindu Docs:** [docs.getbindu.com](https://docs.getbindu.com)
*   🐙 **GitHub:** [github.com/ParasChamoli/reddit-post-generator](https://github.com/ParasChamoli/reddit-post-generator)
*   💬 **Discord:** Bindu Community
*   📱 **Reddit API:** [reddit.com/dev/api](https://www.reddit.com/dev/api)

---

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Empowering meaningful Reddit conversations through AI-powered content creation</em>
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/reddit-post-generator/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/ParasChamoli/reddit-post-generator/issues">🐛 Report Issues</a>
</p>

> **Note:** This agent follows the Bindu pattern with lazy initialization and secure API key handling. It boots without API keys and only fails at runtime if keys are needed but not provided. Always respect Reddit's API rate limits and content policies.
