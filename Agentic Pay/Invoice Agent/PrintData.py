import json

def pretty_log(title: str, data: dict):
    """
    Prints formatted JSON logs in a clean readable way.
    """
    print("\n" + "=" * 60)
    print(f"🔹 {title}")
    print("-" * 60)
    print(json.dumps(data, indent=4, sort_keys=True))
    print("=" * 60 + "\n")
