#!/usr/bin/env python3
"""
GZ Programming Language Compiler
This is the main executable for the GZ compiler with integrated AI capabilities.
"""

import os
import sys
import argparse
import subprocess
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gzc.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("GZC")

# Try to import AI modules
try:
    from gz_ai_integration import AICapabilities
    AI_AVAILABLE = True
except ImportError:
    logger.warning("AI capabilities not available. Running in basic mode.")
    AI_AVAILABLE = False

# Try to import UI modules
try:
    from gz_ui_compiler import UICompiler
    UI_AVAILABLE = True
except ImportError:
    logger.warning("UI capabilities not available. UI compilation disabled.")
    UI_AVAILABLE = False

class GZCompiler:
    """Main GZ compiler class"""
    
    def __init__(self, args):
        self.args = args
        self.source_file = args.source_file
        self.output_file = args.output_file
        self.optimization_level = args.optimization_level
        self.target = args.target
        self.verbose = args.verbose
        self.run = args.run
        self.ui_mode = args.ui
        
        # AI-related options
        self.ai_enabled = not args.no_ai
        self.ai_level = args.ai_level
        self.ai_auto_correct = not args.no_auto_correct
        self.ai_auto_optimize = not args.no_auto_optimize
        self.ai_interactive = args.ai_interactive
        self.ai_model_path = args.ai_model
        self.generate_code = args.generate is not None
        self.generate_description = args.generate
        self.explain_code = args.explain
        
        # Initialize AI capabilities if available
        self.ai = None
        if AI_AVAILABLE and self.ai_enabled:
            try:
                self.ai = AICapabilities()
                self.ai.initialize()
                logger.info(f"AI capabilities initialized with intelligence level {self.ai_level}")
            except Exception as e:
                logger.error(f"Failed to initialize AI capabilities: {str(e)}")
                self.ai_enabled = False
        
        # Initialize UI compiler if available and needed
        self.ui_compiler = None
        if UI_AVAILABLE and self.ui_mode:
            try:
                self.ui_compiler = UICompiler()
                logger.info("UI compiler initialized")
            except Exception as e:
                logger.error(f"Failed to initialize UI compiler: {str(e)}")
                self.ui_mode = False
    
    def compile(self):
        """Compile the source file"""
        if not self.source_file and not self.generate_code:
            logger.error("No source file specified and no code generation requested")
            return False
        
        # Handle code generation
        if self.generate_code:
            if not self.ai:
                logger.error("AI capabilities required for code generation")
                return False
            
            logger.info(f"Generating code from description: {self.generate_description}")
            result = self.ai.generate_code(self.generate_description)
            
            if "error" in result:
                logger.error(f"Code generation failed: {result['error']}")
                return False
            
            generated_code = result.get("code", "")
            
            # Save generated code to file
            if not self.output_file or self.output_file == "a.out":
                self.output_file = "generated.gz"
            
            with open(self.output_file, 'w') as f:
                f.write(generated_code)
            
            logger.info(f"Generated code written to {self.output_file}")
            
            # If run is requested, set the source file to the generated code
            if self.run:
                self.source_file = self.output_file
            else:
                return True
        
        # Check if source file exists
        if not os.path.exists(self.source_file):
            logger.error(f"Source file not found: {self.source_file}")
            return False
        
        # Read source file
        try:
            with open(self.source_file, 'r') as f:
                source_code = f.read()
        except Exception as e:
            logger.error(f"Failed to read source file: {str(e)}")
            return False
        
        # Handle code explanation
        if self.explain_code:
            if not self.ai:
                logger.error("AI capabilities required for code explanation")
                return False
            
            logger.info(f"Explaining code in {self.source_file}")
            result = self.ai.explain_code(source_code)
            
            if "error" in result:
                logger.error(f"Code explanation failed: {result['error']}")
                return False
            
            explanation = result.get("explanation", "")
            print(explanation)
            return True
        
        # Process UI code if in UI mode
        if self.ui_mode:
            if not self.ui_compiler:
                logger.error("UI compiler required for UI mode")
                return False
            
            logger.info(f"Compiling UI code in {self.source_file}")
            ui_result = self.ui_compiler.compile(source_code)
            
            if not ui_result.get("success", False):
                logger.error(f"UI compilation failed: {ui_result.get('error', 'Unknown error')}")
                return False
            
            # Update source code with processed UI code
            source_code = ui_result.get("processed_code", source_code)
        
        # Apply AI auto-correction if enabled
        if self.ai and self.ai_auto_correct:
            logger.info("Applying AI auto-correction")
            correction_result = self.ai.correct_code(source_code)
            
            if "error" in correction_result:
                logger.error(f"Auto-correction failed: {correction_result['error']}")
            elif correction_result.get("corrections_made", False):
                source_code = correction_result.get("corrected_code", source_code)
                logger.info("Auto-correction applied successfully")
        
        # Compile the code
        if self.verbose:
            logger.info(f"Compiling {self.source_file} to {self.output_file}")
            logger.info(f"Optimization level: {self.optimization_level}")
            logger.info(f"Target: {self.target}")
        
        # Apply AI auto-optimization if enabled
        if self.ai and self.ai_auto_optimize:
            logger.info("Applying AI auto-optimization")
            optimization_result = self.ai.optimize_code(source_code, self.optimization_level)
            
            if "error" in optimization_result:
                logger.error(f"Auto-optimization failed: {optimization_result['error']}")
            else:
                source_code = optimization_result.get("optimized_code", source_code)
                logger.info(f"Auto-optimization applied successfully with {len(optimization_result.get('techniques_applied', []))} techniques")
        
        # For now, we'll use our Python interpreter to run the code
        # In a real implementation, this would compile to native code
        
        # Save processed code to a temporary file
        temp_file = f"{self.output_file}.gz"
        with open(temp_file, 'w') as f:
            f.write(source_code)
        
        if self.verbose:
            logger.info(f"Processed code saved to {temp_file}")
        
        # If run is requested, execute the code
        if self.run:
            logger.info(f"Running {self.output_file}")
            
            # For now, we'll use our Python interpreter
            interpreter_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gz_interpreter.py")
            
            if not os.path.exists(interpreter_path):
                # Fall back to the one in the current directory
                interpreter_path = "gz_interpreter.py"
            
            try:
                result = subprocess.run(["python", interpreter_path, temp_file], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(result.stdout)
                    logger.info("Program executed successfully")
                else:
                    print(result.stderr)
                    logger.error(f"Program execution failed with code {result.returncode}")
                    return False
            except Exception as e:
                logger.error(f"Failed to run program: {str(e)}")
                return False
        
        # Learn from the code if AI is enabled
        if self.ai:
            logger.info("Learning from code")
            self.ai.process_code(source_code, {"source_file": self.source_file})
        
        return True
    
    def cleanup(self):
        """Clean up resources"""
        if self.ai:
            self.ai.shutdown()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="GZ Programming Language Compiler")
    
    # Basic options
    parser.add_argument("source_file", nargs="?", help="Source file to compile")
    parser.add_argument("-o", "--output", dest="output_file", default="a.out", help="Output file")
    parser.add_argument("-O", "--optimize", dest="optimization_level", type=int, choices=range(0, 4), default=0, help="Optimization level (0-3)")
    parser.add_argument("-t", "--target", choices=["native", "x86", "x64", "arm", "arm64", "riscv"], default="native", help="Target architecture")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-r", "--run", action="store_true", help="Run the program after compilation")
    
    # AI-related options
    parser.add_argument("--no-ai", action="store_true", help="Disable AI assistant")
    parser.add_argument("--ai-level", type=int, choices=range(1, 11), default=5, help="AI intelligence level (1-10)")
    parser.add_argument("--no-auto-correct", action="store_true", help="Disable auto-correction")
    parser.add_argument("--no-auto-optimize", action="store_true", help="Disable auto-optimization")
    parser.add_argument("--ai-interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("--ai-model", default="models/gz_ai_model.bin", help="Path to AI model")
    parser.add_argument("-g", "--generate", help="Generate code from description")
    parser.add_argument("-e", "--explain", action="store_true", help="Explain the code")
    
    # UI-related options
    parser.add_argument("--ui", action="store_true", help="Enable UI compilation mode")
    
    args = parser.parse_args()
    
    # Create and run the compiler
    compiler = GZCompiler(args)
    success = compiler.compile()
    compiler.cleanup()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
