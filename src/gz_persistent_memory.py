#!/usr/bin/env python3
"""
Persistent Memory System for GZ Programming Language
This module implements a robust memory system that ensures the AI never forgets
patterns, optimizations, or corrections it has learned.
"""

import os
import json
import sqlite3
import time
import hashlib
from datetime import datetime
import pickle

class PersistentMemory:
    def __init__(self, memory_dir="models/memory", use_database=True):
        self.memory_dir = memory_dir
        self.use_database = use_database
        self.memory_cache = {}
        self.last_sync_time = time.time()
        self.sync_interval = 60  # Sync to disk every 60 seconds
        self.memory_categories = [
            "syntax_patterns",
            "optimization_rules",
            "correction_rules",
            "code_templates",
            "algorithm_patterns",
            "error_patterns",
            "user_preferences"
        ]
        
        # Create memory directory if it doesn't exist
        os.makedirs(memory_dir, exist_ok=True)
        
        # Initialize memory files or database
        self._initialize_storage()
        
        # Load all memory categories
        self._load_all_memory()
    
    def _initialize_storage(self):
        """Initialize the storage system (files or database)"""
        if self.use_database:
            self.db_path = os.path.join(self.memory_dir, "gz_memory.db")
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Create tables if they don't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_items (
                    id TEXT PRIMARY KEY,
                    category TEXT,
                    key TEXT,
                    value BLOB,
                    confidence REAL,
                    usage_count INTEGER,
                    last_used TEXT,
                    created TEXT,
                    metadata TEXT
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_stats (
                    category TEXT PRIMARY KEY,
                    item_count INTEGER,
                    last_updated TEXT,
                    total_usage INTEGER
                )
            ''')
            
            self.conn.commit()
        else:
            # Create memory files for each category if they don't exist
            for category in self.memory_categories:
                file_path = os.path.join(self.memory_dir, f"{category}.json")
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        json.dump({}, f)
    
    def _load_all_memory(self):
        """Load all memory categories into cache"""
        for category in self.memory_categories:
            self._load_memory_category(category)
    
    def _load_memory_category(self, category):
        """Load a specific memory category into cache"""
        if category not in self.memory_categories:
            raise ValueError(f"Unknown memory category: {category}")
        
        if self.use_database:
            self.cursor.execute("SELECT key, value, confidence, usage_count, metadata FROM memory_items WHERE category = ?", (category,))
            items = self.cursor.fetchall()
            
            category_data = {}
            for key, value_blob, confidence, usage_count, metadata_json in items:
                value = pickle.loads(value_blob)
                metadata = json.loads(metadata_json) if metadata_json else {}
                
                category_data[key] = {
                    "value": value,
                    "confidence": confidence,
                    "usage_count": usage_count,
                    "metadata": metadata
                }
            
            self.memory_cache[category] = category_data
        else:
            file_path = os.path.join(self.memory_dir, f"{category}.json")
            try:
                with open(file_path, 'r') as f:
                    self.memory_cache[category] = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # Reset if file is corrupted or missing
                self.memory_cache[category] = {}
                with open(file_path, 'w') as f:
                    json.dump({}, f)
    
    def _save_memory_category(self, category):
        """Save a specific memory category to storage"""
        if category not in self.memory_categories:
            raise ValueError(f"Unknown memory category: {category}")
        
        if self.use_database:
            # First, delete all existing items in this category
            self.cursor.execute("DELETE FROM memory_items WHERE category = ?", (category,))
            
            # Then insert all current items
            for key, item_data in self.memory_cache[category].items():
                value_blob = pickle.dumps(item_data["value"])
                metadata_json = json.dumps(item_data.get("metadata", {}))
                
                self.cursor.execute(
                    "INSERT INTO memory_items (id, category, key, value, confidence, usage_count, last_used, created, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        f"{category}:{key}",
                        category,
                        key,
                        value_blob,
                        item_data.get("confidence", 1.0),
                        item_data.get("usage_count", 0),
                        datetime.now().isoformat(),
                        item_data.get("created", datetime.now().isoformat()),
                        metadata_json
                    )
                )
            
            # Update stats
            self.cursor.execute(
                "INSERT OR REPLACE INTO memory_stats (category, item_count, last_updated, total_usage) VALUES (?, ?, ?, ?)",
                (
                    category,
                    len(self.memory_cache[category]),
                    datetime.now().isoformat(),
                    sum(item.get("usage_count", 0) for item in self.memory_cache[category].values())
                )
            )
            
            self.conn.commit()
        else:
            file_path = os.path.join(self.memory_dir, f"{category}.json")
            with open(file_path, 'w') as f:
                json.dump(self.memory_cache[category], f, indent=2)
    
    def store(self, category, key, value, confidence=1.0, metadata=None):
        """Store an item in memory"""
        if category not in self.memory_categories:
            raise ValueError(f"Unknown memory category: {category}")
        
        if category not in self.memory_cache:
            self.memory_cache[category] = {}
        
        # Check if item already exists
        if key in self.memory_cache[category]:
            # Update existing item
            item = self.memory_cache[category][key]
            
            # Never decrease confidence for existing items (persistent memory)
            new_confidence = max(confidence, item.get("confidence", 0.0))
            
            # Update usage count
            usage_count = item.get("usage_count", 0) + 1
            
            # Update metadata
            if metadata:
                item_metadata = item.get("metadata", {})
                item_metadata.update(metadata)
            else:
                item_metadata = item.get("metadata", {})
            
            self.memory_cache[category][key] = {
                "value": value,
                "confidence": new_confidence,
                "usage_count": usage_count,
                "last_used": datetime.now().isoformat(),
                "metadata": item_metadata
            }
        else:
            # Create new item
            self.memory_cache[category][key] = {
                "value": value,
                "confidence": confidence,
                "usage_count": 1,
                "created": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
        
        # Sync to disk if it's been a while
        if time.time() - self.last_sync_time > self.sync_interval:
            self.sync()
    
    def retrieve(self, category, key, default=None):
        """Retrieve an item from memory"""
        if category not in self.memory_categories:
            raise ValueError(f"Unknown memory category: {category}")
        
        if category not in self.memory_cache:
            return default
        
        if key not in self.memory_cache[category]:
            return default
        
        # Update usage statistics
        item = self.memory_cache[category][key]
        item["usage_count"] = item.get("usage_count", 0) + 1
        item["last_used"] = datetime.now().isoformat()
        
        return item["value"]
    
    def search(self, category, query=None, min_confidence=0.0, limit=10):
        """Search for items in memory"""
        if category not in self.memory_categories:
            raise ValueError(f"Unknown memory category: {category}")
        
        if category not in self.memory_cache:
            return []
        
        results = []
        
        for key, item in self.memory_cache[category].items():
            # Skip items with confidence below threshold
            if item.get("confidence", 0.0) < min_confidence:
                continue
            
            # If query is provided, check if it's in the key or value
            if query:
                key_match = query.lower() in key.lower()
                
                # Check if value contains the query (if value is a string)
                value_match = False
                if isinstance(item["value"], str):
                    value_match = query.lower() in item["value"].lower()
                
                if not (key_match or value_match):
                    continue
            
            # Add to results
            results.append({
                "key": key,
                "value": item["value"],
                "confidence": item.get("confidence", 1.0),
                "usage_count": item.get("usage_count", 0),
                "last_used": item.get("last_used", ""),
                "metadata": item.get("metadata", {})
            })
        
        # Sort by confidence and usage count
        results.sort(key=lambda x: (x["confidence"], x["usage_count"]), reverse=True)
        
        # Apply limit
        if limit > 0:
            results = results[:limit]
        
        return results
    
    def get_all(self, category, min_confidence=0.0):
        """Get all items in a category"""
        if category not in self.memory_categories:
            raise ValueError(f"Unknown memory category: {category}")
        
        if category not in self.memory_cache:
            return {}
        
        # Filter by confidence
        return {
            key: item["value"]
            for key, item in self.memory_cache[category].items()
            if item.get("confidence", 0.0) >= min_confidence
        }
    
    def remove(self, category, key):
        """Remove an item from memory (not typically used in persistent memory)"""
        if category not in self.memory_categories:
            raise ValueError(f"Unknown memory category: {category}")
        
        if category in self.memory_cache and key in self.memory_cache[category]:
            # Instead of deleting, mark with very low confidence
            self.memory_cache[category][key]["confidence"] = 0.01
            return True
        
        return False
    
    def sync(self):
        """Sync all memory to disk"""
        for category in self.memory_categories:
            if category in self.memory_cache:
                self._save_memory_category(category)
        
        self.last_sync_time = time.time()
    
    def get_stats(self):
        """Get memory statistics"""
        stats = {}
        
        for category in self.memory_categories:
            if category in self.memory_cache:
                items = self.memory_cache[category]
                stats[category] = {
                    "item_count": len(items),
                    "high_confidence_items": sum(1 for item in items.values() if item.get("confidence", 0) > 0.8),
                    "total_usage": sum(item.get("usage_count", 0) for item in items.values()),
                    "avg_confidence": sum(item.get("confidence", 0) for item in items.values()) / max(1, len(items))
                }
        
        return stats
    
    def close(self):
        """Close the memory system and ensure all data is saved"""
        self.sync()
        
        if self.use_database and hasattr(self, 'conn'):
            self.conn.close()

# Example usage
if __name__ == "__main__":
    memory = PersistentMemory()
    
    # Store some syntax patterns
    memory.store("syntax_patterns", "function_definition", "simula {name} {params}", 1.0)
    memory.store("syntax_patterns", "print_statement", "sulat {expression}", 1.0)
    
    # Store some optimization rules
    memory.store("optimization_rules", "increment", {
        "pattern": "{var} = {var} + 1",
        "replacement": "{var} += 1",
        "explanation": "Use compound assignment for increment"
    }, 0.9)
    
    # Retrieve and use
    print(memory.retrieve("syntax_patterns", "function_definition"))
    
    # Search
    print(memory.search("optimization_rules", "increment"))
    
    # Get stats
    print(memory.get_stats())
    
    # Close properly
    memory.close()
