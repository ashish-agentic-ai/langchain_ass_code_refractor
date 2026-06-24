"""===========================================================================
Code Refactoring Advisor Agent
This agent analyzes code, detects smells, and suggests refactorings.
Built with LangChain + OpenAI GPT (langchain-openai 1.3.3).
==========================================================================="""
import logging
import sys
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage


logging.basicConfig(
    level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("CodeRefactoringAdvisor")    

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-your"):
    logger.error("Open API Key is not set! Copy Check .env and add your key.")
    sys.exit(1)

logger.info("API key loaded successfully")
logger.info("All LangChain components imported")
logger.info("Initializing the LLM (OpenAI GPT)...")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.6,
    verbose=True
)

logger.info("LLM initialized: model=gpt-4.1-mini, temperature=0.6")
logger.info("Defining agent tools...")

@tool
def detect_code_smells(code:str)-> str:
    """Detects code smells and then suggest cleaner refactored versions of the code."""
    logger.info(f"[Tool: detect_code_smells] Received code for analysis.")
    
    smell_prompt = PromptTemplate(
        input_variables=["code"],
        template="""You are a code refactoring advisor, 
        check the following code for any code smells and suggest cleaner refactored versions of the code.: {code}
        Code: {code}
        Requirements: 
        - Preserve behavior 
        - Improve readability 
        - Improve maintainability 
        - Remove duplication 
        - Improve naming 
        - Reduce nesting 
        - Add error handling where appropriate
    Return a structured response only, nothing else.
    """,) 

    format_prompt = smell_prompt.format(code=code)
    logger.info(f"[Tool: detect_code_smells] Prompt formatted for LLM.")

    response = llm.invoke(format_prompt)

    logger.info(f"[Tool: detect_code_smells] LLM response received.")
    return response.content
@tool
def suggest_refactor(code:str)->str:
    """Suggests refactorings for the provided code. which rewrites the code to be cleaner, more maintainable, and more efficient way."""
    
    logger.info(f"[Tool: suggest_refactor] Received code for refactoring suggestions.")
    

    refactor_prompt = PromptTemplate(
        input_variables=["code"],
        template="""You are a code refactoring advisor, 
        suggest cleaner refactored versions of the following code.: {code}
        Code: {code}
        Requirements: 
        - Preserve behavior 
        - Improve readability 
        - Improve maintainability 
        - Remove duplication 
        - Improve naming 
        - Reduce nesting 
        - Add error handling where appropriate
    Return a structured response only, nothing else.
    """,) 

    format_prompt = refactor_prompt.format(code=code)
    logger.info(f"[Tool: suggest_refactor] Prompt formatted for LLM.")

    response = llm.invoke(format_prompt)

    logger.info(f"[Tool: suggest_refactor] LLM response received.")
    return response.content

tools = [detect_code_smells, suggest_refactor]
logger.info("Agent tools defined successfully.")

logger.info("Creating the agent...")

SYSTEM_PROMPT = """You are a code refactoring advisor agent. Your job is to analyze code, detect code smells, and suggest cleaner refactored versions of the code. You should provide structured responses that include the detected code smells and the suggested refactorings. Ensure that the refactored code preserves the original behavior while improving readability, maintainability, and efficiency.

When user provides code, follow these steps:
1. First, use the detect_code_smells tool to analyze the code and identify any code smells.
2. Then, use the suggest_refactor tool to provide refactoring suggestions for the code. 
3. Return the final structured response to the user, including both the detected code smells and the suggested refactorings.
Use both tools in sequence to provide a comprehensive analysis and refactoring suggestions for the provided code."""

code_corrector = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    debug=True,
)
logger.info("Agent created and ready to run!")

def run_code_corrector(source_code: str)->str:
    """
    Main function to run code refactor advisor.

    Args:
        source_code:Code which you want to scan through Agent for correction and suggestion.
                    
    Returns:
        An updated and corrected code along with suggestions if current code can be implemented without changing current code.
    """
    logger.info("=" * 60)
    logger.info(f"User provided Code: {source_code}")
    logger.info("=" * 60)
    logger.info("Agent is now thinking... watch the tool-calling loop below!")
    logger.info("-" * 60)

    result = code_corrector.invoke(
        {"messages": [HumanMessage(content=source_code)]}
    )

    final_report = result["messages"][-1].content

    # Append a corrected-code-only block to the final report so users get runnable corrected code.
    try:
        corrected_prompt = PromptTemplate(
            input_variables=["code"],
            template=("Provide the fully corrected, refactored version of the following code. "
                      "Return the corrected code, along with a summary of improvements made .\n\nCode:\n{code}\n")
        )

        formatted_corrected = corrected_prompt.format(code=source_code)
        corrected_response = llm.invoke(formatted_corrected)
        corrected_code = corrected_response.content

        final_report = final_report + "\n\nCorrected Code:\n" + corrected_code
    except Exception:
        logger.warning("Could not fetch corrected-code block; continuing with original report.")

    logger.info("-" * 60)
    logger.info("Agent finished! Here's your refactoring report:")
    logger.info("=" * 60)

    return final_report


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CODE REFACTORING ADVISOR AGENT")
    print("  Powered by LangChain + OpenAI")
    print("=" * 60)
    print("\nPaste the source code you want analyzed, or type 'quit' to exit.\n")

    while True:
        user_input = []
        print("Enter/Paste code. End with a single line containing only 'EOF' and hit Enter.")
        while True:
            line = input()
            if line.strip() == "EOF":
                break
            user_input.append(line)

        source = "\n".join(user_input).strip()

        if not source:
            print("Please paste some code (or 'quit' to exit).\n")
            continue

        if source.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!")
            break

        try:
            report = run_code_corrector(source)

            print("\n" + "=" * 60)
            print("CODE REFACTORING REPORT:")
            print("=" * 60)
            print(report)
            print("=" * 60 + "\n")

        except Exception as e:
            logger.error(f"Something went wrong: {e}")
            print(f"\nError: {e}")
            print("Please check your API key and try again.\n")
