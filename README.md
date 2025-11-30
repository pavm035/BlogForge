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

```text
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
├── pyproject.toml             # uv project configuration
└── requirements.txt           # Python dependencies
```

### Workflow

1. **Blog Agent**: Analyzes topic and decides whether to search or generate directly
2. **Search Node**: Performs Tavily web search if additional information is needed
3. **Writer Node**: Generates comprehensive blog content in markdown
4. **Validation Node**: Ensures content quality and completeness
5. **Translation Node**: Translates content to requested language (if not English)

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
```

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
     -H "Content-Type: application/json" \
     -d '{"topic": "FastAPI Tutorial"}'

# Generate Spanish blog
curl -X POST "http://localhost:8000/blog/" \
     -H "Content-Type: application/json" \
     -d '{"topic": "FastAPI Tutorial", "language": "es"}'
```

### Using Postman

**Method 1: Interactive Swagger UI (Easiest)**
1. Start the server: `uv run main.py`
2. Open browser: `http://localhost:8000/docs`
3. Click on **POST /blog/** endpoint
4. Click **"Try it out"** button
5. Edit the request body:
   ```json
   {
     "topic": "Your blog topic here",
     "language": "en"
   }
   ```
6. Click **"Execute"** button
7. View the response with generated blog content

**Method 2: Postman Desktop/Web App**
1. **Create New Request**
   - Method: `POST`
   - URL: `http://localhost:8000/blog/`

2. **Set Headers**
   - Click **Headers** tab
   - Add: `Content-Type: application/json`

3. **Set Request Body**
   - Click **Body** tab
   - Select **raw** and **JSON** format
   - Enter:
   ```json
   {
     "topic": "Introduction to FastAPI",
     "language": "en"
   }
   ```

4. **Send Request**
   - Click **Send** button
   - View response in the bottom panel

**Method 3: Import OpenAPI Schema (Advanced)**
1. In Postman, click **Import** button
2. Select **Link** tab
3. Enter: `http://localhost:8000/openapi.json`
4. Click **Continue** → **Import**
5. All endpoints will be auto-imported with examples

### Using Thunder Client (VS Code)

1. Install **Thunder Client** extension in VS Code
2. Click Thunder Client icon in sidebar
3. Click **New Request**
4. Set method to **POST** and URL to `http://localhost:8000/blog/`
5. Go to **Body** tab, select **JSON**
6. Enter request body and click **Send**

### Interactive Documentation

Visit **`http://localhost:8000/docs`** for the interactive Swagger UI documentation with built-in API testing.

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
| `AI_BASE_URL` | Custom API base URL. Required only for custom providers or OpenAI-compatible APIs. Standard providers (Groq, OpenAI, Anthropic) don't need this. | ❌ | `https://api.custom.com/v1` |
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
- Set `AI_BASE_URL` for OpenAI-compatible endpoints

## 🚀 Running the Application

### Development Mode

```bash
# Using uv (recommended)
uv run main.py

# Or using Python directly
python main.py
```

The application starts on:
- **Host**: `0.0.0.0` (accepts external connections)
- **Port**: `8000`
- **Docs**: `http://localhost:8000/docs`
- **OpenAPI**: `http://localhost:8000/openapi.json`

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

## 🎯 Development

### LangGraph Studio

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
- **`studio/`**: LangGraph Studio configuration

## 🛠️ Tech Stack

- **[Python 3.13+](https://www.python.org/)** - Modern Python with latest features
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance web framework
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Multi-agent workflow orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** - LLM application framework
- **[Pydantic v2](https://docs.pydantic.dev/)** - Data validation and settings management
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[uv](https://docs.astral.sh/uv/)** - Ultra-fast Python package installer
- **[Tavily](https://tavily.com/)** - AI-optimized search API

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Quick steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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