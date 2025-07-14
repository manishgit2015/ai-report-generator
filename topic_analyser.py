from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from custom_types import SectionOutLine, ReportGeneratorWorkflowState
from typing import List, Optional, Dict



class TopicAnalyzer:
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert report planner and topic analyzer.
             Your task is to take a high-level user topic and break it down into 3 to 5 detailed,
             well-structured report section titles, each with a brief, clear description of what
             that section will cover. Ensure the sections are logical, comprehensive, and cover
             different aspects of the main topic.
             Provide the output as a JSON array of objects, where each object has 'title' and 'description' keys.

             Example Output:
             [
                {{
                    "title": "Introduction to Quantum Computing",
                    "description": "An overview of quantum computing, its basic principles, and historical context."
                }},
                {{
                    "title": "Key Quantum Algorithms",
                    "description": "Detailed explanation of essential quantum algorithms like Shor's and Grover's."
                }}
             ]
             """),
            ("human", "User topic: {topic}")
        ])
        self.parser = JsonOutputParser(pydantic_object=List[SectionOutLine])
        
        
    def analyze_topic(self, topic: str) -> List[SectionOutLine]:
        """_summary_

         Args:
             topic (str): The high-level topic provided by the user.

         Returns:
             List[SectionBuilder]: A list of SectionBuilder, where each SectionOutLine contains
                                  'title' and 'description' for a report section.
        """
        try:
            chain = self.prompt | self.llm | self.parser
            response = chain.invoke({"topic": topic})
            return response
        except Exception as e:
            print(f"Error during topic analysis: {e}")
            return []



if __name__ == "__main__":
    analyzer = TopicAnalyzer()
    test_topic = "The Impact of AI on the Future of Work"
    print(f"Analyzing topic: '{test_topic}'")
    sections = analyzer.analyze_topic(test_topic)
    if sections:
        print("\nGenerated Report Sections:")
        for i, section in enumerate(sections):
            print(f"  {i+1}. Title: {section['title']}")
            print(f"     Description: {section['description']}\n")
    else:
        print("Failed to generate sections.")