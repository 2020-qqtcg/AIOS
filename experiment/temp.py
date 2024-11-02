import re

string = """
<FINAL ANSWER>
```python
    if not numbers:  # Handle empty input
        return []

    result = []
    current_max = numbers[0]

    for number in numbers:
        current_max = max(current_max, number)
        result.append(current_max)

    return result
```
</FINAL ANSWER>
"""

if __name__ == '__main__':
    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, string, re.DOTALL)

    result = "\n".join(matches)
    print(result)
