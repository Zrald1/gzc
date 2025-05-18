#!/usr/bin/env python3
"""
Feedback Loop System for GZ Programming Language
This module implements a system that continuously refines the AI's understanding
based on code execution results.
"""

import os
import json
import time
import logging
import hashlib
import numpy as np
from datetime import datetime
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("models/feedback_loop.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("GZ-Feedback-Loop")

class ExecutionTracker:
    """Tracks code execution results"""
    
    def __init__(self, history_file="models/execution_history.json"):
        self.history_file = history_file
        self.executions = []
        self.current_execution = None
        
        # Load history if available
        self._load_history()
    
    def _load_history(self):
        """Load execution history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.executions = json.load(f)
        except Exception as e:
            logger.error(f"Error loading execution history: {str(e)}")
            self.executions = []
    
    def _save_history(self):
        """Save execution history to file"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.executions, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving execution history: {str(e)}")
    
    def start_execution(self, code, source_file=None, context=None):
        """Start tracking a new code execution"""
        code_hash = hashlib.md5(code.encode()).hexdigest()
        
        self.current_execution = {
            "id": f"exec_{int(time.time())}_{code_hash[:8]}",
            "timestamp_start": datetime.now().isoformat(),
            "code_hash": code_hash,
            "source_file": source_file,
            "context": context or {},
            "status": "running",
            "output": [],
            "errors": [],
            "execution_time": 0,
            "memory_usage": 0,
            "success": None
        }
        
        return self.current_execution["id"]
    
    def add_output(self, output):
        """Add output from the execution"""
        if self.current_execution:
            self.current_execution["output"].append(output)
    
    def add_error(self, error):
        """Add error from the execution"""
        if self.current_execution:
            self.current_execution["errors"].append(error)
    
    def end_execution(self, success, execution_time, memory_usage=0):
        """End the current execution tracking"""
        if self.current_execution:
            self.current_execution["timestamp_end"] = datetime.now().isoformat()
            self.current_execution["status"] = "completed"
            self.current_execution["success"] = success
            self.current_execution["execution_time"] = execution_time
            self.current_execution["memory_usage"] = memory_usage
            
            self.executions.append(self.current_execution)
            self._save_history()
            
            result = self.current_execution
            self.current_execution = None
            return result
        
        return None
    
    def get_execution(self, execution_id):
        """Get a specific execution by ID"""
        for execution in self.executions:
            if execution["id"] == execution_id:
                return execution
        return None
    
    def get_executions_by_hash(self, code_hash):
        """Get all executions for a specific code hash"""
        return [e for e in self.executions if e["code_hash"] == code_hash]
    
    def get_recent_executions(self, limit=10):
        """Get the most recent executions"""
        return sorted(self.executions, key=lambda e: e["timestamp_start"], reverse=True)[:limit]
    
    def get_execution_stats(self):
        """Get statistics about executions"""
        if not self.executions:
            return {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "avg_execution_time": 0
            }
        
        successful = sum(1 for e in self.executions if e.get("success", False))
        failed = sum(1 for e in self.executions if e.get("success") is False)
        
        execution_times = [e.get("execution_time", 0) for e in self.executions if e.get("execution_time", 0) > 0]
        avg_time = np.mean(execution_times) if execution_times else 0
        
        return {
            "total": len(self.executions),
            "successful": successful,
            "failed": failed,
            "avg_execution_time": avg_time
        }

class PatternExtractor:
    """Extracts patterns from code and execution results"""
    
    def __init__(self):
        self.patterns = defaultdict(list)
    
    def extract_patterns(self, code, execution_result):
        """Extract patterns from code and its execution result"""
        patterns = {}
        
        # Skip if execution result is None
        if not execution_result:
            return patterns
        
        # Extract success/failure patterns
        success = execution_result.get("success", False)
        
        # Basic code metrics
        lines = code.split('\n')
        code_length = len(lines)
        non_empty_lines = sum(1 for line in lines if line.strip())
        
        patterns["code_metrics"] = {
            "length": code_length,
            "non_empty_lines": non_empty_lines,
            "success": success
        }
        
        # Extract syntax patterns
        syntax_patterns = []
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                continue
            
            # Function definitions
            if line.startswith('simula '):
                syntax_patterns.append(("function_definition", line))
            
            # Variable assignments
            elif ' = ' in line and not line.startswith('kung '):
                syntax_patterns.append(("variable_assignment", line))
            
            # Print statements
            elif line.startswith('sulat '):
                syntax_patterns.append(("print_statement", line))
            
            # Conditional statements
            elif line.startswith('kung '):
                syntax_patterns.append(("conditional", line))
            
            # Loop statements
            elif line.startswith('para ') or line.startswith('habang '):
                syntax_patterns.append(("loop", line))
            
            # Return statements
            elif line.startswith('balik '):
                syntax_patterns.append(("return_statement", line))
        
        patterns["syntax_patterns"] = syntax_patterns
        
        # Extract error patterns if execution failed
        if not success and execution_result.get("errors"):
            error_patterns = []
            for error in execution_result["errors"]:
                # Extract line number if available
                line_num = None
                if "line" in error.lower():
                    try:
                        # Try to extract line number from error message
                        parts = error.split("line")
                        if len(parts) > 1:
                            num_part = parts[1].split()[0].strip(":")
                            line_num = int(num_part)
                    except (ValueError, IndexError):
                        pass
                
                # Get the line of code if we have a line number
                error_line = lines[line_num - 1].strip() if line_num and 0 < line_num <= len(lines) else None
                
                error_patterns.append({
                    "error_message": error,
                    "line_number": line_num,
                    "code_line": error_line
                })
            
            patterns["error_patterns"] = error_patterns
        
        # Extract performance patterns
        execution_time = execution_result.get("execution_time", 0)
        memory_usage = execution_result.get("memory_usage", 0)
        
        patterns["performance"] = {
            "execution_time": execution_time,
            "memory_usage": memory_usage
        }
        
        return patterns

