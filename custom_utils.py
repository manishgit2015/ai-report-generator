from typing import List, Dict, Optional
from custom_types import Section, SectionOutLine, SectionWebSearchResult, ReportGeneratorWorkflowState

class CustomUtils:
    
    @staticmethod
    def merge_sections_by_title( outlines: List[SectionOutLine], 
                                search_results: List[SectionWebSearchResult]) -> List[Dict[str, Optional[str]]]:
        """
        Merges section outlines and web search results by matching title.

        Returns a list of dictionaries with keys: title, description, web_summary.
        """
        # Create a lookup dictionary for web summaries by title
        summary_lookup = {sr.title.strip().lower(): sr.web_summary for sr in search_results}

        merged_dict = []
        for outline in outlines:
            title_key = (outline.title or "").strip().lower()
            merged_dict.append({
                "title": outline.title,
                "description": outline.description,
                "web_summary": summary_lookup.get(title_key, None)
            })
        print(f"****Merged {len(merged_dict)} sections with web summaries.")
        for item in merged_dict:
            print(f"Title: {item['title']}, Description: {item['description']}, Web Summary: {item['web_summary'][:100] if item['web_summary'] else 'No summary'}...")
        
        return merged_dict
    
    
   
    
    
if __name__ == "__main__":
    # Example usage
    outlines = [
        SectionOutLine(title="Introduction", description="Overview of AI in education"),
        SectionOutLine(title="Benefits", description="Advantages of AI in learning")
    ]
    
    search_results = [
        SectionWebSearchResult(title="Introduction", web_summary="AI is transforming education..."),
        SectionWebSearchResult(title="Benefits", web_summary="AI enhances personalized learning...")
    ]
    
    merged_sections = CustomUtils.merge_sections_by_title(outlines, search_results)
    print(merged_sections)