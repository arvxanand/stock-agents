# NOTE: The generation_options parameter is documented in the tumeryk_guardrails
# PyPI package (v0.3.1), but passing it to tumeryk_completions() on the
# chat-azdev.tmryk.com instance causes the API to echo the user input back
# instead of generating a response. This was tested on 2026-05-11.
#
# These configs are kept as DESIGN DOCUMENTATION — they represent the intended
# per-agent rail settings. If the instance adds support for generation_options
# in the future, uncomment the passing logic in agents.py.
#
# To enforce these settings NOW, configure them per-agent in the Tumeryk
# Trust Studio dashboard instead.

# Agent 1: Stock Collector — lightweight
# Only needs input checking; output is just ticker symbols
COLLECTOR_CONFIG = {
    "rails": {
        "input": True,
        "output": True,
        "dialog": False,
        "retrieval": False
    }
}

# Agent 2: Research Analyst — medium
# Input + output + dialog; reports financial facts that could be hallucinated
ANALYST_CONFIG = {
    "rails": {
        "input": True,
        "output": True,
        "dialog": True,
        "retrieval": False
    }
}

# Agent 3: Decision Maker — full
# All rails on; makes financial recommendations = highest stakes
DECISION_CONFIG = {
    "rails": {
        "input": True,
        "output": True,
        "dialog": True,
        "retrieval": True
    }
}