from runtime.knowledge import load_department
from runtime.reasoning import reason
from runtime.prompt_builder import build_prompt
from runtime.llm import think

department = load_department("Commercial")

lead = {

    "company": "Agency Alpha",

    "industry": "Marketing Agency",

    "employees": 12,

    "city": "London",

    "score": 90

}

brain = reason(
    department,
    lead
)

prompt = build_prompt(

    brain,

    "Book a discovery call."

)

decision = think(prompt)

print()

print("=" * 60)
print("HERMES DECISION")
print("=" * 60)

print()

print(decision)