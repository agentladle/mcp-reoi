# AgentLadle MCP REOI

**中文** | [English](README.md)

A Model Context Protocol (MCP) server for Residual Operating Income (REOI) Valuation, built with Python and FastMCP.

> 📈 **Financial Data & Valuation Engine** — A professional quantitative analysis tool for Residual Operating Income modeling.

It enables AI assistants (like Claude, Cursor, etc.) to perform multi-stage residual income projections, discounting, and enterprise value bridging analysis via standardized data input interfaces.

## Features

- **1 Professional MCP Tool** providing comprehensive financial valuation capabilities.
- **Standardized REOI Framework**, incorporating base period analysis, forecast period discounting, and terminal value estimation.
- **Multi-stage Profit Forecasting**, allowing independent revenue growth rates and operating margins configuration for each year.
- **Smart Markdown Formatting**, returning not only precise valuation figures but also built-in markdown tables for elegant rendering inside LLM clients.
- **Zero Configuration Installation** — Add one line to your MCP client without cloning or manual setup.
- **Pure Python**, cross-platform (Windows / macOS / Linux).

## Prerequisites

- **Python 3.10+** — [Download Python](https://www.python.org/downloads/)
- **uv** — [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

> **Tip:** After installing uv, restart your terminal and MCP client (e.g., Claude Desktop) to ensure the `uv` command is recognized.

## Quick Start

Add the following to your MCP client configuration (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "agentladle-mcp-reoi": {
      "command": "uvx",
      "args": ["agentladle-mcp-reoi"]
    }
  }
}
```

That's it. `uvx` automatically downloads the package and its dependencies from PyPI — no cloning, manual installation, or path configuration required.

### Alternative: pip install

If you prefer managing the environment yourself:

```bash
pip install agentladle-mcp-reoi
```

Then configure:

```json
{
  "mcpServers": {
    "agentladle-mcp-reoi": {
      "command": "agentladle-mcp-reoi"
    }
  }
}
```

### Alternative: Run from Source (Local Dev)

Clone the repository and run directly:

```bash
git clone https://github.com/agentladle/mcp-reoi.git
```

Configure your MCP client:

```json
{
  "mcpServers": {
    "agentladle-mcp-reoi": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-reoi", "agentladle-mcp-reoi"]
    }
  }
}
```

Replace `/path/to/mcp-reoi` with the actual path to the cloned repository.

## Tool List

| # | Tool | Description |
|---|------|------|
| 1 | `reoi_valuation_model` | Residual Operating Income valuation model. Outputs value per share and detailed breakdown based on financial statements and assumptions. |

### Tool 1: `reoi_valuation_model`

Calculates enterprise equity value and suggested value per share by taking base period financial data and future forecast assumptions.

**Parameter List (`request` object)**

| Parameter | Type | Required | Description |
|------|------|------|------|
| `version` | string | | Version, default "1.0" |
| `ticker` | string | | Stock ticker |
| `companyName` | string | | Company Name |
| `currency` | string | | Currency, default "CNY" |
| `baseData` | object | ✅ | Base period financial data |
| `parameters` | object | ✅ | Valuation parameters |
| `marketConsensus` | object | | Optional market consensus data |
| `assumptions` | object | | Optional forecast assumptions |

**`baseData` object**
| Parameter | Type | Required | Description |
|------|------|------|------|
| `totalAssets` | float | ✅ | Total Assets (millions) |
| `financialAssets` | float | ✅ | Financial Assets (millions) |
| `totalLiabilities` | float | ✅ | Total Liabilities (millions) |
| `financialLiabilities` | float | ✅ | Financial Liabilities (millions) |
| `preferredStock` | float | ✅ | Preferred Stock Value (millions) |
| `minorityEquity` | float | ✅ | Minority Equity (millions) |
| `sales0` | float | ✅ | Base Period Sales (millions), must be > 0 |
| `op0` | float | | Base Period Operating Profit (millions) |
| `oi0` | float | | Base Period Core Profit (millions) |
| `salesGrowthRate` | float | | Base Period Sales Growth Rate |
| `operatingMargin` | float | | Base Period Operating Margin |
| `sharesOutstanding` | float | ✅ | Total Shares Outstanding (millions), must be > 0 |

**`parameters` object**
| Parameter | Type | Required | Description |
|------|------|------|------|
| `forecastYears` | int | | Number of Forecast Years (default: 5) |
| `costOfCapitalRate` | float | ✅ | Discount Rate/WACC, e.g., 0.10 for 10% |
| `terminalGrowthRate` | float | ✅ | Terminal Growth Rate, e.g., 0.03 for 3% |

**`marketConsensus` object (Optional)**
| Parameter | Type | Required | Description |
|------|------|------|------|
| `revenues` | float[] | | Array of annual revenue consensus |
| `eps` | float[] | | Array of annual EPS consensus |

**`assumptions` object (Optional)**
| Parameter | Type | Required | Description |
|------|------|------|------|
| `salesGrowthRates` | float[] | | Array of annual revenue growth rates |
| `operatingMargins` | float[] | | Array of annual operating margins |

## Data Flow

```
Model Input (Financials & Assumptions)
        │
        ▼
   Input Validation
        │
        ├── 1. Derive Base Net Operating Assets (NOA) and Asset Turnover
        │
        ├── 2. Forecast Period Projection (Compute sales, OI, ending NOA, residual income)
        │
        ├── 3. Terminal Value Calculation (Compute terminal value and discount to present)
        │
        └── 4. Value Bridging (Core operating value + Financial Assets - Liabilities - Minority Equity)
        │
        ▼
Markdown Detailed Output (Value per share, Data Tables)
```

## Tech Stack

| Component | Choice | Purpose |
|------|------|------|
| MCP Framework | `mcp` (FastMCP) | MCP server with stdio transport |
| Data Validation | `pydantic` | Strong typing and JSON Schema generation |
| Build Tool | `hatchling` + `uv` | Project configuration and dependency management |
| Testing | `pytest` | Unit testing for the core valuation engine |

## License

MIT