class FeedbackAnalyzer:
    """Analyzes feedback from code executions"""
    
    def __init__(self, knowledge_file="models/feedback_knowledge.json"):
        self.knowledge_file = knowledge_file
        self.knowledge = {
            "syntax_success": defaultdict(lambda: {"success": 0, "failure": 0}),
            "error_patterns": defaultdict(lambda: {"count": 0, "examples": []}),
            "performance_metrics": {
                "execution_times": [],
                "memory_usage": []
            }
        }
        
        # Load knowledge if available
        self._load_knowledge()
    
    def _load_knowledge(self):
        """Load knowledge from file"""
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r') as f:
                    loaded_knowledge = json.load(f)
                
                # Convert defaultdicts
                self.knowledge["syntax_success"] = defaultdict(lambda: {"success": 0, "failure": 0})
                for key, value in loaded_knowledge.get("syntax_success", {}).items():
                    self.knowledge["syntax_success"][key] = value
                
                self.knowledge["error_patterns"] = defaultdict(lambda: {"count": 0, "examples": []})
                for key, value in loaded_knowledge.get("error_patterns", {}).items():
                    self.knowledge["error_patterns"][key] = value
                
                self.knowledge["performance_metrics"] = loaded_knowledge.get("performance_metrics", {
                    "execution_times": [],
                    "memory_usage": []
                })
        except Exception as e:
            logger.error(f"Error loading feedback knowledge: {str(e)}")
    
    def _save_knowledge(self):
        """Save knowledge to file"""
        try:
            os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
            
            # Convert defaultdicts to regular dicts for JSON serialization
            serializable_knowledge = {
                "syntax_success": dict(self.knowledge["syntax_success"]),
                "error_patterns": dict(self.knowledge["error_patterns"]),
                "performance_metrics": self.knowledge["performance_metrics"]
            }
            
            with open(self.knowledge_file, 'w') as f:
                json.dump(serializable_knowledge, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving feedback knowledge: {str(e)}")
    
    def analyze_patterns(self, patterns):
        """Analyze patterns from code execution"""
        if not patterns:
            return
        
        # Update syntax success/failure counts
        success = patterns.get("code_metrics", {}).get("success", False)
        
        for pattern_type, pattern_value in patterns.get("syntax_patterns", []):
            pattern_key = f"{pattern_type}:{hashlib.md5(pattern_value.encode()).hexdigest()[:8]}"
            
            if success:
                self.knowledge["syntax_success"][pattern_key]["success"] += 1
            else:
                self.knowledge["syntax_success"][pattern_key]["failure"] += 1
        
        # Update error patterns
        for error_pattern in patterns.get("error_patterns", []):
            error_msg = error_pattern.get("error_message", "")
            if not error_msg:
                continue
            
            # Create a simplified key from the error message
            # Remove specific details like line numbers, variable names, etc.
            simplified_msg = error_msg.lower()
            for word in ["line", "variable", "function", "module", "file"]:
                if word in simplified_msg:
                    parts = simplified_msg.split(word)
                    if len(parts) > 1:
                        # Replace specific details with placeholders
                        simplified_msg = parts[0] + word + " X" + "".join(parts[1].split()[1:])
            
            error_key = hashlib.md5(simplified_msg.encode()).hexdigest()[:16]
            
            self.knowledge["error_patterns"][error_key]["count"] += 1
            
            # Store example if we don't have too many already
            if len(self.knowledge["error_patterns"][error_key]["examples"]) < 5:
                self.knowledge["error_patterns"][error_key]["examples"].append({
                    "message": error_msg,
                    "code_line": error_pattern.get("code_line")
                })
        
        # Update performance metrics
        execution_time = patterns.get("performance", {}).get("execution_time", 0)
        memory_usage = patterns.get("performance", {}).get("memory_usage", 0)
        
        if execution_time > 0:
            self.knowledge["performance_metrics"]["execution_times"].append(execution_time)
            # Keep only the last 1000 entries
            self.knowledge["performance_metrics"]["execution_times"] = self.knowledge["performance_metrics"]["execution_times"][-1000:]
        
        if memory_usage > 0:
            self.knowledge["performance_metrics"]["memory_usage"].append(memory_usage)
            # Keep only the last 1000 entries
            self.knowledge["performance_metrics"]["memory_usage"] = self.knowledge["performance_metrics"]["memory_usage"][-1000:]
        
        # Save updated knowledge
        self._save_knowledge()
    
    def get_syntax_confidence(self, pattern_type, pattern_value):
        """Get confidence score for a syntax pattern"""
        pattern_key = f"{pattern_type}:{hashlib.md5(pattern_value.encode()).hexdigest()[:8]}"
        
        stats = self.knowledge["syntax_success"].get(pattern_key, {"success": 0, "failure": 0})
        success = stats["success"]
        failure = stats["failure"]
        
        if success + failure == 0:
            return 0.5  # Neutral confidence if no data
        
        return success / (success + failure)
    
    def get_common_errors(self, limit=10):
        """Get the most common error patterns"""
        error_patterns = [(key, data["count"], data["examples"]) for key, data in self.knowledge["error_patterns"].items()]
        error_patterns.sort(key=lambda x: x[1], reverse=True)
        
        return [{
            "id": key,
            "count": count,
            "examples": examples
        } for key, count, examples in error_patterns[:limit]]
    
    def get_performance_stats(self):
        """Get performance statistics"""
        execution_times = self.knowledge["performance_metrics"]["execution_times"]
        memory_usage = self.knowledge["performance_metrics"]["memory_usage"]
        
        return {
            "execution_time": {
                "mean": np.mean(execution_times) if execution_times else 0,
                "median": np.median(execution_times) if execution_times else 0,
                "min": min(execution_times) if execution_times else 0,
                "max": max(execution_times) if execution_times else 0
            },
            "memory_usage": {
                "mean": np.mean(memory_usage) if memory_usage else 0,
                "median": np.median(memory_usage) if memory_usage else 0,
                "min": min(memory_usage) if memory_usage else 0,
                "max": max(memory_usage) if memory_usage else 0
            }
        }

class FeedbackLoop:
    """Main feedback loop system"""
    
    def __init__(self):
        self.tracker = ExecutionTracker()
        self.extractor = PatternExtractor()
        self.analyzer = FeedbackAnalyzer()
    
    def track_execution(self, code, source_file=None, context=None):
        """Start tracking a code execution"""
        return self.tracker.start_execution(code, source_file, context)
    
    def record_output(self, output):
        """Record output from execution"""
        self.tracker.add_output(output)
    
    def record_error(self, error):
        """Record error from execution"""
        self.tracker.add_error(error)
    
    def complete_execution(self, success, execution_time, memory_usage=0):
        """Complete the execution tracking and process feedback"""
        execution_result = self.tracker.end_execution(success, execution_time, memory_usage)
        
        if execution_result:
            # Extract patterns from the execution
            code = self._get_code_from_execution(execution_result)
            patterns = self.extractor.extract_patterns(code, execution_result)
            
            # Analyze patterns
            self.analyzer.analyze_patterns(patterns)
            
            return execution_result["id"]
        
        return None
    
    def _get_code_from_execution(self, execution):
        """Get the code from an execution result"""
        # In a real implementation, we would store the code directly
        # For this example, we'll just return a placeholder
        return "// Code not available"
    
    def get_syntax_suggestions(self, code_snippet, pattern_type):
        """Get syntax suggestions based on feedback knowledge"""
        confidence = self.analyzer.get_syntax_confidence(pattern_type, code_snippet)
        
        if confidence < 0.3:
            return {
                "confidence": confidence,
                "suggestion": f"This {pattern_type} pattern has a low success rate. Consider revising.",
                "alternative": None
            }
        elif confidence > 0.8:
            return {
                "confidence": confidence,
                "suggestion": f"This {pattern_type} pattern has a high success rate.",
                "alternative": None
            }
        else:
            return {
                "confidence": confidence,
                "suggestion": f"This {pattern_type} pattern has a moderate success rate.",
                "alternative": None
            }
    
    def get_error_insights(self):
        """Get insights about common errors"""
        return self.analyzer.get_common_errors()
    
    def get_performance_insights(self):
        """Get insights about code performance"""
        return self.analyzer.get_performance_stats()
    
    def get_execution_history(self, limit=10):
        """Get recent execution history"""
        return self.tracker.get_recent_executions(limit)
    
    def get_feedback_summary(self):
        """Get a summary of the feedback system"""
        execution_stats = self.tracker.get_execution_stats()
        performance_stats = self.analyzer.get_performance_stats()
        error_insights = self.get_error_insights()[:3]  # Top 3 errors
        
        return {
            "executions": execution_stats,
            "performance": performance_stats,
            "top_errors": error_insights
        }

# Example usage
if __name__ == "__main__":
    feedback_loop = FeedbackLoop()
    
    # Simulate code execution
    execution_id = feedback_loop.track_execution("simula main\n    sulat \"Hello, World!\"\n    balik 0")
    feedback_loop.record_output("Hello, World!")
    feedback_loop.complete_execution(True, 0.01)
    
    # Get feedback summary
    print(feedback_loop.get_feedback_summary())
