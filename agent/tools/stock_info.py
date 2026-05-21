import yfinance as yf
from agent.core.shared_state import MessagesState
from langchain_core.tools import tool
import json
from langchain_core.messages import ToolMessage


@tool(description='Takes the ticker of the company and returns the stock information about the company for example, (Company Name : Apple, Ticker : AAPL)')
def get_stock_information(ticker: str):
    """Takes the official stock ticker of a company (e.g., 'AAPL', 'WFC', 'TSLA') and returns live stock market performance information."""
    ticker = ticker
    stock = yf.Ticker(ticker=ticker)
    stock_info = stock.info
    observation = {
        "name": stock_info.get("longName", "N/A"),
        "aboutCompany": stock_info.get("longBusinessSummary", "N/A"),
        "currency": stock_info.get("currency", "N/A"),
        "currentPrice": stock_info.get("currentPrice", "N/A"),
        "fiftyTwoWeekHigh": stock_info.get("fiftyTwoWeekHigh", "N/A"),
        "fiftyTwoWeekLow": stock_info.get("fiftyTwoWeekLow", "N/A"),
        "marketCap": stock_info.get("marketCap", "N/A"),
        "trailingPE": stock_info.get("trailingPegRatio", "N/A"),
        "recommendationKey": stock_info.get("recommendationKey", "N/A"),
    }

    return {
        "messages" : [ToolMessage(content=json.dumps(observation), tool_call_id="dummy_id")],
        "stock_info": observation
    }
