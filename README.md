# Claude Meta Ads Tool

A production-ready FastAPI service that integrates Meta Ad Library scraping with Claude AI for intelligent ad analysis.

## Features

- 🔍 **Meta Ad Library Scraping** - Search for ads by keyword using meta-ads-collector
- 🤖 **Claude AI Analysis** - Get intelligent insights from collected ads
- 🔧 **Tool Use API** - Seamlessly integrate with Claude's tool use capabilities
- 📊 **RESTful API** - Easy-to-use endpoints for ad collection and analysis
- 🔐 **Environment-based Configuration** - Secure credential management
- 📈 **Production Ready** - Includes error handling, logging, and rate limiting

## Quick Start

### Prerequisites

- Python 3.8+
- Anthropic API key (for Claude)
- Meta Ad Library access (no API key required for meta-ads-collector)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/helenpalev-cmyk/claude-meta-ads-tool.git
cd claude-meta-ads-tool
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Search Meta Ads
```bash
POST /api/v1/ads/search

Request:
{
  "query": "solar panels",
  "country": "US",
  "max_results": 10
}
```

### Analyze Ads with Claude
```bash
POST /api/v1/ads/analyze

Request:
{
  "query": "AI tools",
  "country": "US",
  "max_results": 5,
  "analysis_prompt": "Identify top marketing patterns"
}
```

### Health Check
```bash
GET /health
```

## Usage

```python
import requests

BASE_URL = "http://localhost:8000"

# Search for ads
response = requests.post(
    f"{BASE_URL}/api/v1/ads/search",
    json={"query": "cryptocurrency", "country": "US"}
)
print(response.json())
```

## Docker

```bash
docker-compose up
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT License
