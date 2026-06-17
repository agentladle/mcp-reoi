from pydantic import BaseModel, Field
from typing import Optional


class BaseData(BaseModel):
    totalAssets: float = Field(..., description="Total Assets (millions)")
    financialAssets: float = Field(..., description="Financial Assets (millions)")
    totalLiabilities: float = Field(..., description="Total Liabilities (millions)")
    financialLiabilities: float = Field(..., description="Financial Liabilities (millions)")
    preferredStock: float = Field(..., description="Preferred Stock Value (millions)")
    minorityEquity: float = Field(..., description="Minority Equity (millions)")
    sales0: float = Field(..., description="Base Period Sales (millions), must be > 0")
    op0: float = Field(default=0, description="Base Period Operating Profit")
    oi0: float = Field(default=0, description="Base Period Core Profit")
    salesGrowthRate: float = Field(default=0, description="Base Period Sales Growth Rate")
    operatingMargin: float = Field(default=0, description="Base Period Operating Margin")
    sharesOutstanding: float = Field(..., description="Total Shares Outstanding (millions), must be > 0")


class Parameters(BaseModel):
    forecastYears: Optional[int] = Field(default=5, description="Number of Forecast Years")
    costOfCapitalRate: float = Field(..., description="Discount Rate/WACC, e.g., 0.10 for 10%")
    terminalGrowthRate: float = Field(..., description="Terminal Growth Rate, e.g., 0.03 for 3%")


class MarketConsensus(BaseModel):
    revenues: list[float] = Field(default_factory=list, description="Array of annual revenue consensus")
    eps: list[float] = Field(default_factory=list, description="Array of annual EPS consensus")


class Assumptions(BaseModel):
    salesGrowthRates: list[float] = Field(default_factory=list, description="Array of annual revenue growth rates")
    operatingMargins: list[float] = Field(default_factory=list, description="Array of annual operating margins")


class ValuationRequest(BaseModel):
    version: str = Field(default="1.0", description="Version")
    ticker: str = Field(default="", description="Stock ticker")
    companyName: str = Field(default="", description="Company Name")
    description: Optional[str] = Field(default=None, description="Template or valuation description")
    currency: str = Field(default="USD", description="Currency")
    unitDescription: Optional[dict] = Field(default=None, description="Unit description dictionary")
    baseData: BaseData
    parameters: Parameters
    marketConsensus: Optional[MarketConsensus] = None
    assumptions: Optional[Assumptions] = None


class YearlyDetail(BaseModel):
    year: int                  # Year
    sales: float                 # Sales
    operatingIncome: float       # Operating Income
    endingNoa: float             # Ending NOA
    capitalCharge: float         # Capital Charge
    residualIncome: float        # Residual Income
    pvOfRi: float                # Present Value of Residual Income


class ValuationResult(BaseModel):
    baseNoa: float               # Base NOA
    assetTurnover: float         # Asset Turnover
    pvRiSum: float               # PV of Forecast Residual Income
    pvTerminalValue: float       # PV of Terminal Value
    totalEquityValue: float      # Total Equity Value
    valuePerShare: float         # Value Per Share
    yearlyDetails: list[YearlyDetail] # Yearly Details
