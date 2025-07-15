from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from custom_types import Section
from typing import Dict, List

# Load environment variables (OPENAI_API_KEY)
from dotenv import load_dotenv

load_dotenv()
import asyncio


class SectionWriter:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert report writer. Your task is to write a detailed, informative,
             and well-structured section of a report based on the provided section title,
             description, and web research summary.

             Ensure the content is:
             - Comprehensive and covers the key aspects mentioned in the description.
             - Factually accurate, drawing heavily from the provided web research summary.
             - Well-organized with clear paragraphs and, if appropriate, subheadings or bullet points.
             - Engaging and easy to understand for a general audience.
             - Written in a formal, objective tone.
             - Between 300-500 words.
             
             ## Quality Standards:
             - Comprehensive coverage of the section topic
             - Professional, engaging writing style
             - Accurate representation of research findings
             - Logical organization and clear structure
             - Specific examples and concrete details
             - Smooth transitions between ideas
             
             
             ## Content Structure:
                1. **Introduction**: Brief overview of the section topic and its importance
                2. **Main Content**: Core information organized into logical subsections
                3. **Key Insights**: Important findings, trends, or developments
                4. **Conclusion**: Summary of main points and implications

             
             
             Format the output in Markdown. Do NOT include the section title as a Markdown heading (e.g., # Title).
             Just provide the raw content for the section.
             """,
                ),
                (
                    "human",
                    """
                    ** Section Title:
                    {title}
                    
                    **Section Description: 
                    {description}
                    
                   **Research Summary to Use**:
                     {web_summary}
                     
                   ** Target Audience of the section : 
                     {target_audience}
                     
                   ** Sources (for citation/reference): 
                     {sources}
                     """,
                ),
            ]
        )
        self.parser = StrOutputParser()

    async def write_section(
        self, title: str, description: str, web_summary: str,
        target_audience: str = "general audience",
        sources=None
    ) -> Section:
        """
        Writes the detailed content for a single report section.

        Args:
            title (str): The title of the section.
            description (str): A brief description of what the section should cover.
            web_summary (str): The summarized web research results relevant to this section.

        Returns:
            str: The Section Object.
        """
        print(f"Inside method - write_section() \n ")
        chain = self.prompt | self.llm | self.parser

        print(f"Writing content for section: '{title}'...")
        print(f"\nDescription: {description}")
        print(f"\nWeb Summary: {web_summary[:100]}...")  # Print
        try:
            content = chain.invoke(
                {
                    "title": title,
                    "description": description,
                    "web_summary": web_summary,
                    "sources": "\n".join(f"- [{url}]({url})" for url in (sources or [])),
                    "target_audience": target_audience
                }
            )
            # Optionally, append a References section
            if sources:
                content += "\n\n**References:**\n" + "\n".join(f"- [{url}]({url})" for url in sources)
            
            print(
                f"****Content for section '{title}': {content[:100]}..."
            )  # Print first 100 chars
            return Section(title=title, content=content)

        except Exception as e:
            print(f"Error in SectionWriter for section '{title}': {e}")
            return Section(title=title, content=f"Error: {e}")

    async def write_all_sections(
        self, section_details: List[Dict[str, str]]
        ,target_audience:str
    ) -> List[Section]:
        """
        Writes detailed content for all given report sections.

        Args:
            titles (List[Dict[str, str]]): A list of dictionaries, each with 'title' and 'description'.
            web_summaries (Dict[str, str]): A dictionary where keys are section titles and values are
                                            the summarized web research results for that section.

        Returns:
            Dict[str, str]: A dictionary where keys are section titles and values are
                            the detailed content generated for each section.
        """

        sections = []
        tasks = []
        for section in section_details:
            title = section.get("title", "Not specified")
            description = section.get("description", "Not specified")
            web_summary = section.get("web_summary", "Not specified")
            sources = section.get("sources", None)

            print(f"  Writing content for section: '{title}'...")
            task = asyncio.create_task(
                self.write_section(
                    title=title, description=description, 
                    web_summary=web_summary,target_audience=target_audience,
                    sources=sources
                )
            )
            tasks.append(task)
        sections = await asyncio.gather(*tasks)
        print
        return sections


async def main():
    writer = SectionWriter()
    test_titles = [
        {
            "description": "Introduction to Renewable Energy",
            "description": "An overview of different types of renewable energy sources and their importance.",
            "web_summary": "Renewable energy comes from natural sources like sunlight, wind, rain, tides, and geothermal heat, which are naturally replenished. Key types include solar, wind, hydro, geothermal, and biomass. They are crucial for reducing carbon emissions and combating climate change.",
        },
        {
            "title": "Solar Power Technologies",
            "description": "Detailed explanation of photovoltaic cells and solar thermal systems.",
            "web_summary": "Solar power harnesses sunlight using technologies like photovoltaic (PV) panels, which convert light directly into electricity, and concentrated solar power (CSP) systems, which use mirrors to focus sunlight to heat a fluid and generate steam for turbines. Advancements include improved efficiency, reduced costs, and flexible solar cells.",
        },
    ]

    print("Starting section writing for test sections...")
    sections = await writer.write_all_sections(test_titles)
    print("\n--- Generated Section Contents ---")

    for section in sections:
        print(f"\nSection title: \n {section.title}\n\n")
        print(f"Section content: \n {section.content}\n\n")


# asyncio.run(main())
