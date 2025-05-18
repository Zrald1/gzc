# GZ Collective Learning Summary

Last updated: 2025-05-18 16:11:26

Total learnings: 44
Updates pushed: 0

## Learning Types

- syntax_pattern: 43
- code_sample: 1

## Recent Learnings

### code_sample (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "code": "// Advanced GZ Programming Patterns\n// This file demonstrates advanced programming patterns in GZ\n\n// Advanced function with multiple parameters and return value\nsimula calculate_statistics numbers\n    // Variable declarations\n    count = len(numbers)\n    sum = 0\n    min_val = numbers[0]\n    max_val = numbers[0]\n    \n    // Calculate sum, min, and max\n    para i 0 count - 1\n        current = numbers[i]\n        sum = sum + current\n        \n        kung current < min_val\n            min_val = current\n        \n        kung current > max_val\n            max_val = current\n    \n    // Calculate average\n    average = sum / count\n    \n    // Create and return statistics object\n    stats = {\n        \"count\": count,\n        \"sum\": sum,\n        \"average\": average,\n        \"min\": min_val,\n        \"max\": max_val,\n        \"range\": max_val - min_val\n    }\n    \n    balik stats\n\n// Function to generate Fibonacci sequence\nsimula fibonacci n\n    // Handle edge cases\n    kung n <= 0\n        balik []\n    kung n == 1\n        balik [0]\n    kung n == 2\n        balik [0, 1]\n    \n    // Initialize sequence with first two numbers\n    sequence = [0, 1]\n    \n    // Generate remaining numbers\n    para i 2 n - 1\n        next_number = sequence[i-1] + sequence[i-2]\n        sequence.append(next_number)\n    \n    balik sequence\n\n// Function to check if a number is prime\nsimula is_prime n\n    // Handle edge cases\n    kung n <= 1\n        balik mali\n    kung n <= 3\n        balik tama\n    kung n % 2 == 0 or n % 3 == 0\n        balik mali\n    \n    // Check for divisibility by numbers of form 6k \u00c2\u00b1 1\n    i = 5\n    habang i * i <= n\n        kung n % i == 0 or n % (i + 2) == 0\n            balik mali\n        i = i + 6\n    \n    balik tama\n\n// Function to sort an array using bubble sort\nsimula bubble_sort arr\n    n = len(arr)\n    \n    // Traverse through all array elements\n    para i 0 n - 1\n        // Last i elements are already in place\n        para j 0 n - i - 1\n            // Swap if current element is greater than next element\n            kung arr[j] > arr[j + 1]\n                temp = arr[j]\n                arr[j] = arr[j + 1]\n                arr[j + 1] = temp\n    \n    balik arr\n\n// Main function to demonstrate the advanced patterns\nsimula main\n    // Test calculate_statistics function\n    numbers = [23, 45, 12, 67, 89, 34, 56]\n    sulat \"Statistics for\", numbers\n    stats = calculate_statistics(numbers)\n    sulat \"Count:\", stats[\"count\"]\n    sulat \"Sum:\", stats[\"sum\"]\n    sulat \"Average:\", stats[\"average\"]\n    sulat \"Min:\", stats[\"min\"]\n    sulat \"Max:\", stats[\"max\"]\n    sulat \"Range:\", stats[\"range\"]\n    \n    // Test fibonacci function\n    n = 10\n    sulat \"\\nFibonacci sequence of length\", n\n    fib_sequence = fibonacci(n)\n    sulat fib_sequence\n    \n    // Test is_prime function\n    sulat \"\\nChecking prime numbers:\"\n    para num 10 20\n        kung is_prime(num)\n            sulat num, \"is prime\"\n        kundi\n            sulat num, \"is not prime\"\n    \n    // Test bubble_sort function\n    unsorted = [64, 34, 25, 12, 22, 11, 90]\n    sulat \"\\nUnsorted array:\", unsorted\n    sorted = bubble_sort(unsorted)\n    sulat \"Sorted array:\", sorted\n    \n    balik 0\n",
  "source": "examples/advanced_patterns.gz",
  "timestamp": 1747555885.0159984
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "loops",
  "value": "num",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "loops",
  "value": "j",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 3, Confidence: 0.50

```
{
  "type": "loops",
  "value": "i",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "conditionals",
  "value": "is_prime(num)",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "conditionals",
  "value": "arr[j] > arr[j + 1]",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "conditionals",
  "value": "n % i == 0 or n % (i + 2) == 0",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "conditionals",
  "value": "n % 2 == 0 or n % 3 == 0",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "conditionals",
  "value": "n <= 3",
  "source": "examples/advanced_patterns.gz"
}
```

### syntax_pattern (2025-05-18)
Frequency: 1, Confidence: 0.50

```
{
  "type": "conditionals",
  "value": "n <= 1",
  "source": "examples/advanced_patterns.gz"
}
```

