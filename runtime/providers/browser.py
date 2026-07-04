from runtime.artifacts import Artifact


def execute(objective):

    print("      Browser searching...")

    artifact = Artifact(
        type="LeadList",
        title="Potential Leads",
        content="""
Agency Alpha|Marketing Agency|London|12 Employees
Agency Bravo|Creative Agency|Manchester|7 Employees
Agency Charlie|Automation Agency|Birmingham|4 Employees
Agency Delta|Web Design Agency|London|22 Employees
Agency Echo|SEO Agency|Leeds|9 Employees
""",
        created_by="Browser"
    )

    return artifact