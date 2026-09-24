from pathlib import Path
import webbrowser


html_file = Path(__file__).parent / "big.html"

if html_file.exists():

    print("Opening:", html_file)

    webbrowser.open(
        html_file.resolve().as_uri()
    )

else:

    print("big.html not found.")