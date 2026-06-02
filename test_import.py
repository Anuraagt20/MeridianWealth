from pathlib import Path

pdfs = list(
    Path("data").glob("*.pdf")
)

print(pdfs)