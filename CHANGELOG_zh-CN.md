# 更新日志

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本规范](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2026-06-17

### 新增功能
- 首次发布基于 Python 的 `agentladle-mcp-reoi` MCP 服务器。
- 内置 `reoi_valuation_model` 工具（剩余经营性收益估值模型）。
- 支持基于管理用财务报表数据的多阶段剩余收益预测。
- 使用 `FastMCP` 框架，自动从 Pydantic 数据模型转换并生成完全符合 MCP 规范的输入 Schema 描述。
- 支持直接通过 `uvx agentladle-mcp-reoi` 运行服务，实现真正的零配置使用体验。
