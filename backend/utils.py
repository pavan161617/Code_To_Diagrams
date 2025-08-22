def sample_mermaid_flowchart(code_snippet: str):
    """
    Simple local parser to create a mermaid flowchart from Python function definitions.
    Not AI-based, just a fallback for testing.
    """
    lines = code_snippet.split("\n")
    mermaid_lines = ["flowchart TD"]
    for i, line in enumerate(lines):
        mermaid_lines.append(f"  A{i}[{line.strip()}]")
        if i > 0:
            mermaid_lines.append(f"  A{i-1} --> A{i}")
    return "\n".join(mermaid_lines)
