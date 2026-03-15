import json
raw_text = """```json
{
  "ikigai_profile_summary": {
    "what_you_love": "Test"
  },
  "match_reasoning": {}
}
```"""
if raw_text.startswith("```"):
    raw_text = raw_text.split("```")[1]
    if raw_text.startswith("json"):
        raw_text = raw_text[4:]
    raw_text = raw_text.rsplit("```", 1)[0].strip()

print(repr(raw_text))
try:
    data = json.loads(raw_text)
    print("Parsed successfully:", type(data))
except Exception as e:
    print("Error:", repr(e))
