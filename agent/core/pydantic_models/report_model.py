from typing import Optional
from pydantic import BaseModel, Field

class FinalReport(BaseModel):
    """The structured output format for the final financial report."""
    
    rag_section: Optional[str] = Field(
        description="Detailed information retrieved from the Wells Fargo 2025 Annual Report. This MUST be a plain markdown string (NOT a JSON object/dict). Leave null if no RAG data was provided."
    )
    web_section: Optional[str] = Field(
        description="Recent news and general information retrieved from the web search. This MUST be a plain markdown string (NOT a JSON object/dict). Leave null if no web data was provided."
    )
    finance_section: Optional[str] = Field(
        description="Live stock price and market data retrieved from Yahoo Finance. This MUST be a plain markdown string (NOT a JSON object/dict). Leave null if no market data was provided."
    )
    combined_summary: str = Field(
        description="A cohesive, final synthesis that answers the user's prompt directly, combining all available data into a single narrative."
    )
