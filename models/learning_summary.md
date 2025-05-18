# GZ Collective Learning Summary

Last updated: 2025-05-18 15:45:00

Total learnings: 7
Updates pushed: 3

## Learning Types

- correction_rule: 3
- optimization_rule: 2
- code_template: 2

## Recent Learnings

### correction_rule (2025-05-18)
Frequency: 15, Confidence: 0.98

```
{
  "pattern": ";",
  "replacement": "",
  "explanation": "In GZ, statements don't end with semicolons"
}
```

### correction_rule (2025-05-18)
Frequency: 10, Confidence: 0.95

```
{
  "pattern": "simula\\s+(\\w+)\\s*\\(",
  "replacement": "simula \\1 ",
  "explanation": "In GZ, function declarations don't use parentheses"
}
```

### correction_rule (2025-05-18)
Frequency: 8, Confidence: 0.9

```
{
  "pattern": "sulat\\s*\\(",
  "replacement": "sulat ",
  "explanation": "In GZ, function calls don't use parentheses"
}
```

### optimization_rule (2025-05-18)
Frequency: 5, Confidence: 0.85

```
{
  "pattern": "(\\w+)\\s*=\\s*\\1\\s*\\+\\s*([^;]+)",
  "replacement": "\\1 += \\2",
  "explanation": "Use compound assignment for increment"
}
```

### optimization_rule (2025-05-18)
Frequency: 3, Confidence: 0.8

```
{
  "pattern": "kung\\s+(\\w+)\\s*==\\s*tama",
  "replacement": "kung \\1",
  "explanation": "Simplify boolean comparison"
}
```

### code_template (2025-05-18)
Frequency: 20, Confidence: 0.99

```
{
  "name": "hello_world",
  "code": "simula main\n    sulat \"Hello, World!\"\n    balik 0\n",
  "description": "A simple hello world program"
}
```

### code_template (2025-05-18)
Frequency: 7, Confidence: 0.9

```
{
  "name": "factorial",
  "code": "simula factorial n\n    kung n <= 1\n        balik 1\n    balik n * factorial(n-1)\n\nsimula main\n    para i 1 5\n        sulat i, \"! =\", factorial(i)\n    balik 0\n",
  "description": "A program that calculates factorials"
}
```
