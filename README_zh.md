# AgentLadle MCP REOI

[English](README.md) | **中文**

> 📈 **金融数据与估值引擎** — 专业的剩余收益 (REOI) 模型量化分析工具。

一个基于 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 的服务器，提供**企业剩余经营性收益估值 (Residual Operating Income Valuation)** 的核心计算引擎工具。

它使 AI 助手（Claude、Cursor 等）能够通过标准化的数据输入接口，执行多阶段的剩余收益预测、折现和企业价值桥接分析。

## 功能特性

- **1 个专业 MCP 工具**提供完善的财务估值能力
- **标准化的剩余收益估值框架**，内置基期分析、预测期折现和永续终值测算逻辑
- **多阶段利润预测**，支持针对每年配置独立的营收增长率与营业利润率
- **智能排版输出**，不仅返回精准的估值数字，还内置 Markdown 表格生成功能，方便在大模型端呈现逐年明细
- **零配置安装** —— 只需一行添加到 MCP 客户端，无需克隆或手动设置
- **纯 Python**，跨平台（Windows / macOS / Linux）

## 前置要求

- **Python 3.10+** — [下载 Python](https://www.python.org/downloads/)
- **uv** — [安装 uv](https://docs.astral.sh/uv/getting-started/installation/)

> **提示：** 安装 uv 后，请重启终端和 MCP 客户端（如 Claude Desktop），确保 `uv` 命令可被识别。

## 快速开始

添加到你的 MCP 客户端配置中（Claude Desktop、Cursor 等）：

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

就这么简单。`uvx` 会自动从 PyPI 下载包及其依赖 —— 无需克隆、无需手动安装、无需配置路径。

### 替代方案：pip 安装

如果你更喜欢自己管理环境：

```bash
pip install agentladle-mcp-reoi
```

然后配置：

```json
{
  "mcpServers": {
    "agentladle-mcp-reoi": {
      "command": "agentladle-mcp-reoi"
    }
  }
}
```

### 替代方案：从源码运行（本地开发）

克隆仓库并直接运行：

```bash
git clone https://github.com/agentladle/mcp-reoi.git
```

然后配置你的 MCP 客户端：

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

将 `/path/to/mcp-reoi` 替换为克隆仓库的实际路径。

## 工具列表

| # | 工具 | 描述 |
|---|------|------|
| 1 | `reoi_valuation_model` | 剩余经营性收益估值模型，基于财务报表和预测假设输出每股价值与估值明细 |

### 工具 1：`reoi_valuation_model`

输入基期财报数据和未来的预测假设，计算得出企业总权益价值及每股建议价值。

**参数列表 (`request` 对象)**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `version` | string | | 版本号，默认 "1.0" |
| `ticker` | string | | 股票代码 |
| `companyName` | string | | 公司名称 |
| `currency` | string | | 货币单位，默认 "CNY" |
| `baseData` | object | ✅ | 基期财务数据 |
| `parameters` | object | ✅ | 估值核心参数 |
| `marketConsensus` | object | | 市场共识预测 (可选) |
| `assumptions` | object | | 预测假设 (可选) |

**`baseData` 对象**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `totalAssets` | float | ✅ | 总资产（百万元） |
| `financialAssets` | float | ✅ | 金融资产（百万元） |
| `totalLiabilities` | float | ✅ | 总负债（百万元） |
| `financialLiabilities` | float | ✅ | 金融负债（百万元） |
| `preferredStock` | float | ✅ | 优先股价值（百万元） |
| `minorityEquity` | float | ✅ | 少数股东权益（百万元） |
| `sales0` | float | ✅ | 基期销售额（百万元），必须大于0 |
| `op0` | float | | 基期营业利润 |
| `oi0` | float | | 基期核心利润 |
| `salesGrowthRate` | float | | 基期营收增长率 |
| `operatingMargin` | float | | 基期营业利润率 |
| `sharesOutstanding` | float | ✅ | 发行在外总股本（百万股），必须大于0 |

**`parameters` 对象**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `forecastYears` | int | | 预测年数，默认 5 |
| `costOfCapitalRate` | float | ✅ | 折现率/WACC，如 0.10 表示 10% |
| `terminalGrowthRate` | float | ✅ | 永续增长率，如 0.03 表示 3% |

**`marketConsensus` 对象 (可选)**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `revenues` | float[] | | 各年营收共识数组 |
| `eps` | float[] | | 各年每股收益共识数组 |

**`assumptions` 对象 (可选)**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `salesGrowthRates` | float[] | | 各年营收增长率数组 |
| `operatingMargins` | float[] | | 各年营业利润率数组 |

## 数据流

```
模型输入 (财务 & 假设数据)
        │
        ▼
   输入数据验证
        │
        ├── 1. 推导基期净经营资产(NOA) 和 资产周转率
        │
        ├── 2. 预测期逐年推演 (计算销售额、营业利润、期末NOA和剩余收益)
        │
        ├── 3. 终值测算 (计算永续期价值并折现)
        │
        └── 4. 价值桥接 (核心经营价值 + 金融资产 - 负债 - 少数权益)
        │
        ▼
Markdown 明细输出 (每股价值、明细表格)
```

## 使用示例

在配置完成后，AI 助手在处理用户需要进行估值的请求时会调用该工具：

**用户**："帮我用剩余收益模型对这家公司进行估值，这里有它2025年的基期数据（总资产16683，金融资产5879...股本543），假设未来5年营收增长率保持在18%，营业利润率14.5%，折现率8%，永续增长3%。"

**AI 助手** 内部将调用：
```python
reoi_valuation_model(
    request={
        "baseData": {
            "totalAssets": 16683.0,
            "financialAssets": 5879.0,
            "totalLiabilities": 6790.0,
            "financialLiabilities": 3235.0,
            "preferredStock": 0.0,
            "minorityEquity": 348.0,
            "sales0": 7130.0,
            "sharesOutstanding": 543.0
        },
        "parameters": {
            "forecastYears": 5,
            "costOfCapitalRate": 0.08,
            "terminalGrowthRate": 0.03
        },
        "assumptions": {
            "salesGrowthRates": [0.18, 0.18, 0.18, 0.18, 0.18],
            "operatingMargins": [0.145, 0.145, 0.145, 0.145, 0.145]
        }
    }
)
```
工具将迅速返回处理好的 Markdown 财务分析表格。

## 技术栈

| 组件 | 选型 | 用途 |
|------|------|------|
| MCP 框架 | `mcp` (FastMCP) | MCP 服务器，stdio 传输 |
| 数据校验 | `pydantic` | 强类型数据验证与 Schema 生成 |
| 打包工具 | `hatchling` + `uv` | 项目配置与依赖管理 |
| 测试框架 | `pytest` | 核心估值引擎单元测试 |

## 项目结构

```
src/mcp_reoi/
├── __init__.py
├── server.py          # MCP 服务器入口
├── models.py          # Pydantic 财务与假设模型
├── tools/
│   ├── __init__.py
│   └── reoi_valuation.py # MCP 工具注册层
└── services/
    ├── __init__.py
    └── engine.py      # 核心 REOI 估值推演逻辑
```

## 许可证

MIT
