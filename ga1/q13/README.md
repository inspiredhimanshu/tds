# Fix Corrupted Configuration Export

## Problem

This JSON file was corrupted during application configuration. It contains approximately 10 syntax errors that prevent it from being parsed.

**Common error types:**
- Missing commas between array/object elements
- Extra commas before closing braces/brackets
- Missing quotes around property names
- Single quotes instead of double quotes
- Missing or extra braces/brackets

## Task

1. Download `broken.json`
2. Fix all syntax errors
3. Validate the JSON parses correctly
4. Submit the fixed JSON

## Validation

You can validate JSON using:

**Python:**
```bash
python -m json.tool broken.json
```

**Node.js:**
```bash
node -e "JSON.parse(require('fs').readFileSync('broken.json', 'utf8'))"
```

**Online:**
- https://jsonlint.com/
- VS Code: Install "JSON Tools" extension

## Tips

- Use a text editor with JSON syntax highlighting (VS Code, Sublime)
- Fix errors one at a time, validate frequently
- Look for: missing commas, extra commas, quote issues
- The file is 189KB - be patient!
