"""One external tool: read the student attendance notice."""

from pathlib import Path
from bs4 import BeautifulSoup


NOTICE_FILE = Path(__file__).parent / "notice.html"


def read_attendance_notice() -> str:
    """Read the attendance notice and return only visible text."""

    if not NOTICE_FILE.exists():
        return "Error: attendance notice was not found."

    html = NOTICE_FILE.read_text(
        encoding="utf-8"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove scripts and styles
    for element in soup(["script", "style"]):
        element.decompose()

    # Extract visible text
    text = soup.get_text(
        separator="\n",
        strip=True
    )

    return text


# ONE TOOL
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_attendance_notice",
            "description": (
                "Read the current student attendance notice "
                "and return the attendance information."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


if __name__ == "__main__":

    print("=== ATTENDANCE NOTICE TOOL TEST ===")
    print()

    result = read_attendance_notice()

    print(result)