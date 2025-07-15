from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class SectionOutLine(BaseModel):
    """
    Represents a section outline in the report.
    """
    title: Optional[str] = Field(..., description="The title of the section")
    description: Optional[str] = Field(..., description="The content of the section")
   
    
class SectionWebSearchResult(BaseModel):
    """
    Represents a web search result.
    """
    title: str = Field(..., description="The title of the search result")
    web_summary: str = Field(..., description="A summarized string of the search results")
    sources: Optional[List[str]] = Field(default=None, description="List of citation URLs for the summary")
    
class Section(BaseModel):
    """
    Represents a section in the report.
    """
    title: str = Field(..., description="The title of the section")
    content: str = Field(..., description="The content of the section")
    
    
class ReportGeneratorWorkflowState(BaseModel):
    """
    Represents the state of the report generator workflow.
    """
    
    topic: str = Field(
        default=None,
        description="The high-level topic provided by the user for the report."
    )
    requirements: str = Field(
        default="Standard report requirements",
        description="The high-level Additional requirements or constraints for the report."
    )
    target_audience: Optional[str] = Field(
        default="general audience",
        description="The intended audience for the report (e.g., 'technical experts', 'general audience', 'business executives','Academic tone and style')."
    )
    
    target_word_count: int = Field(
        default=1200,
        description="Target word count for the report."
    )
   
    
    
    sections_outline: Optional[List[SectionOutLine]] = Field(
        default=None,
        description="A list of SectionOutLine, where each section out line contains 'title' and 'description' for a report section."
    )
    
    sectionWebSearchResults: Optional[List[SectionWebSearchResult]] = Field(
        default=None,
        description="A list of SectionWebSearchResult, where each section web search result contains 'title' and 'web_summary' for a report section."
    )
    
    sections: Optional[List[Section]] = Field(
        default=None,
        description="A list of Section, where each section contains 'title' and 'content' for a report section."
    )
    final_report: Optional[str] = Field(
        default=None,
        description="The complete, compiled report in Markdown format."
    )
    final_report_path: Optional[str] = Field(
        default=None,
        description="The complete, compiled report in Markdown format."
    )