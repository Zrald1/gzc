#!/usr/bin/env python3
"""
Exponential Learning Module for GZ Programming Language
This module implements accelerated learning capabilities where the AI learns
100 times faster with each code sample it processes.
"""

import numpy as np
import json
import os
import time
from datetime import datetime
import hashlib

class ExponentialLearner:
    def __init__(self, base_learning_rate=0.01, acceleration_factor=100, memory_path="models/gz_memory"):
        self.base_learning_rate = base_learning_rate
        self.acceleration_factor = acceleration_factor
        self.memory_path = memory_path
        self.samples_processed = 0
        self.learning_rate = base_learning_rate
        self.pattern_weights = {}
        self.last_update_time = time.time()
        self.knowledge_graph = {}
        self.pattern_confidence = {}
        self.learning_history = []
        
        # Create memory directory if it doesn't exist
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        
        # Load existing memory if available
        self.load_memory()
    
    def calculate_learning_rate(self):
        """Calculate the current learning rate based on exponential growth"""
        if self.samples_processed == 0:
            return self.base_learning_rate
        
        # Exponential growth formula: base_rate * acceleration_factor^(samples_processed)
        # We use a dampened version to prevent numerical overflow
        exponent = min(self.samples_processed / 100, 10)  # Cap at 10 to prevent overflow
        return self.base_learning_rate * (self.acceleration_factor ** exponent)
    
    def extract_patterns(self, code_sample):
        """Extract patterns from a code sample for learning"""
        patterns = {}
        
        # Extract syntax patterns (simplified example)
        lines = code_sample.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                continue
            
            # Function definitions
            if line.startswith('simula '):
                pattern_key = "function_definition"
                pattern_value = line
                patterns[pattern_key] = pattern_value
            
            # Variable assignments
            elif ' = ' in line and not line.startswith('kung '):
                pattern_key = "variable_assignment"
                pattern_value = line
                patterns[pattern_key] = pattern_value
            
            # Print statements
            elif line.startswith('sulat '):
                pattern_key = "print_statement"
                pattern_value = line
                patterns[pattern_key] = pattern_value
            
            # Conditional statements
            elif line.startswith('kung '):
                pattern_key = "conditional"
                pattern_value = line
                patterns[pattern_key] = pattern_value
            
            # Loop statements
            elif line.startswith('para ') or line.startswith('habang '):
                pattern_key = "loop"
                pattern_value = line
                patterns[pattern_key] = pattern_value
            
            # Return statements
            elif line.startswith('balik '):
                pattern_key = "return_statement"
                pattern_value = line
                patterns[pattern_key] = pattern_value
        
        # Extract semantic patterns (more complex)
        # This would involve analyzing the code structure, control flow, etc.
        # For simplicity, we'll just use a basic approach here
        
        # Check for common algorithms
        code_lower = code_sample.lower()
        if 'fibonacci' in code_lower:
            patterns["algorithm"] = "fibonacci"
        elif 'factorial' in code_lower:
            patterns["algorithm"] = "factorial"
        elif 'prime' in code_lower:
            patterns["algorithm"] = "prime_numbers"
        elif 'sort' in code_lower:
            patterns["algorithm"] = "sorting"
        
        return patterns
    
    def learn_from_sample(self, code_sample, execution_result=None, feedback=None):
        """Learn from a code sample with exponential acceleration"""
        # Extract patterns from the code sample
        patterns = self.extract_patterns(code_sample)
        
        # Calculate current learning rate
        self.learning_rate = self.calculate_learning_rate()
        
        # Update pattern weights based on learning rate
        for pattern_key, pattern_value in patterns.items():
            # Create a unique identifier for this pattern
            pattern_id = f"{pattern_key}:{hashlib.md5(pattern_value.encode()).hexdigest()}"
            
            # Initialize if not seen before
            if pattern_id not in self.pattern_weights:
                self.pattern_weights[pattern_id] = 1.0
                self.pattern_confidence[pattern_id] = 0.5  # Start with moderate confidence
            
            # Update weight based on learning rate
            self.pattern_weights[pattern_id] *= (1 + self.learning_rate)
            
            # Update confidence based on execution result
            if execution_result is not None:
                if execution_result == "success":
                    self.pattern_confidence[pattern_id] = min(1.0, self.pattern_confidence[pattern_id] + 0.1)
                else:
                    self.pattern_confidence[pattern_id] = max(0.1, self.pattern_confidence[pattern_id] - 0.1)
            
            # Add to knowledge graph
            if pattern_key not in self.knowledge_graph:
                self.knowledge_graph[pattern_key] = []
            
            if pattern_value not in self.knowledge_graph[pattern_key]:
                self.knowledge_graph[pattern_key].append(pattern_value)
        
        # Record learning event
        self.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "patterns_count": len(patterns),
            "learning_rate": self.learning_rate,
            "execution_result": execution_result
        })
        
        # Increment samples processed
        self.samples_processed += 1
        
        # Save memory periodically (every 5 samples or if it's been more than 5 minutes)
        if self.samples_processed % 5 == 0 or (time.time() - self.last_update_time) > 300:
            self.save_memory()
            self.last_update_time = time.time()
        
        return {
            "samples_processed": self.samples_processed,
            "learning_rate": self.learning_rate,
            "patterns_learned": len(patterns),
            "total_patterns_known": len(self.pattern_weights)
        }
    
    def get_pattern_suggestions(self, pattern_key, threshold=0.5):
        """Get suggestions for a specific pattern type based on learned weights"""
        if pattern_key not in self.knowledge_graph:
            return []
        
        suggestions = []
        for pattern in self.knowledge_graph[pattern_key]:
            pattern_id = f"{pattern_key}:{hashlib.md5(pattern.encode()).hexdigest()}"
            if pattern_id in self.pattern_weights and self.pattern_confidence[pattern_id] >= threshold:
                suggestions.append({
                    "pattern": pattern,
                    "weight": self.pattern_weights.get(pattern_id, 1.0),
                    "confidence": self.pattern_confidence.get(pattern_id, 0.5)
                })
        
        # Sort by weight * confidence
        suggestions.sort(key=lambda x: x["weight"] * x["confidence"], reverse=True)
        return suggestions
    
    def save_memory(self):
        """Save the learner's memory to disk"""
        memory_data = {
            "samples_processed": self.samples_processed,
            "base_learning_rate": self.base_learning_rate,
            "acceleration_factor": self.acceleration_factor,
            "pattern_weights": self.pattern_weights,
            "pattern_confidence": self.pattern_confidence,
            "knowledge_graph": self.knowledge_graph,
            "learning_history": self.learning_history[-100:]  # Keep only the last 100 entries
        }
        
        with open(f"{self.memory_path}.json", 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def load_memory(self):
        """Load the learner's memory from disk"""
        try:
            with open(f"{self.memory_path}.json", 'r') as f:
                memory_data = json.load(f)
            
            self.samples_processed = memory_data.get("samples_processed", 0)
            self.base_learning_rate = memory_data.get("base_learning_rate", self.base_learning_rate)
            self.acceleration_factor = memory_data.get("acceleration_factor", self.acceleration_factor)
            self.pattern_weights = memory_data.get("pattern_weights", {})
            self.pattern_confidence = memory_data.get("pattern_confidence", {})
            self.knowledge_graph = memory_data.get("knowledge_graph", {})
            self.learning_history = memory_data.get("learning_history", [])
            
            # Recalculate learning rate
            self.learning_rate = self.calculate_learning_rate()
            
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            # No memory file or invalid format
            return False
    
    def get_learning_stats(self):
        """Get statistics about the learning progress"""
        return {
            "samples_processed": self.samples_processed,
            "current_learning_rate": self.learning_rate,
            "patterns_known": len(self.pattern_weights),
            "knowledge_categories": list(self.knowledge_graph.keys()),
            "high_confidence_patterns": sum(1 for conf in self.pattern_confidence.values() if conf > 0.8),
            "learning_acceleration": self.learning_rate / self.base_learning_rate
        }

# Example usage
if __name__ == "__main__":
    learner = ExponentialLearner()
    
    # Example code sample
    code_sample = """
    simula fibonacci n
        kung n <= 1
            balik n
        balik fibonacci(n-1) + fibonacci(n-2)

    simula main
        para i 0 10
            sulat fibonacci(i)
        balik 0
    """
    
    # Learn from the sample
    result = learner.learn_from_sample(code_sample, execution_result="success")
    print(f"Learning result: {result}")
    
    # Get suggestions for function definitions
    suggestions = learner.get_pattern_suggestions("function_definition")
    print(f"Function definition suggestions: {suggestions}")
    
    # Save memory
    learner.save_memory()
