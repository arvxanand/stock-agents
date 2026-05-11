# Agent 1: Stock Collector
# Lightweight — only checks the input (is the user's query safe?)
# Output rails skipped because the response is just ticker symbols
COLLECTOR_CONFIG = {
    "rails": {
        "input": True,
        "output": False,
        "dialog": False,
        "retrieval": False
    }
}

# Agent 2: Research Analyst
# Medium — checks both input AND output
# Output rails matter here because this agent reports financial facts
# that could be hallucinated or biased
ANALYST_CONFIG = {
    "rails": {
        "input": True,
        "output": True,
        "dialog": False,
        "retrieval": False
    }
}

# Agent 3: Decision Maker
# Full — all rails on, strictest checking
# This agent makes financial recommendations = highest stakes
DECISION_CONFIG = {
    "rails": {
        "input": True,
        "output": True,
        "dialog": True,
        "retrieval": False
    }
}