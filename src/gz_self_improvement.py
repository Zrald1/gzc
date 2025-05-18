#!/usr/bin/env python3
"""
Self-Improvement Mechanism for GZ Programming Language
This module implements a system that allows the AI to autonomously enhance
its own codebase and algorithms.
"""

import os
import sys
import json
import time
import importlib
import inspect
import ast
import astor
import hashlib
from datetime import datetime
import logging
import threading
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("models/self_improvement.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("GZ-Self-Improvement")

class CodeAnalyzer:
    """Analyzes code to identify improvement opportunities"""
    
    def __init__(self):
        self.metrics = {}
        self.improvement_opportunities = []
    
    def analyze_module(self, module_path):
        """Analyze a Python module for improvement opportunities"""
        try:
            with open(module_path, 'r') as f:
                code = f.read()
            
            # Parse the code into an AST
            tree = ast.parse(code)
            
            # Collect metrics
            self.metrics = {
                "loc": len(code.split('\n')),
                "functions": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
                "classes": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                "complexity": self._calculate_complexity(tree)
            }
            
            # Identify improvement opportunities
            self.improvement_opportunities = []
            
            # Check for long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_code = astor.to_source(node)
                    func_lines = func_code.count('\n') + 1
                    
                    if func_lines > 30:
                        self.improvement_opportunities.append({
                            "type": "long_function",
                            "name": node.name,
                            "location": f"Line {node.lineno}",
                            "description": f"Function '{node.name}' is {func_lines} lines long. Consider refactoring.",
                            "priority": "medium"
                        })
            
            # Check for complex conditionals
            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    test_code = astor.to_source(node.test)
                    if test_code.count('and') + test_code.count('or') > 2:
                        self.improvement_opportunities.append({
                            "type": "complex_conditional",
                            "location": f"Line {node.lineno}",
                            "description": f"Complex conditional: {test_code}. Consider simplifying.",
                            "priority": "medium"
                        })
            
            # Check for duplicate code (simplified)
            function_bodies = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    body_code = astor.to_source(ast.Module(body=node.body))
                    body_hash = hashlib.md5(body_code.encode()).hexdigest()
                    
                    if body_hash in function_bodies:
                        self.improvement_opportunities.append({
                            "type": "duplicate_code",
                            "name": node.name,
                            "location": f"Line {node.lineno}",
                            "description": f"Function '{node.name}' has similar code to '{function_bodies[body_hash]}'.",
                            "priority": "high"
                        })
                    else:
                        function_bodies[body_hash] = node.name
            
            return self.metrics, self.improvement_opportunities
        
        except Exception as e:
            logger.error(f"Error analyzing module {module_path}: {str(e)}")
            return {}, []
    
    def _calculate_complexity(self, tree):
        """Calculate cyclomatic complexity of the code"""
        complexity = 0
        
        # Count branches that increase complexity
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
                complexity += len(node.values) - 1
        
        return complexity

class CodeImprover:
    """Implements code improvements based on analysis"""
    
    def __init__(self, backup_dir="models/backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def backup_file(self, file_path):
        """Create a backup of a file before modifying it"""
        try:
            with open(file_path, 'r') as f:
                original_code = f.read()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            backup_path = os.path.join(self.backup_dir, f"{filename}.{timestamp}.bak")
            
            with open(backup_path, 'w') as f:
                f.write(original_code)
            
            logger.info(f"Created backup of {file_path} at {backup_path}")
            return backup_path
        
        except Exception as e:
            logger.error(f"Error creating backup of {file_path}: {str(e)}")
            return None
    
    def apply_improvements(self, file_path, improvements):
        """Apply improvements to a file"""
        if not improvements:
            logger.info(f"No improvements to apply to {file_path}")
            return False
        
        # Create a backup first
        backup_path = self.backup_file(file_path)
        if not backup_path:
            return False
        
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Parse the code into an AST
            tree = ast.parse(code)
            
            # Apply improvements
            modified = False
            
            for improvement in improvements:
                if improvement["type"] == "long_function":
                    # This would require complex refactoring, not implemented here
                    pass
                
                elif improvement["type"] == "complex_conditional":
                    # Simplify complex conditionals
                    for node in ast.walk(tree):
                        if isinstance(node, ast.If) and node.lineno == int(improvement["location"].split()[1]):
                            # This would require complex transformation, not implemented here
                            pass
                
                elif improvement["type"] == "duplicate_code":
                    # Extract duplicate code to a common function
                    # This would require complex refactoring, not implemented here
                    pass
            
            if modified:
                # Convert the modified AST back to code
                modified_code = astor.to_source(tree)
                
                with open(file_path, 'w') as f:
                    f.write(modified_code)
                
                logger.info(f"Applied improvements to {file_path}")
                return True
            
            logger.info(f"No improvements were applied to {file_path}")
            return False
        
        except Exception as e:
            logger.error(f"Error applying improvements to {file_path}: {str(e)}")
            
            # Restore from backup if something went wrong
            try:
                with open(backup_path, 'r') as f:
                    original_code = f.read()
                
                with open(file_path, 'w') as f:
                    f.write(original_code)
                
                logger.info(f"Restored {file_path} from backup after error")
            except Exception as restore_error:
                logger.error(f"Error restoring from backup: {str(restore_error)}")
            
            return False

class AlgorithmOptimizer:
    """Optimizes algorithms based on performance metrics"""
    
    def __init__(self):
        self.performance_history = {}
    
    def measure_performance(self, func, *args, **kwargs):
        """Measure the performance of a function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Record performance
        func_name = func.__name__
        if func_name not in self.performance_history:
            self.performance_history[func_name] = []
        
        self.performance_history[func_name].append({
            "execution_time": execution_time,
            "args_hash": hashlib.md5(str(args).encode()).hexdigest(),
            "timestamp": datetime.now().isoformat()
        })
        
        return result, execution_time
    
    def suggest_optimizations(self, func):
        """Suggest optimizations for a function based on its code"""
        func_name = func.__name__
        func_code = inspect.getsource(func)
        
        suggestions = []
        
        # Check if function is in performance history
        if func_name in self.performance_history and len(self.performance_history[func_name]) > 5:
            # Calculate average execution time
            avg_time = np.mean([p["execution_time"] for p in self.performance_history[func_name]])
            
            if avg_time > 0.1:  # If function takes more than 100ms on average
                suggestions.append({
                    "type": "performance",
                    "description": f"Function '{func_name}' takes {avg_time:.4f}s on average. Consider optimization.",
                    "priority": "high"
                })
        
        # Analyze function code for optimization opportunities
        if "for" in func_code and "append" in func_code:
            suggestions.append({
                "type": "list_comprehension",
                "description": f"Consider using list comprehension instead of for loop with append in '{func_name}'.",
                "priority": "medium"
            })
        
        if func_code.count("if") > 3:
            suggestions.append({
                "type": "conditional_complexity",
                "description": f"Function '{func_name}' has many conditional statements. Consider refactoring.",
                "priority": "medium"
            })
        
        return suggestions

class SelfImprovementEngine:
    """Main engine for self-improvement"""
    
    def __init__(self, source_dir="src", improvement_interval=3600):
        self.source_dir = source_dir
        self.improvement_interval = improvement_interval  # Run self-improvement every hour
        self.analyzer = CodeAnalyzer()
        self.improver = CodeImprover()
        self.optimizer = AlgorithmOptimizer()
        self.running = False
        self.improvement_thread = None
        self.improvement_history = []
        self.last_improvement_time = 0
        
        # Load improvement history if available
        self._load_history()
    
    def _load_history(self):
        """Load improvement history from file"""
        history_path = "models/improvement_history.json"
        try:
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    self.improvement_history = json.load(f)
                    if self.improvement_history:
                        self.last_improvement_time = datetime.fromisoformat(
                            self.improvement_history[-1]["timestamp"]
                        ).timestamp()
        except Exception as e:
            logger.error(f"Error loading improvement history: {str(e)}")
    
    def _save_history(self):
        """Save improvement history to file"""
        history_path = "models/improvement_history.json"
        try:
            with open(history_path, 'w') as f:
                json.dump(self.improvement_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving improvement history: {str(e)}")
    
    def start(self):
        """Start the self-improvement engine"""
        if self.running:
            logger.warning("Self-improvement engine is already running")
            return
        
        self.running = True
        self.improvement_thread = threading.Thread(target=self._improvement_loop)
        self.improvement_thread.daemon = True
        self.improvement_thread.start()
        
        logger.info("Self-improvement engine started")
    
    def stop(self):
        """Stop the self-improvement engine"""
        self.running = False
        if self.improvement_thread:
            self.improvement_thread.join(timeout=5)
        
        logger.info("Self-improvement engine stopped")
    
    def _improvement_loop(self):
        """Main loop for periodic self-improvement"""
        while self.running:
            # Check if it's time to run self-improvement
            current_time = time.time()
            if current_time - self.last_improvement_time >= self.improvement_interval:
                logger.info("Running self-improvement cycle")
                
                # Analyze and improve all Python files in source directory
                for root, _, files in os.walk(self.source_dir):
                    for file in files:
                        if file.endswith(".py"):
                            file_path = os.path.join(root, file)
                            self._improve_file(file_path)
                
                self.last_improvement_time = current_time
                self._save_history()
                
                logger.info("Self-improvement cycle completed")
            
            # Sleep for a while
            time.sleep(60)  # Check every minute
    
    def _improve_file(self, file_path):
        """Analyze and improve a single file"""
        logger.info(f"Analyzing {file_path}")
        
        # Analyze the file
        metrics, opportunities = self.analyzer.analyze_module(file_path)
        
        if opportunities:
            logger.info(f"Found {len(opportunities)} improvement opportunities in {file_path}")
            
            # Apply improvements
            success = self.improver.apply_improvements(file_path, opportunities)
            
            # Record the improvement attempt
            improvement_record = {
                "timestamp": datetime.now().isoformat(),
                "file": file_path,
                "opportunities": len(opportunities),
                "success": success,
                "metrics_before": metrics
            }
            
            if success:
                # Re-analyze to get updated metrics
                updated_metrics, _ = self.analyzer.analyze_module(file_path)
                improvement_record["metrics_after"] = updated_metrics
            
            self.improvement_history.append(improvement_record)
        else:
            logger.info(f"No improvement opportunities found in {file_path}")
    
    def force_improvement_cycle(self):
        """Force an immediate improvement cycle"""
        logger.info("Forcing immediate self-improvement cycle")
        
        # Analyze and improve all Python files in source directory
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self._improve_file(file_path)
        
        self.last_improvement_time = time.time()
        self._save_history()
        
        logger.info("Forced self-improvement cycle completed")
        
        return len(self.improvement_history)
    
    def get_improvement_stats(self):
        """Get statistics about self-improvement"""
        if not self.improvement_history:
            return {
                "total_improvements": 0,
                "successful_improvements": 0,
                "last_improvement": None,
                "most_improved_file": None
            }
        
        successful = sum(1 for imp in self.improvement_history if imp.get("success", False))
        
        # Count improvements by file
        file_counts = {}
        for imp in self.improvement_history:
            file = imp["file"]
            if file not in file_counts:
                file_counts[file] = 0
            if imp.get("success", False):
                file_counts[file] += 1
        
        most_improved = max(file_counts.items(), key=lambda x: x[1]) if file_counts else (None, 0)
        
        return {
            "total_improvements": len(self.improvement_history),
            "successful_improvements": successful,
            "last_improvement": self.improvement_history[-1]["timestamp"] if self.improvement_history else None,
            "most_improved_file": most_improved[0],
            "most_improved_count": most_improved[1]
        }

# Example usage
if __name__ == "__main__":
    engine = SelfImprovementEngine()
    
    # Force an immediate improvement cycle
    engine.force_improvement_cycle()
    
    # Get improvement stats
    print(engine.get_improvement_stats())
    
    # Start the engine for continuous improvement
    # engine.start()
    
    # ... (application runs) ...
    
    # Stop the engine when done
    # engine.stop()
