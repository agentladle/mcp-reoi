from mcp.server.fastmcp import FastMCP
from mcp_reoi.models import ValuationRequest
from mcp_reoi.services.engine import calculate_reoi, format_valuation_result

def register_reoi_valuation_tool(mcp: FastMCP):
    @mcp.tool(
        name="reoi_valuation_model",
        description="Residual Operating Income Valuation Model (Strict Replica based on Ladleagent frontend). Accepts a full JSON state object for valuation calculation."
    )
    def reoi_valuation_model(request: ValuationRequest) -> str:
        try:
            result = calculate_reoi(request)
            return format_valuation_result(result)
        except Exception as e:
            return f"Valuation calculation failed: {str(e)}"
