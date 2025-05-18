#!/usr/bin/env python3
"""
AI Integration Module for GZ Programming Language
This module integrates all the advanced AI capabilities into a unified system.
"""

import os
import sys
import json
import time
import logging
import threading
from datetime import datetime

# Import all AI capability modules
from gz_exponential_learning import ExponentialLearner
from gz_persistent_memory import PersistentMemory
from gz_self_improvement import SelfImprovementEngine
from gz_feedback_loop import FeedbackLoop
from gz_transfer_learning import KnowledgeTransfer
from gz_progressive_optimization import ProgressiveOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("models/ai_integration.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("GZ-AI-Integration")

class AICapabilities:
    """Unified interface for all AI capabilities"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.initialized = False
        
        # Default configuration
        self.default_config = {
            "exponential_learning": {
                "enabled": True,
                "base_learning_rate": 0.01,
                "acceleration_factor": 100
            },
            "persistent_memory": {
                "enabled": True,
                "use_database": False
            },
            "self_improvement": {
                "enabled": True,
                "improvement_interval": 3600  # 1 hour
            },
            "feedback_loop": {
                "enabled": True
            },
            "transfer_learning": {
                "enabled": True
            },
            "progressive_optimization": {
                "enabled": True
            }
        }
        
        # Merge with provided config
        for section, options in self.default_config.items():
            if section not in self.config:
                self.config[section] = {}
            
            for option, value in options.items():
                if option not in self.config[section]:
                    self.config[section][option] = value
        
        # Initialize components
        self.learner = None
        self.memory = None
        self.improvement_engine = None
        self.feedback_loop = None
        self.knowledge_transfer = None
        self.optimizer = None
        
        # Statistics
        self.stats = {
            "initialization_time": 0,
            "code_samples_processed": 0,
            "optimizations_applied": 0,
            "corrections_made": 0,
            "knowledge_transfers": 0,
            "self_improvements": 0
        }
    
    def initialize(self):
        """Initialize all AI capabilities"""
        start_time = time.time()
        
        try:
            # Initialize exponential learning
            if self.config["exponential_learning"]["enabled"]:
                logger.info("Initializing exponential learning...")
                self.learner = ExponentialLearner(
                    base_learning_rate=self.config["exponential_learning"]["base_learning_rate"],
                    acceleration_factor=self.config["exponential_learning"]["acceleration_factor"]
                )
            
            # Initialize persistent memory
            if self.config["persistent_memory"]["enabled"]:
                logger.info("Initializing persistent memory...")
                self.memory = PersistentMemory(
                    use_database=self.config["persistent_memory"]["use_database"]
                )
            
            # Initialize self-improvement engine
            if self.config["self_improvement"]["enabled"]:
                logger.info("Initializing self-improvement engine...")
                self.improvement_engine = SelfImprovementEngine(
                    improvement_interval=self.config["self_improvement"]["improvement_interval"]
                )
            
            # Initialize feedback loop
            if self.config["feedback_loop"]["enabled"]:
                logger.info("Initializing feedback loop...")
                self.feedback_loop = FeedbackLoop()
            
            # Initialize knowledge transfer
            if self.config["transfer_learning"]["enabled"]:
                logger.info("Initializing knowledge transfer...")
                self.knowledge_transfer = KnowledgeTransfer()
            
            # Initialize progressive optimizer
            if self.config["progressive_optimization"]["enabled"]:
                logger.info("Initializing progressive optimizer...")
                self.optimizer = ProgressiveOptimizer()
            
            self.initialized = True
            self.stats["initialization_time"] = time.time() - start_time
            
            logger.info(f"AI capabilities initialized in {self.stats['initialization_time']:.2f} seconds")
            
            # Start self-improvement engine if enabled
            if self.improvement_engine:
                self.improvement_engine.start()
            
            return True
        
        except Exception as e:
            logger.error(f"Error initializing AI capabilities: {str(e)}")
            return False
    
    def shutdown(self):
        """Shutdown all AI capabilities"""
        logger.info("Shutting down AI capabilities...")
        
        # Stop self-improvement engine
        if self.improvement_engine:
            self.improvement_engine.stop()
        
        # Close persistent memory
        if self.memory:
            self.memory.close()
        
        logger.info("AI capabilities shutdown complete")
    
    def process_code(self, code, context=None):
        """Process a code sample through all AI capabilities"""
        if not self.initialized:
            logger.warning("AI capabilities not initialized")
            return {"error": "AI capabilities not initialized"}
        
        context = context or {}
        results = {}
        
        try:
            # Track execution with feedback loop
            if self.feedback_loop:
                execution_id = self.feedback_loop.track_execution(code, context.get("source_file"))
                results["execution_id"] = execution_id
            
            # Learn from the code sample
            if self.learner:
                learning_result = self.learner.learn_from_sample(code)
                results["learning"] = learning_result
            
            # Store in persistent memory
            if self.memory:
                code_hash = context.get("code_hash", hash(code))
                self.memory.store("code_snippets", str(code_hash), code, 1.0, context)
            
            # Extract concepts and store in knowledge transfer
            if self.knowledge_transfer:
                transfer_result = self.knowledge_transfer.learn_from_code(code, context)
                results["transfer_learning"] = transfer_result
            
            self.stats["code_samples_processed"] += 1
            
            return results
        
        except Exception as e:
            logger.error(f"Error processing code: {str(e)}")
            return {"error": str(e)}
    
    def optimize_code(self, code, level=None):
        """Optimize code using progressive optimization"""
        if not self.initialized:
            logger.warning("AI capabilities not initialized")
            return {"error": "AI capabilities not initialized"}
        
        try:
            if self.optimizer:
                optimization_result = self.optimizer.optimize(code, force_level=level)
                self.stats["optimizations_applied"] += 1
                return optimization_result
            else:
                return {"error": "Progressive optimizer not initialized"}
        
        except Exception as e:
            logger.error(f"Error optimizing code: {str(e)}")
            return {"error": str(e)}
    
    def correct_code(self, code, error_message=None):
        """Correct syntax errors in code"""
        if not self.initialized:
            logger.warning("AI capabilities not initialized")
            return {"error": "AI capabilities not initialized"}
        
        try:
            # Use feedback loop to analyze error patterns
            if self.feedback_loop and error_message:
                self.feedback_loop.record_error(error_message)
            
            # Use knowledge transfer to find similar code
            if self.knowledge_transfer:
                similar_code = self.knowledge_transfer.find_similar_code(code, threshold=0.6, limit=1)
                
                if similar_code:
                    # Use the most similar code as a reference
                    reference_code = similar_code[0]["code"]
                    
                    # Simple correction: replace problematic parts
                    corrected_code = code
                    
                    # For demonstration, just fix common syntax errors
                    corrections = [
                        ("simula main()", "simula main"),
                        ("sulat(", "sulat "),
                        ("kung(", "kung "),
                        ("para(", "para "),
                        ("habang(", "habang "),
                        (";", ""),
                        ("{", ""),
                        ("}", "")
                    ]
                    
                    for old, new in corrections:
                        if old in corrected_code:
                            corrected_code = corrected_code.replace(old, new)
                    
                    self.stats["corrections_made"] += 1
                    
                    return {
                        "corrected_code": corrected_code,
                        "original_code": code,
                        "reference_code": reference_code,
                        "corrections_made": corrected_code != code
                    }
            
            # If no correction was made
            return {
                "corrected_code": code,
                "original_code": code,
                "corrections_made": False
            }
        
        except Exception as e:
            logger.error(f"Error correcting code: {str(e)}")
            return {"error": str(e)}
    
    def transfer_knowledge(self, source_code, target_context):
        """Transfer knowledge from source code to a new context"""
        if not self.initialized:
            logger.warning("AI capabilities not initialized")
            return {"error": "AI capabilities not initialized"}
        
        try:
            if self.knowledge_transfer:
                transfer_result = self.knowledge_transfer.transfer_knowledge(source_code, target_context)
                self.stats["knowledge_transfers"] += 1
                return transfer_result
            else:
                return {"error": "Knowledge transfer not initialized"}
        
        except Exception as e:
            logger.error(f"Error transferring knowledge: {str(e)}")
            return {"error": str(e)}
    
    def get_suggestions(self, code):
        """Get suggestions for improving code"""
        if not self.initialized:
            logger.warning("AI capabilities not initialized")
            return {"error": "AI capabilities not initialized"}
        
        try:
            suggestions = []
            
            # Get optimization suggestions
            if self.optimizer:
                optimization_level = self.optimizer.current_level
                suggestions.append({
                    "type": "optimization",
                    "description": f"Code can be optimized at level {optimization_level}",
                    "action": "optimize"
                })
            
            # Get knowledge transfer suggestions
            if self.knowledge_transfer:
                transfer_suggestions = self.knowledge_transfer.suggest_improvements(code)
                for suggestion in transfer_suggestions:
                    suggestions.append({
                        "type": "knowledge_transfer",
                        "description": suggestion["description"],
                        "confidence": suggestion.get("confidence", 0.5),
                        "action": "apply_pattern"
                    })
            
            # Get feedback loop suggestions
            if self.feedback_loop:
                error_insights = self.feedback_loop.get_error_insights()
                if error_insights:
                    suggestions.append({
                        "type": "error_prevention",
                        "description": f"Avoid common error: {error_insights[0]['examples'][0]['message'] if error_insights[0]['examples'] else 'Unknown error'}",
                        "action": "review"
                    })
            
            return {
                "suggestions": suggestions,
                "count": len(suggestions)
            }
        
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            return {"error": str(e)}
    
    def get_stats(self):
        """Get statistics about AI capabilities"""
        stats = self.stats.copy()
        
        # Add component-specific stats
        if self.learner:
            stats["learning"] = self.learner.get_learning_stats()
        
        if self.memory:
            stats["memory"] = self.memory.get_stats()
        
        if self.improvement_engine:
            stats["self_improvement"] = self.improvement_engine.get_improvement_stats()
        
        if self.feedback_loop:
            stats["feedback_loop"] = self.feedback_loop.get_feedback_summary()
        
        if self.knowledge_transfer:
            stats["knowledge_transfer"] = self.knowledge_transfer.get_knowledge_stats()
        
        if self.optimizer:
            stats["optimization"] = self.optimizer.get_optimization_stats()
        
        return stats

# Example usage
if __name__ == "__main__":
    # Create and initialize AI capabilities
    ai = AICapabilities()
    ai.initialize()
    
    # Process a code sample
    code = """
    simula fibonacci n
        kung n <= 1
            balik n
        balik fibonacci(n-1) + fibonacci(n-2)

    simula main
        para i 0 10
            sulat fibonacci(i)
        balik 0
    """
    
    result = ai.process_code(code, {"source_file": "example.gz"})
    print(f"Processing result: {result}")
    
    # Optimize the code
    optimization = ai.optimize_code(code)
    print(f"Optimized code: {optimization['optimized_code']}")
    
    # Get suggestions
    suggestions = ai.get_suggestions(code)
    print(f"Suggestions: {suggestions}")
    
    # Get stats
    stats = ai.get_stats()
    print(f"AI stats: {stats}")
    
    # Shutdown
    ai.shutdown()
