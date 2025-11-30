# 🚀 BlogForge

AI-powered blog generation service built with FastAPI, LangGraph, and modern Python architecture. Generate high-quality, comprehensive blog posts from simple topics using state-of-the-art language models.

## ✨ Features

- **🤖 AI Blog Generation**: Create comprehensive, well-structured blog posts from simple topics
- **🔄 Multi-Provider Support**: Works with Groq, OpenAI, Anthropic, and custom APIs
- **🌍 Multi-language Support**: Generate and translate content in multiple languages
- **🔍 Web Search Integration**: Automatic Tavily search for up-to-date information
- **⚡ RESTful API**: FastAPI-based web service with automatic OpenAPI documentation
- **🎨 Visual Debugging**: LangGraph Studio integration for workflow visualization
- **🏗️ Production Ready**: Clean architecture with proper configuration management
## 🏗️ Architecture

BlogForge uses a multi-node LangGraph workflow for intelligent blog generation:

```
BlogForge/
├── src/
│   ├── ai/                    # AI workflow components
│   │   ├── agent/             # Blog generation agent orchestration
│   │   ├── graph/             # LangGraph workflow builder
│   │   ├── llm/               # LLM manager and configuration
│   │   ├── node/              # Workflow nodes (search, write, translate, validate)
│   │   ├── state/             # State management for workflow
│   │   └── model/             # Data models for search and content
│   ├── api/                   # FastAPI endpoints and API managers
│   ├── core/                  # Core utilities and session management
│   └── app.py                 # Application server configuration
├── studio/                    # LangGraph Studio configuration
├── main.py                    # Application entry point
├── server.py                  # Alternative server with dev/prod modes
## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** (recommended) or Python 3.11+
- **API Keys**:
  - Groq API key (recommended, free tier available) OR OpenAI/Anthropic key
  - Tavily API key (for web search, free tier available)
- **Optional**: [uv](https://docs.astral.sh/uv/) package manager (recommended for faster installs)

### Installation

#### Option 1: Using uv (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/pavm035/BlogForge.git
cd BlogForge

# 2. Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies (uv automatically creates venv)
uv sync

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys (see Configuration section below)

# 5. Run the application
uv run main.py
```

#### Option 2: Using pip

```bash
# 1. Clone the repository
git clone https://github.com/pavm035/BlogForge.git
cd BlogForge

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run the application
python main.py
## 📖 API Usage

### Generate Blog (English)

**Endpoint:** `POST /blog/`

**Request:**
```json
{
  "topic": "Introduction to Machine Learning"
}
```

**Response:**
```json
{
  "topic": "Introduction to Machine Learning",
  "blog": {
    "title": "# Introduction to Machine Learning: A Comprehensive Guide",
    "content": "## Overview\n\nMachine learning is a subset of artificial intelligence...\n\n## Key Concepts\n\n..."
  }
}
```

### Generate Blog (Multi-language)

**Request:**
```json
{
  "topic": "Introduction to Machine Learning",
  "language": "es"
}
```

**Supported Languages:**
- `en` - English (default)
- `es` - Spanish
- `fr` - French
- `de` - German
- `hi` - Hindi
- `te` - Telugu
- And more...

### Using cURL

```bash
# Generate English blog
curl -X POST "http://localhost:8000/blog/" \
## 🔧 Configuration

### Environment Variables

Edit your `.env` file with the following variables:

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key | ✅ | `gsk_...` |
| `TAVILY_API_KEY` | Tavily search API key | ✅ | `tvly-...` |
| `MODEL_NAME` | AI model name | ✅ | `llama-3.3-70b-versatile` |
| `MODEL_PROVIDER` | Provider name | ✅ | `groq`, `openai`, `anthropic` |
| `AI_API_KEY` | Alias for your provider's API key | ✅ | Same as GROQ_API_KEY |
| `AI_BASE_URL` | Custom API endpoint | ❌ | `https://api.custom.com/v1` |
| `LANGSMITH_API_KEY` | LangSmith tracing | ❌ | `ls__...` |
| `LANGSMITH_TRACING` | Enable LangSmith tracing | ❌ | `true` or `false` |
| `LANGSMITH_PROJECT` | LangSmith project name | ❌ | `BlogForge` |

