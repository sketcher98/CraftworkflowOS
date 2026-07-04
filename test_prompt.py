from runtime.knowledge import load_department
from runtime.reasoning import reason
from runtime.prompt_builder import build_prompt

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

    "Book a discovery call with this lead."

)

print(prompt)