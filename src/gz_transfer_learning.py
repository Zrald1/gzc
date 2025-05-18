#!/usr/bin/env python3
"""
Transfer Learning System for GZ Programming Language
This module implements a system that allows knowledge gained from one programming
task to be applied to different contexts.
"""

import os
import json
import numpy as np
import hashlib
import logging
from datetime import datetime
from collections import defaultdict
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("models/transfer_learning.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("GZ-Transfer-Learning")

class KnowledgeEmbedding:
    """Represents code and concepts as embeddings for transfer learning"""
    
    def __init__(self, embedding_dim=64):
        self.embedding_dim = embedding_dim
        self.code_embeddings = {}
        self.concept_embeddings = {}
        self.embedding_similarity_cache = {}
    
    def _generate_embedding(self, text, seed=None):
        """
        Generate a simple embedding for text
        Note: In a real implementation, this would use a proper embedding model
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Create a deterministic seed from the text
        text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(text_hash)
        
        # Generate a random embedding (in a real system, this would be a proper embedding)
        embedding = np.random.normal(0, 1, self.embedding_dim)
        
        # Normalize to unit length
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def get_code_embedding(self, code):
        """Get embedding for a code snippet"""
        code_hash = hashlib.md5(code.encode()).hexdigest()
        
        if code_hash not in self.code_embeddings:
            # Generate embedding for this code
            self.code_embeddings[code_hash] = self._generate_embedding(code)
        
        return self.code_embeddings[code_hash]
    
    def get_concept_embedding(self, concept):
        """Get embedding for a concept"""
        if concept not in self.concept_embeddings:
            # Generate embedding for this concept
            self.concept_embeddings[concept] = self._generate_embedding(concept)
        
        return self.concept_embeddings[concept]
    
    def compute_similarity(self, embedding1, embedding2):
        """Compute cosine similarity between two embeddings"""
        # Check cache first
        cache_key = f"{hash(embedding1.tobytes())}-{hash(embedding2.tobytes())}"
        if cache_key in self.embedding_similarity_cache:
            return self.embedding_similarity_cache[cache_key]
        
        # Compute cosine similarity
        similarity = np.dot(embedding1, embedding2)
        
        # Cache the result
        self.embedding_similarity_cache[cache_key] = similarity
        
        return similarity
    
    def find_similar_code(self, code, threshold=0.7, limit=5):
        """Find similar code snippets"""
        query_embedding = self.get_code_embedding(code)
        
        similarities = []
        for code_hash, embedding in self.code_embeddings.items():
            if code_hash != hashlib.md5(code.encode()).hexdigest():
                similarity = self.compute_similarity(query_embedding, embedding)
                if similarity >= threshold:
                    similarities.append((code_hash, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:limit]
    
    def find_related_concepts(self, code, threshold=0.6, limit=5):
        """Find concepts related to a code snippet"""
        code_embedding = self.get_code_embedding(code)
        
        similarities = []
        for concept, embedding in self.concept_embeddings.items():
            similarity = self.compute_similarity(code_embedding, embedding)
            if similarity >= threshold:
                similarities.append((concept, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:limit]

class ConceptExtractor:
    """Extracts programming concepts from code"""
    
    def __init__(self):
        # Define concept patterns
        self.concept_patterns = {
            "recursion": r"simula\s+(\w+).*\n.*\1\s*\(",
            "iteration": r"para\s+|habang\s+",
            "conditional": r"kung\s+|kundi\s+",
            "function_definition": r"simula\s+\w+",
            "variable_assignment": r"\w+\s*=\s*",
            "arithmetic": r"[+\-*/]",
            "string_manipulation": r"\".*\"",
            "list_operation": r"\[\s*\]|\[\s*\w+\s*\]",
            "error_handling": r"try\s+|catch\s+|except\s+",
            "file_io": r"open\s*\(|read\s*\(|write\s*\(",
            "sorting": r"sort\s*\(|sorted\s*\(",
            "searching": r"find\s*\(|search\s*\(|index\s*\(",
            "matrix_operation": r"\w+\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]"
        }
    
    def extract_concepts(self, code):
        """Extract programming concepts from code"""
        concepts = {}
        
        for concept, pattern in self.concept_patterns.items():
            matches = re.findall(pattern, code)
            if matches:
                concepts[concept] = len(matches)
        
        return concepts
    
    def extract_algorithm_type(self, code):
        """Try to identify the algorithm type"""
        code_lower = code.lower()
        
        algorithm_patterns = {
            "sorting": ["sort", "bubble", "quick", "merge", "insertion"],
            "searching": ["search", "find", "binary search", "linear search"],
            "graph": ["graph", "node", "edge", "vertex", "adjacency"],
            "dynamic_programming": ["dynamic", "memoization", "memo", "fibonacci"],
            "recursion": ["recursion", "recursive"],
            "mathematical": ["math", "factorial", "prime", "number"],
            "string_processing": ["string", "substring", "concatenate"],
            "data_structure": ["list", "array", "stack", "queue", "tree", "hash"]
        }
        
        algorithm_scores = {}
        
        for algo_type, keywords in algorithm_patterns.items():
            score = sum(1 for keyword in keywords if keyword in code_lower)
            if score > 0:
                algorithm_scores[algo_type] = score
        
        if not algorithm_scores:
            return "unknown"
        
        # Return the algorithm type with the highest score
        return max(algorithm_scores.items(), key=lambda x: x[1])[0]

class KnowledgeTransfer:
    """Manages transfer of knowledge between different programming contexts"""
    
    def __init__(self, knowledge_file="models/transfer_knowledge.json"):
        self.knowledge_file = knowledge_file
        self.embeddings = KnowledgeEmbedding()
        self.concept_extractor = ConceptExtractor()
        self.knowledge_base = {
            "code_snippets": {},
            "concepts": {},
            "algorithms": {},
            "patterns": {},
            "transformations": []
        }
        
        # Load knowledge if available
        self._load_knowledge()
    
    def _load_knowledge(self):
        """Load knowledge from file"""
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r') as f:
                    self.knowledge_base = json.load(f)
        except Exception as e:
            logger.error(f"Error loading transfer knowledge: {str(e)}")
    
    def _save_knowledge(self):
        """Save knowledge to file"""
        try:
            os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
            with open(self.knowledge_file, 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving transfer knowledge: {str(e)}")
    
    def learn_from_code(self, code, metadata=None):
        """Learn from a code snippet"""
        code_hash = hashlib.md5(code.encode()).hexdigest()
        
        # Extract concepts
        concepts = self.concept_extractor.extract_concepts(code)
        
        # Identify algorithm type
        algorithm_type = self.concept_extractor.extract_algorithm_type(code)
        
        # Store code snippet
        self.knowledge_base["code_snippets"][code_hash] = {
            "code": code,
            "concepts": concepts,
            "algorithm_type": algorithm_type,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Update concept knowledge
        for concept, count in concepts.items():
            if concept not in self.knowledge_base["concepts"]:
                self.knowledge_base["concepts"][concept] = {
                    "examples": [],
                    "total_occurrences": 0
                }
            
            # Add this code as an example if we don't have too many
            if len(self.knowledge_base["concepts"][concept]["examples"]) < 5:
                self.knowledge_base["concepts"][concept]["examples"].append(code_hash)
            
            # Update occurrence count
            self.knowledge_base["concepts"][concept]["total_occurrences"] += count
        
        # Update algorithm knowledge
        if algorithm_type != "unknown":
            if algorithm_type not in self.knowledge_base["algorithms"]:
                self.knowledge_base["algorithms"][algorithm_type] = {
                    "examples": [],
                    "count": 0
                }
            
            # Add this code as an example if we don't have too many
            if len(self.knowledge_base["algorithms"][algorithm_type]["examples"]) < 5:
                self.knowledge_base["algorithms"][algorithm_type]["examples"].append(code_hash)
            
            # Update count
            self.knowledge_base["algorithms"][algorithm_type]["count"] += 1
        
        # Generate embedding for this code
        self.embeddings.get_code_embedding(code)
        
        # Save updated knowledge
        self._save_knowledge()
        
        return {
            "code_hash": code_hash,
            "concepts": concepts,
            "algorithm_type": algorithm_type
        }
    
    def learn_transformation(self, source_code, target_code, transformation_type, metadata=None):
        """Learn a code transformation"""
        source_hash = hashlib.md5(source_code.encode()).hexdigest()
        target_hash = hashlib.md5(target_code.encode()).hexdigest()
        
        # Store the transformation
        transformation = {
            "source_hash": source_hash,
            "target_hash": target_hash,
            "transformation_type": transformation_type,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.knowledge_base["transformations"].append(transformation)
        
        # Make sure both code snippets are in the knowledge base
        if source_hash not in self.knowledge_base["code_snippets"]:
            self.learn_from_code(source_code)
        
        if target_hash not in self.knowledge_base["code_snippets"]:
            self.learn_from_code(target_code)
        
        # Save updated knowledge
        self._save_knowledge()
        
        return transformation
    
    def find_similar_code(self, code, threshold=0.7, limit=5):
        """Find similar code snippets"""
        similar_hashes = self.embeddings.find_similar_code(code, threshold, limit)
        
        results = []
        for code_hash, similarity in similar_hashes:
            if code_hash in self.knowledge_base["code_snippets"]:
                snippet = self.knowledge_base["code_snippets"][code_hash]
                results.append({
                    "code_hash": code_hash,
                    "similarity": similarity,
                    "code": snippet["code"],
                    "concepts": snippet["concepts"],
                    "algorithm_type": snippet["algorithm_type"]
                })
        
        return results
    
    def find_applicable_transformations(self, code, threshold=0.7, limit=3):
        """Find transformations that might be applicable to this code"""
        code_embedding = self.embeddings.get_code_embedding(code)
        
        applicable_transformations = []
        
        for transformation in self.knowledge_base["transformations"]:
            source_hash = transformation["source_hash"]
            
            if source_hash in self.knowledge_base["code_snippets"]:
                source_code = self.knowledge_base["code_snippets"][source_hash]["code"]
                source_embedding = self.embeddings.get_code_embedding(source_code)
                
                similarity = self.embeddings.compute_similarity(code_embedding, source_embedding)
                
                if similarity >= threshold:
                    target_hash = transformation["target_hash"]
                    target_code = self.knowledge_base["code_snippets"][target_hash]["code"] if target_hash in self.knowledge_base["code_snippets"] else None
                    
                    applicable_transformations.append({
                        "transformation_type": transformation["transformation_type"],
                        "similarity": similarity,
                        "source_code": source_code,
                        "target_code": target_code,
                        "metadata": transformation["metadata"]
                    })
        
        # Sort by similarity (descending)
        applicable_transformations.sort(key=lambda x: x["similarity"], reverse=True)
        
        return applicable_transformations[:limit]
    
    def suggest_improvements(self, code):
        """Suggest improvements for a code snippet based on learned knowledge"""
        # Extract concepts from the code
        concepts = self.concept_extractor.extract_concepts(code)
        
        # Find similar code
        similar_code = self.find_similar_code(code, threshold=0.6, limit=3)
        
        # Find applicable transformations
        transformations = self.find_applicable_transformations(code, threshold=0.6, limit=3)
        
        # Generate suggestions
        suggestions = []
        
        # Suggestions based on similar code
        for similar in similar_code:
            suggestions.append({
                "type": "similar_code",
                "confidence": similar["similarity"],
                "description": f"Found similar code with {len(similar['concepts'])} concepts",
                "example": similar["code"]
            })
        
        # Suggestions based on transformations
        for transform in transformations:
            suggestions.append({
                "type": "transformation",
                "confidence": transform["similarity"],
                "description": f"Suggested transformation: {transform['transformation_type']}",
                "source": transform["source_code"],
                "target": transform["target_code"]
            })
        
        # Suggestions based on concepts
        for concept, count in concepts.items():
            if concept in self.knowledge_base["concepts"]:
                concept_info = self.knowledge_base["concepts"][concept]
                
                if concept_info["examples"]:
                    example_hash = concept_info["examples"][0]
                    example_code = self.knowledge_base["code_snippets"][example_hash]["code"] if example_hash in self.knowledge_base["code_snippets"] else None
                    
                    suggestions.append({
                        "type": "concept",
                        "confidence": 0.8,
                        "description": f"Concept '{concept}' identified ({count} occurrences)",
                        "example": example_code
                    })
        
        return suggestions
    
    def transfer_knowledge(self, source_code, target_context):
        """Transfer knowledge from source code to a new context"""
        # Extract concepts from source code
        source_concepts = self.concept_extractor.extract_concepts(source_code)
        
        # Find similar code that matches the target context
        similar_code = []
        
        for code_hash, snippet in self.knowledge_base["code_snippets"].items():
            # Check if this snippet matches the target context
            if target_context in snippet.get("metadata", {}).get("context", ""):
                # Generate embeddings if needed
                source_embedding = self.embeddings.get_code_embedding(source_code)
                snippet_embedding = self.embeddings.get_code_embedding(snippet["code"])
                
                # Compute similarity
                similarity = self.embeddings.compute_similarity(source_embedding, snippet_embedding)
                
                if similarity >= 0.5:
                    similar_code.append({
                        "code": snippet["code"],
                        "similarity": similarity,
                        "concepts": snippet["concepts"]
                    })
        
        # Sort by similarity
        similar_code.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Generate adapted code (in a real system, this would be more sophisticated)
        if similar_code:
            best_match = similar_code[0]
            
            return {
                "adapted_code": best_match["code"],
                "similarity": best_match["similarity"],
                "source_concepts": source_concepts,
                "target_concepts": best_match["concepts"]
            }
        
        return {
            "adapted_code": source_code,
            "similarity": 0,
            "source_concepts": source_concepts,
            "target_concepts": {}
        }
    
    def get_knowledge_stats(self):
        """Get statistics about the knowledge base"""
        return {
            "code_snippets": len(self.knowledge_base["code_snippets"]),
            "concepts": len(self.knowledge_base["concepts"]),
            "algorithms": len(self.knowledge_base["algorithms"]),
            "transformations": len(self.knowledge_base["transformations"]),
            "top_concepts": sorted(
                [(concept, info["total_occurrences"]) for concept, info in self.knowledge_base["concepts"].items()],
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "top_algorithms": sorted(
                [(algo, info["count"]) for algo, info in self.knowledge_base["algorithms"].items()],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

# Example usage
if __name__ == "__main__":
    transfer = KnowledgeTransfer()
    
    # Learn from a code snippet
    fibonacci_code = """
    simula fibonacci n
        kung n <= 1
            balik n
        balik fibonacci(n-1) + fibonacci(n-2)

    simula main
        para i 0 10
            sulat fibonacci(i)
        balik 0
    """
    
    result = transfer.learn_from_code(fibonacci_code, {"context": "mathematical"})
    print(f"Learned from code: {result}")
    
    # Find similar code
    similar = transfer.find_similar_code(fibonacci_code)
    print(f"Similar code: {len(similar)} found")
    
    # Get knowledge stats
    stats = transfer.get_knowledge_stats()
    print(f"Knowledge stats: {stats}")
