from mcp_reoi.models import ValuationRequest, ValuationResult, YearlyDetail

def calculate_reoi(req: ValuationRequest) -> ValuationResult:
    """
    Residual Operating Income Valuation Core Engine (Strict Replica)
    Replicates ladleagent frontend useValuationStore logic
    """
    bd = req.baseData
    params = req.parameters
    
    mc = req.marketConsensus
    ass = req.assumptions
    
    # ---------- 1. Inference and Preprocessing ----------
    forecast_years = params.forecastYears if params.forecastYears and params.forecastYears > 0 else 5
    
    growth_rates = list(ass.salesGrowthRates) if ass and ass.salesGrowthRates else []
    margins = list(ass.operatingMargins) if ass and ass.operatingMargins else []
    
    has_market_consensus = mc is not None and isinstance(mc.revenues, list) and isinstance(mc.eps, list)
    
    if len(growth_rates) == 0 and len(margins) == 0:
        if has_market_consensus and len(mc.revenues) > 0:
            forecast_years = min(len(mc.revenues), len(mc.eps))
        
        growth_rates = [0.0] * forecast_years
        margins = [0.0] * forecast_years
    else:
        forecast_years = max(len(growth_rates), len(margins))
        while len(growth_rates) < forecast_years:
            growth_rates.append(0.0)
        while len(margins) < forecast_years:
            margins.append(0.0)

    # Market consensus derivation
    if has_market_consensus:
        revenues = mc.revenues
        eps = mc.eps
        shares = bd.sharesOutstanding
        
        for i in range(forecast_years):
            if i < len(revenues) and i < len(eps):
                current_revenue = revenues[i]
                current_eps = eps[i]
                
                # Derive sales growth rate
                if current_revenue is not None:
                    previous_revenue = bd.sales0 if i == 0 else revenues[i - 1]
                    if previous_revenue is not None and previous_revenue > 0:
                        growth_rates[i] = (current_revenue / previous_revenue) - 1.0

                # Derive operating margin (implied net margin = (EPS * shares) / revenue)
                if current_eps is not None and current_revenue is not None and current_revenue > 0 and shares > 0:
                    net_income = current_eps * shares
                    implied_margin = net_income / current_revenue
                    margins[i] = implied_margin

    # ---------- 2. Validations ----------
    errors = []

    if bd.sharesOutstanding <= 0:
        errors.append("Shares outstanding must be greater than 0.")

    base_noa = (bd.totalAssets - bd.financialAssets) - (bd.totalLiabilities - bd.financialLiabilities)
    if base_noa <= 0:
        errors.append("Net Operating Assets (NOA) must be greater than 0. Check balance sheet data.")

    if bd.sales0 <= 0:
        errors.append("Base period sales must be greater than 0.")

    if params.costOfCapitalRate <= params.terminalGrowthRate:
        errors.append("Cost of capital (WACC) must be greater than terminal growth rate.")

    if errors:
        raise ValueError(" ".join(errors))

    # ---------- 3. Core Engine ----------
    # Step 1: Base metrics
    asset_turnover = bd.sales0 / base_noa

    yearly_details: list[YearlyDetail] = []

    # Step 2: Forecast projection
    current_sales = bd.sales0
    beginning_noa = base_noa
    pv_ri_sum = 0.0

    for year in range(1, forecast_years + 1):
        year_index = year - 1

        growth_rate = growth_rates[year_index] if year_index < len(growth_rates) else 0.10
        margin = margins[year_index] if year_index < len(margins) else 0.15

        sales = current_sales * (1 + growth_rate)
        operating_income = sales * margin
        ending_noa = sales / asset_turnover
        capital_charge = beginning_noa * params.costOfCapitalRate
        residual_income = operating_income - capital_charge
        pv_of_ri = residual_income / ((1 + params.costOfCapitalRate) ** year)

        pv_ri_sum += pv_of_ri

        yearly_details.append(YearlyDetail(
            year=year,
            sales=sales,
            operatingIncome=operating_income,
            endingNoa=ending_noa,
            capitalCharge=capital_charge,
            residualIncome=residual_income,
            pvOfRi=pv_of_ri
        ))

        current_sales = sales
        beginning_noa = ending_noa

    # Step 3: Terminal value
    if len(yearly_details) == 0:
        raise ValueError("Failed to calculate forecast period data.")

    last_year_detail = yearly_details[forecast_years - 1]
    last_year_ri = last_year_detail.residualIncome
    terminal_ri = last_year_ri * (1 + params.terminalGrowthRate)
    terminal_value = terminal_ri / (params.costOfCapitalRate - params.terminalGrowthRate)
    pv_terminal_value = terminal_value / ((1 + params.costOfCapitalRate) ** forecast_years)

    # Step 4: Value bridging
    core_operating_value = base_noa + pv_ri_sum + pv_terminal_value

    total_equity_value = core_operating_value + bd.financialAssets - bd.financialLiabilities - bd.preferredStock - bd.minorityEquity
    value_per_share = total_equity_value / bd.sharesOutstanding

    return ValuationResult(
        baseNoa=base_noa,
        assetTurnover=asset_turnover,
        pvRiSum=pv_ri_sum,
        pvTerminalValue=pv_terminal_value,
        totalEquityValue=total_equity_value,
        valuePerShare=value_per_share,
        yearlyDetails=yearly_details
    )


def format_valuation_result(result: ValuationResult) -> str:
    text = "Valuation Successful (Model: Residual Operating Income Valuation REOI - Strict Replica)\n"
    text += "──────────────────────────────\n"
    text += "【Conclusion】\n"
    text += f"· Suggested Value Per Share: {result.valuePerShare:.2f}\n"
    text += f"· Total Equity Value: {result.totalEquityValue:.2f} (millions)\n\n"

    text += "【Value Breakdown】\n"
    text += f"· Base Net Operating Assets (NOA): {result.baseNoa:.2f} (millions)\n"
    text += f"· PV of Forecast Residual Income: {result.pvRiSum:.2f} (millions)\n"
    text += f"· PV of Terminal Value: {result.pvTerminalValue:.2f} (millions)\n\n"

    text += "【Core Metrics】\n"
    text += f"· Asset Turnover: {result.assetTurnover:.4f}\n\n"

    text += "【Yearly Forecast Details】\n"
    
    text += "| Year | Sales | Operating Income | Ending NOA | Capital Charge | Residual Income | Present Value |\n"
    text += "|---|---|---|---|---|---|---|\n"
    
    for detail in result.yearlyDetails:
        text += f"| {detail.year} | {detail.sales:.2f} | {detail.operatingIncome:.2f} | {detail.endingNoa:.2f} | {detail.capitalCharge:.2f} | {detail.residualIncome:.2f} | {detail.pvOfRi:.2f} |\n"

    return text
