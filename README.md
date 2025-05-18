# GZ Programming Language

GZ is a Filipino-inspired programming language designed to outperform C in speed and efficiency while maintaining a lighter syntax than Python. It features advanced AI capabilities that make it self-evolving, self-improving, and increasingly powerful over time.

## Features

### Core Language Features

- **Filipino-Inspired Keywords**: Uses Filipino keywords like `simula` (function), `balik` (return), `sulat` (print), and `kung` (if)
- **Minimal Syntax**: No parentheses for function calls, no semicolons, indentation-based blocks
- **High Performance**: Designed to outperform C in speed and efficiency
- **Lightweight**: Lighter syntax than Python with minimal overhead

### Advanced AI Capabilities

- **Exponential Learning**: Learns 100x faster with each code sample it processes
- **Persistent Memory**: Never forgets patterns, optimizations, or corrections
- **Self-Improvement**: Autonomously enhances its own codebase and algorithms
- **Feedback Loop**: Continuously refines understanding based on execution results
- **Transfer Learning**: Applies knowledge from one task to different contexts
- **Progressive Optimization**: Optimization levels evolve as knowledge grows
- **GitHub Auto-Updates**: Automatically updates the GitHub repository with new learnings
- **Collective Intelligence**: Learns from all users and shares knowledge with everyone

### UI Design Capabilities

- **Declarative UI**: Define UIs using a declarative syntax
- **Layout System**: Powerful layout system for arranging UI elements
- **Styling**: Apply styles to UI elements
- **Event Handling**: Handle UI events with custom functions

## Installation

### Prerequisites

- Python 3.6 or higher

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Zrald1/gzc.git
   ```

2. Run the installer:
   ```bash
   cd gzc
   ./install.sh
   ```

3. The installer will:
   - Copy the necessary files to `~/.gz/`
   - Create a `gzc` executable in `~/.local/bin/`
   - Add `~/.local/bin` to your PATH (if you choose to)

4. Restart your terminal or run:
   ```bash
   source ~/.bashrc  # or ~/.zshrc if you use zsh
   ```

5. Verify the installation:
   ```bash
   gzc --version
   ```

## Usage

### Basic Usage

Compile and run a GZ program:
```bash
gzc program.gz -r
```

Compile a GZ program to an executable:
```bash
gzc program.gz -o program
```

### AI-Powered Features

Generate code from a description:
```bash
gzc -g "Create a program that calculates the factorial of a number" -o factorial.gz
```

Explain code:
```bash
gzc -e program.gz
```

Optimize code:
```bash
gzc program.gz -O3 -o optimized_program
```

### UI Design

Compile a GZ program with UI components:
```bash
gzc ui_program.gz --ui -r
```

## Language Syntax

### Hello World

```
simula main
    sulat "Hello, World!"
    balik 0
```

### Variables and Data Types

```
simula main
    // Variables
    x = 10
    y = 20
    name = "Juan"
    is_active = tama  // Boolean true

    // Print variables
    sulat "x =", x
    sulat "y =", y
    sulat "name =", name
    sulat "is_active =", is_active

    balik 0
```

### Control Flow

```
simula main
    // If statement
    x = 10

    kung x > 5
        sulat "x is greater than 5"
    kundi
        sulat "x is not greater than 5"

    // For loop
    sulat "Counting from 1 to 5:"
    para i 1 5
        sulat i

    // While loop
    j = 0
    habang j < 5
        sulat "j =", j
        j = j + 1

    balik 0
```

### Functions

```
simula add x y
    balik x + y

simula main
    result = add(10, 20)
    sulat "10 + 20 =", result
    balik 0
```

### UI Design

```
// Define UI elements
ui_element main_window {
    type: window;
    title: "My GZ Application";
    width: 800;
    height: 600;
}

ui_element hello_button {
    type: button;
    text: "Say Hello";
    width: 100;
    height: 30;
}

// Define layout
ui_layout main_layout {
    main_window -> hello_button;
    hello_button @ center;
}

// Define style
ui_style button_style {
    background-color: #3498db;
    text-color: white;
    font-size: 14;
    border-radius: 5;
}

// Define events
ui_event main_events {
    hello_button onClick: function_say_hello;
}

// Main function
simula main
    // Initialize UI
    init_ui()

    // Show main window
    show_window(main_window)

    balik 0

// Event handler
simula function_say_hello
    sulat "Hello, World!"
    show_message(main_window, "Hello", "Hello, World!")
    balik tama
```

## Advanced Features

### AI-Powered Code Generation

The GZ compiler can generate code based on natural language descriptions:

```bash
gzc -g "Create a function to calculate the nth Fibonacci number" -o fibonacci.gz
```

### Auto-Correction

The GZ compiler can automatically correct syntax errors:

```bash
gzc program_with_errors.gz -o fixed_program
```

### Auto-Optimization

The GZ compiler can automatically optimize code for better performance:

```bash
gzc program.gz -O3 -o optimized_program
```

### Self-Improvement and GitHub Auto-Updates

The GZ compiler learns from every interaction and continuously improves itself. It automatically updates the GitHub repository with new learnings, making them available to all users:

```bash
# Force an update to GitHub with new learnings
gzc --force-update

# View learning statistics
gzc --ai-stats

# View AI evolution statistics
gzc --ai-evolution

# Disable auto-updates (not recommended)
gzc --no-auto-update
```

When the GZ compiler learns enough new patterns, optimizations, or corrections, it will automatically update the GitHub repository, ensuring that all users benefit from the collective intelligence of the community.

### Advanced AI Capabilities

The GZ compiler provides advanced AI capabilities for learning and optimization:

```bash
# Learn from a code file without compiling it
gzc --ai-learn examples/advanced_patterns.gz

# Optimize a code file without compiling it
gzc --ai-optimize examples/needs_optimization.gz -o examples/optimized.gz
```

These capabilities allow you to:

1. **Learn from Code**: The AI can learn from your code without compiling it, which helps it improve its understanding of GZ syntax and patterns.

2. **Optimize Code**: The AI can optimize your code without compiling it, applying various optimization techniques to make your code more efficient.

3. **Track Evolution**: The AI can show detailed statistics about its evolution, including learning rate, progress in different areas, and evolution history.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Filipino language and culture
- Built with advanced AI capabilities for continuous improvement
