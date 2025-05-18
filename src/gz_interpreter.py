#!/usr/bin/env python3
"""
GZ Programming Language Interpreter
This is a simple interpreter for the GZ programming language.
"""

import os
import sys
import re
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gz_interpreter.log"),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger("GZ-Interpreter")

# Try to import AI modules
try:
    from gz_ai_integration import AICapabilities
    AI_AVAILABLE = True
except ImportError:
    logger.warning("AI capabilities not available. Running in basic mode.")
    AI_AVAILABLE = False

class GZInterpreter:
    """GZ language interpreter"""
    
    def __init__(self, ai_enabled=True):
        self.variables = {}
        self.functions = {}
        self.current_indent = 0
        self.line_num = 0
        
        # Initialize AI capabilities if available
        self.ai = None
        if AI_AVAILABLE and ai_enabled:
            try:
                self.ai = AICapabilities()
                self.ai.initialize()
                logger.info("AI capabilities initialized")
            except Exception as e:
                logger.error(f"Failed to initialize AI capabilities: {str(e)}")
    
    def tokenize(self, code):
        """Convert code string into tokens with indentation tracking"""
        # Remove comments
        code = re.sub(r'//.*', '', code)
        
        # Split into lines and track indentation
        lines = []
        for line_num, line in enumerate(code.split('\n'), 1):
            # Skip empty lines
            if not line.strip():
                continue
            
            # Calculate indentation level
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            
            if content:  # Skip empty lines
                lines.append((line_num, indent, content))
        
        return lines
    
    def parse_and_execute(self, tokens):
        """Parse and execute the tokenized code"""
        i = 0
        while i < len(tokens):
            line_num, indent, content = tokens[i]
            self.line_num = line_num
            
            # Function definition
            if content.startswith('simula '):
                func_def = content[7:].strip()
                func_name = func_def.split()[0]
                func_params = func_def.split()[1:] if len(func_def.split()) > 1 else []
                
                # Collect function body
                body = []
                i += 1
                while i < len(tokens) and tokens[i][1] > indent:
                    body.append(tokens[i])
                    i += 1
                
                # Store function
                self.functions[func_name] = {
                    'params': func_params,
                    'body': body
                }
                
                # If this is the main function, execute it
                if func_name == 'main' and not self.variables.get('_executed_main'):
                    self.variables['_executed_main'] = True
                    self.call_function('main', [])
                
                continue
            
            i += 1
    
    def call_function(self, name, args):
        """Call a function by name with arguments"""
        if name not in self.functions:
            self.error(f"Function '{name}' not defined")
            return None
        
        func = self.functions[name]
        
        # Create new scope for function variables
        old_vars = self.variables.copy()
        
        # Bind parameters to arguments
        for i, param in enumerate(func['params']):
            if i < len(args):
                self.variables[param] = args[i]
        
        # Execute function body
        result = self.execute_block(func['body'])
        
        # Restore previous scope
        self.variables = old_vars
        
        return result
    
    def execute_block(self, block):
        """Execute a block of code"""
        result = None
        i = 0
        while i < len(block):
            line_num, indent, content = block[i]
            self.line_num = line_num
            
            # Handle return statement
            if content.startswith('balik '):
                expr = content[6:].strip()
                if expr:
                    result = self.evaluate_expression(expr)
                return result
            
            # Handle print statement
            elif content.startswith('sulat '):
                args = self.parse_print_args(content[6:])
                print(*args)
            
            # Handle if statement
            elif content.startswith('kung '):
                condition = content[5:].strip()
                if self.evaluate_expression(condition):
                    # Collect if body
                    if_body = []
                    i += 1
                    while i < len(block) and block[i][1] > indent:
                        if_body.append(block[i])
                        i += 1
                    
                    # Execute if body
                    result = self.execute_block(if_body)
                    if result is not None:  # Return from function
                        return result
                else:
                    # Skip if body
                    i += 1
                    while i < len(block) and block[i][1] > indent:
                        i += 1
                
                continue
            
            # Handle for loop
            elif content.startswith('para '):
                parts = content[5:].strip().split()
                if len(parts) >= 3:
                    var_name = parts[0]
                    
                    # Handle range syntax (0..10)
                    if '..' in parts[1]:
                        start, end = parts[1].split('..')
                        start = int(start)
                        end = int(end)
                        range_values = range(start, end + 1)
                    else:
                        # Handle explicit range (0 10)
                        start = int(parts[1])
                        end = int(parts[2])
                        range_values = range(start, end + 1)
                    
                    # Collect loop body
                    loop_body = []
                    i += 1
                    while i < len(block) and block[i][1] > indent:
                        loop_body.append(block[i])
                        i += 1
                    
                    # Execute loop
                    for val in range_values:
                        self.variables[var_name] = val
                        result = self.execute_block(loop_body)
                        if result is not None:  # Return from function
                            return result
                    
                    continue
            
            # Handle variable assignment
            elif ' = ' in content:
                var_name, expr = content.split(' = ', 1)
                self.variables[var_name.strip()] = self.evaluate_expression(expr)
            
            # Handle function call as statement
            elif '(' in content and ')' in content:
                self.evaluate_expression(content)
            
            i += 1
        
        return result
    
    def parse_print_args(self, args_str):
        """Parse arguments for print statement"""
        args = []
        
        # Handle string literals
        in_string = False
        current_arg = ''
        i = 0
        
        while i < len(args_str):
            char = args_str[i]
            
            if char == '"' and (i == 0 or args_str[i-1] != '\\'):
                in_string = not in_string
                if not in_string:  # End of string
                    args.append(current_arg)
                    current_arg = ''
                i += 1
                continue
            
            if in_string:
                current_arg += char
            elif char.strip():  # Non-whitespace outside string
                if char == ',':
                    if current_arg:
                        args.append(self.evaluate_expression(current_arg.strip()))
                        current_arg = ''
                else:
                    current_arg += char
            
            i += 1
        
        # Add the last argument if any
        if current_arg.strip():
            args.append(self.evaluate_expression(current_arg.strip()))
        
        return args
    
    def evaluate_expression(self, expr):
        """Evaluate an expression"""
        # Handle string literals
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        
        # Handle numeric literals
        if expr.isdigit():
            return int(expr)
        
        # Handle boolean literals
        if expr == 'tama':
            return True
        if expr == 'mali':
            return False
        
        # Handle null
        if expr == 'wala':
            return None
        
        # Handle variable reference
        if expr in self.variables:
            return self.variables[expr]
        
        # Handle function calls
        match = re.match(r'(\w+)\((.*)\)', expr)
        if match:
            func_name = match.group(1)
            args_str = match.group(2)
            
            # Parse arguments
            args = []
            if args_str.strip():
                # Simple argument parsing (doesn't handle nested calls properly)
                for arg in args_str.split(','):
                    args.append(self.evaluate_expression(arg.strip()))
            
            # Call function
            if func_name in self.functions:
                return self.call_function(func_name, args)
            else:
                self.error(f"Function '{func_name}' not defined")
                return None
        
        # Handle basic arithmetic
        if '+' in expr:
            left, right = expr.split('+', 1)
            return self.evaluate_expression(left.strip()) + self.evaluate_expression(right.strip())
        
        if '-' in expr and not expr.startswith('-'):
            left, right = expr.split('-', 1)
            return self.evaluate_expression(left.strip()) - self.evaluate_expression(right.strip())
        
        if '*' in expr:
            left, right = expr.split('*', 1)
            return self.evaluate_expression(left.strip()) * self.evaluate_expression(right.strip())
        
        if '/' in expr:
            left, right = expr.split('/', 1)
            return self.evaluate_expression(left.strip()) / self.evaluate_expression(right.strip())
        
        # Handle comparisons
        if '<=' in expr:
            left, right = expr.split('<=', 1)
            return self.evaluate_expression(left.strip()) <= self.evaluate_expression(right.strip())
        
        if '>=' in expr:
            left, right = expr.split('>=', 1)
            return self.evaluate_expression(left.strip()) >= self.evaluate_expression(right.strip())
        
        if '==' in expr:
            left, right = expr.split('==', 1)
            return self.evaluate_expression(left.strip()) == self.evaluate_expression(right.strip())
        
        if '!=' in expr:
            left, right = expr.split('!=', 1)
            return self.evaluate_expression(left.strip()) != self.evaluate_expression(right.strip())
        
        if '<' in expr:
            left, right = expr.split('<', 1)
            return self.evaluate_expression(left.strip()) < self.evaluate_expression(right.strip())
        
        if '>' in expr:
            left, right = expr.split('>', 1)
            return self.evaluate_expression(left.strip()) > self.evaluate_expression(right.strip())
        
        self.error(f"Cannot evaluate expression: {expr}")
        return None
    
    def error(self, message):
        """Report an error"""
        print(f"Error at line {self.line_num}: {message}", file=sys.stderr)
    
    def cleanup(self):
        """Clean up resources"""
        if self.ai:
            self.ai.shutdown()

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: gz_interpreter.py <source_file>", file=sys.stderr)
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    if not os.path.exists(source_file):
        print(f"Error: File '{source_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(source_file, 'r') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize interpreter
    interpreter = GZInterpreter()
    
    # Tokenize and execute
    tokens = interpreter.tokenize(code)
    interpreter.parse_and_execute(tokens)
    
    # Clean up
    interpreter.cleanup()

if __name__ == "__main__":
    main()