### Supported Providers & Models

#### Groq (Recommended)
- **llama-3.3-70b-versatile** - Latest Llama model, excellent for blog generation
- **mixtral-8x7b-32768** - Good balance of speed and quality
- **gemma2-9b-it** - Fast and efficient for shorter content

#### OpenAI
- **gpt-4-turbo** - Highest quality, best for complex topics
- **gpt-3.5-turbo** - Fast and cost-effective

#### Anthropic
- **claude-3-opus** - Highest quality
- **claude-3-sonnet** - Balanced performance

#### Custom APIs
## 🚀 Running the Application

### Development Mode

```bash
# Using uv (recommended)
uv run main.py

# Or using Python directly
## 🧪 Testing

### Quick Test

```bash
# 1. Start the server in one terminal
uv run main.py

# 2. Test in another terminal
curl -X POST "http://localhost:8000/blog/" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Python Web Development", "language": "en"}'
```

### Test Different Languages

```bash
# Spanish
curl -X POST "http://localhost:8000/blog/" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Desarrollo Web con Python", "language": "es"}'

# French
curl -X POST "http://localhost:8000/blog/" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Développement Web Python", "language": "fr"}'
```

### Using Postman or Thunder Client

1. Import the OpenAPI schema from `http://localhost:8000/openapi.json`
2. Use the interactive docs at `http://localhost:8000/docs`

The application starts on:
- **Host**: `0.0.0.0` (accepts external connections)
- **Port**: `8000`
- **Docs**: `http://localhost:8000/docs`
- **OpenAPI**: `http://localhost:8000/openapi.json`
For visual debugging and development:

```bash
cd studio
langgraph dev
```

This opens the LangGraph Studio interface for visualizing and debugging your blog generation workflow.

### Project Structure

- **`src/ai/`**: Core AI components using LangGraph
- **`src/api/`**: FastAPI endpoints and API management
- **`src/core/`**: Application configuration and utilities
## 🛠️ Tech Stack

- **[Python 3.13+](https://www.python.org/)** - Modern Python with latest features
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance web framework
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Multi-agent workflow orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** - LLM application framework
- **[Pydantic v2](https://docs.pydantic.dev/)** - Data validation and settings management
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[uv](https://docs.astral.sh/uv/)** - Ultra-fast Python package installer
- **[Tavily](https://tavily.com/)** - AI-optimized search API

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for powerful workflow orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Groq](https://groq.com/) for lightning-fast LLM inference
- [Tavily](https://tavily.com/) for AI-optimized search capabilities

## 📞 Support

- 🐛 Create an [issue](https://github.com/pavm035/BlogForge/issues) for bug reports
- 💬 Start a [discussion](https://github.com/pavm035/BlogForge/discussions) for questions
- ⭐ Star the repo if you find it useful!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Python, FastAPI, LangGraph, and modern AI technologies**
### Supported Providers

- **Groq**: Fast inference with open models
- **OpenAI**: GPT-3.5, GPT-4, and newer models
- **Anthropic**: Claude models
- **Custom APIs**: Any OpenAI-compatible API

## 🧪 Testing

### Manual Testing

```bash
# Test the API
curl -X POST "http://localhost:8000/blog/" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Python Web Development"}'
```

### Using Postman

Import the API schema from `http://localhost:8000/openapi.json` for testing with Postman.

## 🚀 Deployment

### Development

```bash
python main.py
```

### Production

```bash
# Using the built-in production server
python server.py prod
```

### Docker

```bash
# Build image
docker build -t blogforge .

# Run container
docker run -p 8000:8000 --env-file .env blogforge
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation

## 📞 Support

- Create an [issue](https://github.com/yourusername/blogforge/issues) for bug reports
- Start a [discussion](https://github.com/yourusername/blogforge/discussions) for questions

---

**Built with ❤️ using Python, FastAPI, and LangGraph**
