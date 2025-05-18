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
    # First try to import from the ai package
    try:
        from .ai import AICapabilities
        AI_AVAILABLE = True
    except (ImportError, ValueError):
        # Then try to import from the ai directory
        try:
            from ai.gz_ai_integration import AICapabilities
            AI_AVAILABLE = True
        except ImportError:
            # Finally try to import directly
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
        self.ai_auto_update = not args.no_auto_update
        self.force_update = args.force_update
        self.show_ai_stats = args.ai_stats
        self.show_ai_evolution = args.ai_evolution
        self.ai_interactive = args.ai_interactive
        self.ai_model_path = args.ai_model
        self.ai_learn_file = args.ai_learn
        self.ai_optimize_file = args.ai_optimize
        self.generate_code = args.generate is not None
        self.generate_description = args.generate
        self.explain_code = args.explain

        # Initialize AI capabilities if available
        self.ai = None
        if AI_AVAILABLE and self.ai_enabled:
            try:
                # Configure AI
                ai_config = {
                    "intelligence_level": self.ai_level,
                    "auto_update": self.ai_auto_update,
                    "model_path": self.ai_model_path
                }

                self.ai = AICapabilities(ai_config)
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
        # Handle force update
        if self.force_update:
            if not self.ai:
                logger.error("AI capabilities required for force update")
                return False

            # Check if self-improvement is available
            if not hasattr(self.ai, 'self_improvement') or not self.ai.self_improvement:
                logger.error("Self-improvement capabilities not available")
                return False

            logger.info("Forcing update to GitHub repository")
            success = self.ai.self_improvement.force_update()

            if success:
                logger.info("Successfully updated GitHub repository")
            else:
                logger.error("Failed to update GitHub repository")

            return success

        # Handle AI stats
        if self.show_ai_stats:
            if not self.ai:
                logger.error("AI capabilities required for AI stats")
                return False

            logger.info("Showing AI statistics")
            stats = self.ai.get_stats()

            # Print stats in a readable format
            print("\nGZ AI Statistics")
            print("===============")
            print(f"Initialization time: {stats.get('initialization_time', 0):.2f} seconds")
            print(f"Code samples processed: {stats.get('code_samples_processed', 0)}")
            print(f"Corrections made: {stats.get('corrections_made', 0)}")
            print(f"Optimizations applied: {stats.get('optimizations_applied', 0)}")

            # Print memory stats
            if 'memory' in stats:
                print("\nMemory Statistics")
                print("----------------")
                for category, category_stats in stats['memory'].items():
                    print(f"{category}: {category_stats.get('item_count', 0)} items")

            # Print self-improvement stats
            if 'self_improvement' in stats:
                print("\nSelf-Improvement Statistics")
                print("--------------------------")
                si_stats = stats['self_improvement']
                print(f"Total improvements: {si_stats.get('total_improvements', 0)}")
                print(f"Successful improvements: {si_stats.get('successful_improvements', 0)}")
                print(f"Last improvement: {si_stats.get('last_improvement', 'Never')}")

            return True

        # Handle AI evolution stats
        if self.show_ai_evolution:
            if not self.ai:
                logger.error("AI capabilities required for AI evolution stats")
                return False

            logger.info("Showing AI evolution statistics")

            # Get evolution stats
            if hasattr(self.ai, 'get_evolution_stats'):
                evolution_stats = self.ai.get_evolution_stats()

                # Print evolution stats in a readable format
                print("\nGZ AI Evolution Statistics")
                print("=========================")
                print(f"Learning iterations: {evolution_stats.get('learning_iterations', 0)}")
                print(f"Current learning rate: {evolution_stats.get('current_learning_rate', 0):.6f}")
                print(f"Learning acceleration: {evolution_stats.get('learning_acceleration', 1.0):.2f}x")

                # Print learning progress
                if 'learning_progress' in evolution_stats:
                    print("\nLearning Progress")
                    print("----------------")
                    progress = evolution_stats['learning_progress']
                    print(f"Syntax understanding: {progress.get('syntax_understanding', 0):.2f}%")
                    print(f"Optimization capability: {progress.get('optimization_capability', 0):.2f}%")
                    print(f"Error correction: {progress.get('error_correction', 0):.2f}%")
                    print(f"Code generation: {progress.get('code_generation', 0):.2f}%")

                # Print evolution history
                if 'evolution_history' in evolution_stats:
                    print("\nEvolution History")
                    print("----------------")
                    history = evolution_stats['evolution_history']
                    for i, entry in enumerate(history[-5:], 1):  # Show last 5 entries
                        print(f"{i}. {entry.get('date', 'Unknown')}: {entry.get('description', 'Unknown')}")

                return True
            else:
                logger.error("Evolution statistics not available")
                return False

        # Handle AI learn
        if self.ai_learn_file:
            if not self.ai:
                logger.error("AI capabilities required for learning")
                return False

            logger.info(f"Learning from file: {self.ai_learn_file}")

            try:
                # Read the file
                with open(self.ai_learn_file, 'r') as f:
                    code = f.read()

                # Process the code
                result = self.ai.process_code(code, {"source_file": self.ai_learn_file})

                # Print results
                print("\nLearning Results")
                print("===============")
                print(f"Learning iterations: {result.get('learning', {}).get('learning_iterations', 0)}")
                print(f"Patterns learned: {result.get('learning', {}).get('patterns_learned', 0)}")

                return True
            except Exception as e:
                logger.error(f"Error learning from file: {str(e)}")
                return False

        # Handle AI optimize
        if self.ai_optimize_file:
            if not self.ai:
                logger.error("AI capabilities required for optimization")
                return False

            logger.info(f"Optimizing file: {self.ai_optimize_file}")

            try:
                # Read the file
                with open(self.ai_optimize_file, 'r') as f:
                    code = f.read()

                # Optimize the code
                result = self.ai.optimize_code(code, self.optimization_level)

                # Print results
                print("\nOptimization Results")
                print("===================")
                print(f"Techniques applied: {len(result.get('techniques_applied', []))}")
                print(f"Code size reduction: {result.get('code_size_reduction', 0)} bytes")

                # Write optimized code to output file
                output_file = self.output_file or f"{self.ai_optimize_file}.opt"
                with open(output_file, 'w') as f:
                    f.write(result.get('optimized_code', code))

                print(f"\nOptimized code written to: {output_file}")

                return True
            except Exception as e:
                logger.error(f"Error optimizing file: {str(e)}")
                return False

        # Regular compilation
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
    parser.add_argument("--no-auto-update", action="store_true", help="Disable GitHub auto-updates")
    parser.add_argument("--force-update", action="store_true", help="Force an update to GitHub with new learnings")
    parser.add_argument("--ai-stats", action="store_true", help="Show AI statistics")
    parser.add_argument("--ai-interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("--ai-model", default="models/gz_ai_model.bin", help="Path to AI model")
    parser.add_argument("--ai-learn", help="Learn from a code file without compiling it")
    parser.add_argument("--ai-optimize", help="Optimize a code file without compiling it")
    parser.add_argument("--ai-evolution", action="store_true", help="Show AI evolution statistics")
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
