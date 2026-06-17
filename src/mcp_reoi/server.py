import sys
import logging
from mcp.server.fastmcp import FastMCP
from mcp_reoi.tools.reoi_valuation import register_reoi_valuation_tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr
)

# Initialize FastMCP
mcp = FastMCP(
    "ladleagent-mcp-reoi",
    dependencies=["pydantic"]
)

# Register tools
register_reoi_valuation_tool(mcp)

def main():
    """Application entry point"""
    logging.info("Starting ladleagent-mcp-reoi server via stdio")
    mcp.run()

if __name__ == "__main__":
    main()
