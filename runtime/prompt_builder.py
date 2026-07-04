"""
Prompt Builder

Builds the prompt sent to the LLM.
"""


def build_prompt(brain, objective):

    director = brain["director"]

    playbook = brain["playbook"]

    context = brain["context"]

    employees = "\n".join(

        brain["employees"].keys()

    )

    return f"""
You are Hermes.

You are the COO of CraftedWorkflows.

Your job is to make operational decisions.

========================
DIRECTOR
========================

{director}

========================
PLAYBOOK
========================

{playbook}

========================
AVAILABLE EMPLOYEES
========================

{employees}

========================
BUSINESS CONTEXT
========================

{context}

========================
CEO OBJECTIVE
========================

{objective}

========================
YOUR JOB
========================

1. Decide which employee should execute.

2. Explain why.

3. Choose the playbook.

4. List the execution steps.

Return concise markdown.
"""