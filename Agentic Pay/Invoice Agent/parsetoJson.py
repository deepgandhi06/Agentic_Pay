import json


def print_json_safe(raw_output):
    try:
        data = json.loads(raw_output)
        print("try block")

    except json.JSONDecodeError:
        print("catch block")
        lines = []

        for line in raw_output.splitlines():
            line = line.strip()
            if not line or "summary" in line.lower():
                continue
            lines.append(line.lstrip("-• "))

        data = {
            "summary": lines
        }

    print(json.dumps(data, indent=2))
