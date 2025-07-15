from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI
from custom_types import SectionWebSearchResult,SectionOutLine, Section
from typing import List, Optional, Dict
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv(),override=True)
import asyncio



class WebResearcher:

    def __init__(self):
        # Initialize the Google Serper tool
        self.tool = GoogleSerperAPIWrapper()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

        # Prompt for summarizing web search results
        self.summarize_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert at summarizing web search results concisely and accurately.
             Given a search query and a set of search results, extract the most relevant information
             to answer the query. Focus on factual accuracy and synthesize information from multiple
             sources if necessary. 
             ## Quality and Response Standards:
                - Comprehensive coverage of the search topic
                - Focus on the most current and relevant information
                - Clear, professional writing style
                - Accurate representation of source material
                - Include specific facts, statistics, and examples where available
                - Note and remove any conflicting information or uncertainties
                - Logical organization and flow
                - Focus on actionable insights and concrete information
             If the results are not relevant, state that clearly. 
             Remember: Your summaries will be used by other agents to write detailed report sections, so provide rich, 
             detailed information that can support comprehensive writing.
             """,
                ),
                ("human", "Search Query: {query}\n\nSearch Results:\n{results}"),
            ]
        )

    async def _perform_search_and_summarize(self, title: str, query: str) -> SectionWebSearchResult:
        """
        Performs a web search and summarizes the results.

        Args:
            query (str): The search query.

        Returns:
            str: A summarized string of the search results.
        """
        try:
            # Perform the search using the tool
            search_results = self.tool.run(query)
            # Extract URLs (assuming search_results is a dict with 'results' as a list of dicts)
            urls = []
            if isinstance(search_results, dict) and "results" in search_results:
                urls = [item.get("link") for item in search_results["results"] if "link" in item]

            # Create a summarization chain
            summarization_chain = (
                {"query": RunnablePassthrough(), "results": RunnablePassthrough()}
                | self.summarize_prompt
                | self.llm
                | StrOutputParser()
            )
            # Invoke the summarization chain with the original query and search results
            web_summary = summarization_chain.invoke(
                {"query": query, "results": search_results}
            )
            
            sectionWebSearchResult = SectionWebSearchResult(
                title=title,
                web_summary=web_summary,
                sources=urls)
            # print(
            #     f"  Summary for '{sectionWebSearchResult.title}': {sectionWebSearchResult.web_summary[:100]}..."
            # )  # Print first 100 chars of web_summary
            
            return sectionWebSearchResult
        except Exception as e:
            print(f"Error during web search or summarization for query '{query}': {e}")
            return f"Could not retrieve information for '{query}'. Error: {e}"

    async def research_sections(
        self, section_titles: List[SectionOutLine]
    ) -> List[SectionWebSearchResult]:
        """
        Researches and summarizes information for each given report section.

        Args:
            section_titles (List[Dict[str, str]]): A list of dictionaries, each with 'title' and 'description'.

        Returns:
            Dict[str, str]: A dictionary where keys are section titles and values are
                            the summarized web research results for that section.
        """
        
        tasks = []
        for section in section_titles:
            title = section.title
            description = section.description
            search_query = (
                f"{title}: {description}"  # Use both for a comprehensive query
            )
            print(f"  Researching for section: '{title}' with query: '{search_query}'")
            task = asyncio.create_task(
                self._perform_search_and_summarize(title=title, query=search_query)
            )
            tasks.append(task)

        web_summaries = await asyncio.gather(*tasks)
        print(f"*****Web research completed for {len(web_summaries)} sections.")
        # for sectionWebSearchResult in web_summaries:
        #     print(f"\nSection: {sectionWebSearchResult.title}")
        #     print(f"Summary: {sectionWebSearchResult.web_summary}\n")
        return web_summaries


async def main():
    researcher = WebResearcher()
    test_sections = [
        {
            "title": "The Rise of AI in Healthcare",
            "description": "Impact of artificial intelligence on medical diagnostics and patient care.",
        },
        {
            "title": "Ethical Considerations of AI",
            "description": "Discussing bias, privacy, and accountability in AI development and deployment.",
        },
    ]
    print("Starting web research for test sections...")
    sectionWebSearchResults = await researcher.research_sections(test_sections)
    print("\n--- Web Research Summaries ---")
    for sectionWebSearchResult in sectionWebSearchResults:
        print(f"\nSection: {sectionWebSearchResult.title}")
        print(f"Summary: {sectionWebSearchResult.web_summary}\n")


# asyncio.run(main())
