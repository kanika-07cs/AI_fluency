
import os
import ast
import operator

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from lc_config import store

load_dotenv()

# Adjust this value after measuring your actual embedding distances.
MAX_DISTANCE = 0.6


# ---------------------------------------------------------
# Tool 1: Handbook search with relevance guard
# ---------------------------------------------------------

@tool
def search_handbook(query: str) -> str:
    """Search the college handbook and return relevant chunks only."""

    results = store.similarity_search_with_score(query, k=3)
    relevant_docs = []

    print(f"\nSearch query: {query}")

    for doc, score in results:
        source = doc.metadata.get("source", "unknown")
        print(f"Distance: {score:.4f} | Source: {source}")

        if score <= MAX_DISTANCE:
            relevant_docs.append(doc)

    if not relevant_docs:
        return (
            "NO_MATCH: this is not covered in the college handbook."
        )

    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"{doc.page_content}"
        for doc in relevant_docs
    )


# ---------------------------------------------------------
# Tool 2: Exam eligibility
# ---------------------------------------------------------

@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check whether attendance percentage (0-100) permits a student to write the end-semester exam."""

    if not 0 <= attendance_percent <= 100:
        return "ERROR: Attendance percentage must be between 0 and 100."

    if attendance_percent >= 75:
        return "ELIGIBLE: You may write the end-semester exam."

    if attendance_percent >= 65:
        return (
            "CONDONATION: You may write the end-semester exam after "
            "paying Rs. 500 per course as a condonation fee."
        )

    return (
        "NOT ELIGIBLE: Attendance below 65% does not meet "
        "the exam eligibility requirement."
    )


# ---------------------------------------------------------
# Tool 3: Course fee lookup
# ---------------------------------------------------------

@tool
def get_course_fee(course_code: str) -> str:
    """Return the fee for a supported course code."""

    fees = {
        "CS101": 12000,
        "AI202": 18000,
    }

    code = course_code.strip().upper()

    if code not in fees:
        return f"ERROR: No fee information found for {code}."

    return f"{code} fee: Rs. {fees[code]}"


# ---------------------------------------------------------
# Tool 4: Maximum late fee
# ---------------------------------------------------------

@tool
def get_maximum_late_fee() -> str:
    """Return the maximum late fee from the sample fee policy."""

    return "Maximum late fee: Rs. 2000."


# ---------------------------------------------------------
# Tool 5: Late fee calculation
# ---------------------------------------------------------

@tool
def get_late_fee(days_late: int) -> str:
    """Calculate the late fee for a specified number of days."""

    if days_late < 0:
        return "ERROR: Days late cannot be negative."

    # Example rule consistent with the task's expected totals.
    fee = min(days_late * 100, 2000)

    return f"Late fee for {days_late} days: Rs. {fee}"


# ---------------------------------------------------------
# Tool 6: Safe arithmetic calculator
# ---------------------------------------------------------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _calculate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

    if isinstance(node, ast.BinOp):
        operation = type(node.op)

        if operation not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported arithmetic operation.")

        left = _calculate(node.left)
        right = _calculate(node.right)

        if operation is ast.Div and right == 0:
            raise ValueError("Division by zero.")

        return _ALLOWED_OPERATORS[operation](left, right)

    if isinstance(node, ast.UnaryOp):
        operation = type(node.op)

        if operation not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported arithmetic operation.")

        return _ALLOWED_OPERATORS[operation](
            _calculate(node.operand)
        )

    raise ValueError("Only basic arithmetic expressions are allowed.")


@tool
def calculator(expression: str) -> str:
    """Calculate an arithmetic expression containing numbers and basic operators."""

    try:
        tree = ast.parse(expression, mode="eval")
        result = _calculate(tree.body)
        return f"Result: {result}"
    except (ValueError, SyntaxError, TypeError, ZeroDivisionError) as exc:
        return f"Calculator error: {exc}"


# ---------------------------------------------------------
# Agent configuration
# ---------------------------------------------------------

tools = [
    search_handbook,
    check_exam_eligibility,
    get_course_fee,
    get_maximum_late_fee,
    get_late_fee,
    calculator,
]

SYSTEM_PROMPT = """
You are the college helpdesk assistant.

Instructions:
1. Use search_handbook for placement and college-policy questions.
2. Use check_exam_eligibility for attendance-based exam questions.
3. Use get_course_fee for individual course fee lookups.
4. Use get_maximum_late_fee for the maximum late fee.
5. Use get_late_fee when a specific number of late days is provided.
6. Use calculator for arithmetic; do not calculate totals mentally.
7. Keep track of relevant information from earlier messages in the
   same conversation thread.
8. If search_handbook returns NO_MATCH, say that you do not know
   because the information is not covered by the college handbook.
   Do not guess or invent a college policy.
9. For fee questions, use the tools to retrieve the amounts and
   calculator to calculate the total.
10. Give a concise answer and state the final amount in rupees.
"""

# Example .env value: MODEL=openai:gpt-4o-mini
MODEL = os.getenv("MODEL", "openai:gpt-4o-mini")

model = init_chat_model(MODEL)
checkpointer = MemorySaver()

agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)


# ---------------------------------------------------------
# Direct eligibility-tool tests
# ---------------------------------------------------------

def test_exam_eligibility():
    print("\nEXAM ELIGIBILITY TOOL TESTS")

    for value in [82, 70, 50, 120]:
        output = check_exam_eligibility.invoke(
            {"attendance_percent": value}
        )
        print(f"{value}% -> {output}")


# ---------------------------------------------------------
# Five required questions in one thread
# ---------------------------------------------------------

def run_task_questions():
    questions = [
        "What CGPA do I need to be eligible for placements?",
        "My attendance is 70%. Can I write the exam?",
        (
            "What is the total of the CS101 fee, the AI202 fee "
            "and the maximum late fee?"
        ),
        "And if I pay only 5 days late instead?",
        "What is the capital of France?",
    ]

    config = {
        "configurable": {
            "thread_id": "task-run"
        }
    }

    for number, question in enumerate(questions, start=1):
        print("\n" + "=" * 70)
        print(f"QUESTION {number}: {question}")
        print("=" * 70)

        result = agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            config=config,
        )

        # Print actual tool calls made by the agent.
        for message in result["messages"]:
            tool_calls = getattr(message, "tool_calls", [])

            for call in tool_calls:
                print(f"Tool called: {call['name']}")

        print("\nAgent answer:")
        print(result["messages"][-1].content)


if __name__ == "__main__":
    test_exam_eligibility()
    run_task_questions()
