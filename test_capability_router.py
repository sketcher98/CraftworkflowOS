from runtime.capability_router import request

print(request(
    "writing",
    "Write a LinkedIn post."
))

print()

print(request(
    "research",
    "Find agency owners."
))

print()

print(request(
    "design",
    "Create hero image."
))