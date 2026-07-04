from runtime.workspace import *

create_folder("Sandbox")

create_file(

    "Sandbox/test.md",

    "# Hermes built this."

)

print()

print(read_file(

    "Sandbox/test.md"

))