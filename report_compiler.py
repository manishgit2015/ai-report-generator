import os
from datetime import datetime
from typing import Dict, List
from custom_types import Section, ReportGeneratorWorkflowState


class ReportCompiler:

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def compile_report(
        self,
        topic: str,
        sections: List[Section],
    ) -> str:
        """
        Compiles all report sections into a single Markdown-formatted report.

        Args:
            topic (str): The original high-level topic.
            sections List[Section]: A list of Section, each with 'title' and 'content'.

        Returns:
            str: The complete Markdown-formatted report content.
        """
        report_lines = [
            f"# Report on: {topic}\n",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "---\n",
        ]
        i = 1
        for section in sections:
            
            title_slug = (
                section.title.lower()
                .replace(" ", "-")
                .replace(":", "")
                .replace(",", "")
                .replace(".", "")
            )
            report_lines.append(f"{i}. [{section.title}](#{title_slug})\n")
            i = i + 1
            
            
        report_lines.append("\n---\n")
        # Add each section with its title and content
        for section in sections:
            title = section.title
            content = getattr(
                section, "content", f"Content not found for section: {title}"
            )

            report_lines.append(f"\n## {title}\n")
            report_lines.append(content)
            report_lines.append("\n---\n")  # Separator between sections

        final_report_content = "\n".join(report_lines)
        print("Report compilation complete.")
        return final_report_content

    def save_report(self, report_content: str, topic: str) -> str:
        """
        Saves the compiled report to a Markdown file with a timestamped filename.

        Args:
            report_content (str): The complete Markdown-formatted report content.
            topic (str): The original topic, used to generate a filename.

        Returns:
            str: The full path to the saved report file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize topic for filename: replace spaces with underscores, remove special chars
        sanitized_topic = "".join(c if c.isalnum() else "_" for c in topic)
        filename = f"{sanitized_topic}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report_content)
            print(f"Report successfully saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving report to {filepath}: {e}")
            return None



if __name__ == "__main__":
    compiler = ReportCompiler(output_dir="../reports_test") # Use a test directory
    test_topic = "The Future of Quantum Computing"
    test_sections = [
        {"title": "Introduction to Quantum Computing", 
         "content": "This section introduces the fascinating field of quantum computing..."},
        
        {"title": "Quantum Algorithms", 
         "content": "Quantum algorithms like Shor's and Grover's promise to revolutionize..."},
        
        {"title": "Challenges and Future Outlook", 
         "content": "Despite its immense potential, quantum computing faces significant challenges..."
        }
    ]
    
    section_objects: List[Section] = [Section(**section) for section in test_sections]

    print("Compiling test report...")
    compiled_report = compiler.compile_report(test_topic, section_objects)
    if compiled_report:
        print("\n--- Compiled Report Content (first 500 chars) ---")
        print(compiled_report[:500])
        print("\n--- End of preview ---")
        # Ensure the test directory exists before saving
        os.makedirs("../reports_test", exist_ok=True)
        saved_path = compiler.save_report(compiled_report, test_topic)
        if saved_path:
            print(f"Test report saved to: {saved_path}")
