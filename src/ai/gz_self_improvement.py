#!/usr/bin/env python3
"""
GZ Self-Improvement and GitHub Update Module
This module enables the GZ compiler to learn from user code, improve itself,
and automatically update the GitHub repository with new learnings.
"""

import os
import sys
import json
import time
import logging
import subprocess
import hashlib
import re
import random
import uuid
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gz_self_improvement.log"),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger("GZ-Self-Improvement")

class SelfImprovement:
    """Self-improvement and GitHub update system for GZ"""

    def __init__(self, config=None):
        self.config = config or {}

        # Default configuration
        self.default_config = {
            "github_repo": "https://github.com/Zrald1/gzc.git",
            "github_branch": "main",
            "github_username": "Zrald1",
            "github_token_env": "GZ_GITHUB_TOKEN",
            "memory_file": os.path.expanduser("~/.gz/models/collective_memory.json"),
            "update_interval": 86400,  # 24 hours in seconds
            "improvement_threshold": 10,  # Number of new learnings before triggering an update
            "auto_update": True
        }

        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value

        # Initialize memory
        self.memory = {
            "last_update": 0,
            "collective_learnings": {},
            "improvement_count": 0,
            "update_history": []
        }

        # Load memory if available
        self._load_memory()

        # Statistics
        self.stats = {
            "improvements_made": 0,
            "updates_pushed": 0,
            "last_update_time": 0
        }

    def _load_memory(self):
        """Load memory from file"""
        try:
            if os.path.exists(self.config["memory_file"]):
                with open(self.config["memory_file"], 'r') as f:
                    loaded_memory = json.load(f)

                # Update memory with loaded data
                for key, value in loaded_memory.items():
                    self.memory[key] = value

                logger.info(f"Collective memory loaded from {self.config['memory_file']}")
                return True
            else:
                logger.info("No collective memory file found, using default memory")
                return False
        except Exception as e:
            logger.error(f"Error loading collective memory: {str(e)}")
            return False

    def _save_memory(self):
        """Save memory to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config["memory_file"]), exist_ok=True)

            with open(self.config["memory_file"], 'w') as f:
                json.dump(self.memory, f, indent=2)

            logger.info(f"Collective memory saved to {self.config['memory_file']}")
            return True
        except Exception as e:
            logger.error(f"Error saving collective memory: {str(e)}")
            return False

    def add_learning(self, learning_type, learning_data):
        """Add a new learning to the collective memory"""
        try:
            # Create a unique ID for this learning
            learning_id = hashlib.md5(json.dumps(learning_data).encode()).hexdigest()

            # Check if this learning already exists
            if learning_id in self.memory["collective_learnings"]:
                # Update existing learning
                existing_learning = self.memory["collective_learnings"][learning_id]
                existing_learning["frequency"] += 1
                existing_learning["last_seen"] = time.time()

                logger.info(f"Updated existing learning: {learning_id}")
                return learning_id

            # Add new learning
            self.memory["collective_learnings"][learning_id] = {
                "type": learning_type,
                "data": learning_data,
                "frequency": 1,
                "confidence": 0.5,  # Start with moderate confidence
                "created": time.time(),
                "last_seen": time.time()
            }

            # Increment improvement count
            self.memory["improvement_count"] += 1

            # Update statistics
            self.stats["improvements_made"] += 1

            # Save memory
            self._save_memory()

            logger.info(f"Added new learning: {learning_id}")

            # Check if we should update GitHub
            self._check_for_update()

            return learning_id

        except Exception as e:
            logger.error(f"Error adding learning: {str(e)}")
            return None

    def _check_for_update(self):
        """Check if we should update the GitHub repository"""
        if not self.config["auto_update"]:
            return False

        current_time = time.time()
        time_since_last_update = current_time - self.memory["last_update"]

        # Check if enough time has passed and we have enough new learnings
        if (time_since_last_update >= self.config["update_interval"] and
            self.memory["improvement_count"] >= self.config["improvement_threshold"]):

            # Update GitHub
            success = self._update_github()

            if success:
                # Reset improvement count
                self.memory["improvement_count"] = 0

                # Update last update time
                self.memory["last_update"] = current_time

                # Add to update history
                self.memory["update_history"].append({
                    "timestamp": current_time,
                    "improvements": self.stats["improvements_made"],
                    "success": True
                })

                # Update statistics
                self.stats["updates_pushed"] += 1
                self.stats["last_update_time"] = current_time

                # Save memory
                self._save_memory()

                return True

        return False

    def _update_github(self):
        """Update the GitHub repository with new learnings"""
        try:
            # Create a unique temporary directory for the repository
            temp_base = os.path.expanduser("~/.gz/temp")
            os.makedirs(temp_base, exist_ok=True)

            # Generate a unique ID for this update
            unique_id = str(uuid.uuid4())
            temp_dir = os.path.join(temp_base, f"repo_{unique_id}")

            logger.info(f"Using temporary directory: {temp_dir}")

            # Create the directory
            os.makedirs(temp_dir, exist_ok=True)

            # Clone the repository
            logger.info(f"Cloning repository: {self.config['github_repo']}")
            clone_cmd = f"git clone {self.config['github_repo']} {temp_dir}"
            subprocess.run(clone_cmd, shell=True, check=True)

            # Update the repository with new learnings
            logger.info("Updating repository with new learnings")

            # Update the memory files
            self._update_memory_files(temp_dir)

            # Update the AI modules
            self._update_ai_modules(temp_dir)

            # Commit and push changes
            logger.info("Committing and pushing changes")

            # Configure Git
            git_config_cmd = f"cd {temp_dir} && git config user.name '{self.config['github_username']}' && git config user.email '{self.config['github_username']}@users.noreply.github.com'"
            subprocess.run(git_config_cmd, shell=True, check=True)

            # Add changes
            git_add_cmd = f"cd {temp_dir} && git add ."
            subprocess.run(git_add_cmd, shell=True, check=True)

            # Commit changes
            commit_message = f"Auto-update: Added {self.memory['improvement_count']} new learnings [AI-generated]"
            git_commit_cmd = f"cd {temp_dir} && git commit -m \"{commit_message}\""

            # Check if there are changes to commit
            try:
                subprocess.run(git_commit_cmd, shell=True, check=True)
            except subprocess.CalledProcessError:
                # No changes to commit, create an empty commit
                logger.info("No changes to commit, creating empty commit")
                git_commit_cmd = f"cd {temp_dir} && git commit --allow-empty -m \"Auto-update: No new learnings [AI-generated]\""
                subprocess.run(git_commit_cmd, shell=True, check=True)

            # Push changes
            git_token = os.environ.get(self.config["github_token_env"])
            if git_token:
                # Use token for authentication
                repo_url = self.config["github_repo"].replace("https://", f"https://{self.config['github_username']}:{git_token}@")
                git_push_cmd = f"cd {temp_dir} && git push {repo_url} {self.config['github_branch']}"
            else:
                # Use SSH or cached credentials
                git_push_cmd = f"cd {temp_dir} && git push origin {self.config['github_branch']}"

            subprocess.run(git_push_cmd, shell=True, check=True)

            # Clean up
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory: {temp_dir}, error: {str(e)}")

            logger.info("Successfully updated GitHub repository")
            return True

        except Exception as e:
            logger.error(f"Error updating GitHub repository: {str(e)}")
            return False

    def _update_memory_files(self, repo_dir):
        """Update memory files in the repository"""
        try:
            # Create models directory if it doesn't exist
            models_dir = os.path.join(repo_dir, "models")
            os.makedirs(models_dir, exist_ok=True)

            # Copy collective memory
            collective_memory_path = os.path.join(models_dir, "collective_memory.json")
            with open(collective_memory_path, 'w') as f:
                json.dump(self.memory["collective_learnings"], f, indent=2)

            # Create a summary file
            summary_path = os.path.join(models_dir, "learning_summary.md")
            with open(summary_path, 'w') as f:
                f.write("# GZ Collective Learning Summary\n\n")
                f.write(f"Last updated: {datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Total learnings: {len(self.memory['collective_learnings'])}\n")
                f.write(f"Updates pushed: {self.stats['updates_pushed']}\n\n")

                # Add learning types summary
                learning_types = {}
                for learning_id, learning in self.memory["collective_learnings"].items():
                    learning_type = learning["type"]
                    if learning_type not in learning_types:
                        learning_types[learning_type] = 0
                    learning_types[learning_type] += 1

                f.write("## Learning Types\n\n")
                for learning_type, count in learning_types.items():
                    f.write(f"- {learning_type}: {count}\n")

                f.write("\n## Recent Learnings\n\n")

                # Add recent learnings
                recent_learnings = sorted(
                    self.memory["collective_learnings"].items(),
                    key=lambda x: x[1]["last_seen"],
                    reverse=True
                )[:10]

                for learning_id, learning in recent_learnings:
                    f.write(f"### {learning['type']} ({datetime.fromtimestamp(learning['created']).strftime('%Y-%m-%d')})\n")
                    f.write(f"Frequency: {learning['frequency']}, Confidence: {learning['confidence']:.2f}\n\n")
                    f.write("```\n")
                    f.write(json.dumps(learning['data'], indent=2))
                    f.write("\n```\n\n")

            logger.info("Updated memory files in repository")
            return True

        except Exception as e:
            logger.error(f"Error updating memory files: {str(e)}")
            return False

    def _update_ai_modules(self, repo_dir):
        """Update AI modules in the repository based on learnings"""
        try:
            # Create src directory if it doesn't exist
            src_dir = os.path.join(repo_dir, "src", "ai")
            os.makedirs(src_dir, exist_ok=True)

            # Update correction rules
            self._update_correction_rules(src_dir)

            # Update optimization rules
            self._update_optimization_rules(src_dir)

            # Update code templates
            self._update_code_templates(src_dir)

            logger.info("Updated AI modules in repository")
            return True

        except Exception as e:
            logger.error(f"Error updating AI modules: {str(e)}")
            return False

    def _update_correction_rules(self, src_dir):
        """Update correction rules based on learnings"""
        # Get correction learnings
        correction_learnings = [
            learning for _, learning in self.memory["collective_learnings"].items()
            if learning["type"] == "correction_rule" and learning["confidence"] > 0.6
        ]

        if not correction_learnings:
            return

        # Read the AI integration file
        ai_integration_path = os.path.join(src_dir, "gz_ai_integration.py")
        if not os.path.exists(ai_integration_path):
            return

        with open(ai_integration_path, 'r') as f:
            content = f.read()

        # Find the correction rules section
        correction_rules_pattern = r'self\.memory\["correction_rules"\]\s*=\s*{([^}]*)}'
        match = re.search(correction_rules_pattern, content, re.DOTALL)

        if not match:
            return

        # Generate new correction rules
        new_rules = "        self.memory[\"correction_rules\"] = {\n"

        # Add existing rules
        existing_rules = match.group(1)
        new_rules += existing_rules

        # Add new rules from learnings
        for learning in correction_learnings:
            rule_data = learning["data"]
            if "pattern" in rule_data and "replacement" in rule_data:
                rule_name = rule_data.get("name", f"rule_{random.randint(1000, 9999)}")

                # Check if rule already exists
                if f'"{rule_name}"' in existing_rules:
                    continue

                new_rules += f',\n            "{rule_name}": {{\n'
                new_rules += f'                "pattern": r"{rule_data["pattern"]}",\n'
                new_rules += f'                "replacement": r"{rule_data["replacement"]}",\n'

                if "explanation" in rule_data:
                    new_rules += f'                "explanation": "{rule_data["explanation"]}"\n'
                else:
                    new_rules += f'                "explanation": "Auto-generated correction rule"\n'

                new_rules += '            }'

        new_rules += "\n        }"

        # Replace the correction rules section
        updated_content = re.sub(correction_rules_pattern, new_rules, content, flags=re.DOTALL)

        # Write the updated file
        with open(ai_integration_path, 'w') as f:
            f.write(updated_content)

        logger.info("Updated correction rules in AI integration module")

    def _update_optimization_rules(self, src_dir):
        """Update optimization rules based on learnings"""
        # Get optimization learnings
        optimization_learnings = [
            learning for _, learning in self.memory["collective_learnings"].items()
            if learning["type"] == "optimization_rule" and learning["confidence"] > 0.6
        ]

        if not optimization_learnings:
            return

        # Read the AI integration file
        ai_integration_path = os.path.join(src_dir, "gz_ai_integration.py")
        if not os.path.exists(ai_integration_path):
            return

        with open(ai_integration_path, 'r') as f:
            content = f.read()

        # Find the optimization rules section
        optimization_rules_pattern = r'self\.memory\["optimization_rules"\]\s*=\s*{([^}]*)}'
        match = re.search(optimization_rules_pattern, content, re.DOTALL)

        if not match:
            return

        # Generate new optimization rules
        new_rules = "        self.memory[\"optimization_rules\"] = {\n"

        # Add existing rules
        existing_rules = match.group(1)
        new_rules += existing_rules

        # Add new rules from learnings
        for learning in optimization_learnings:
            rule_data = learning["data"]
            if "pattern" in rule_data and "replacement" in rule_data:
                rule_name = rule_data.get("name", f"rule_{random.randint(1000, 9999)}")

                # Check if rule already exists
                if f'"{rule_name}"' in existing_rules:
                    continue

                new_rules += f',\n            "{rule_name}": {{\n'
                new_rules += f'                "pattern": r"{rule_data["pattern"]}",\n'
                new_rules += f'                "replacement": r"{rule_data["replacement"]}",\n'

                if "explanation" in rule_data:
                    new_rules += f'                "explanation": "{rule_data["explanation"]}"\n'
                else:
                    new_rules += f'                "explanation": "Auto-generated optimization rule"\n'

                new_rules += '            }'

        new_rules += "\n        }"

        # Replace the optimization rules section
        updated_content = re.sub(optimization_rules_pattern, new_rules, content, flags=re.DOTALL)

        # Write the updated file
        with open(ai_integration_path, 'w') as f:
            f.write(updated_content)

        logger.info("Updated optimization rules in AI integration module")

    def _update_code_templates(self, src_dir):
        """Update code templates based on learnings"""
        # Get template learnings
        template_learnings = [
            learning for _, learning in self.memory["collective_learnings"].items()
            if learning["type"] == "code_template" and learning["confidence"] > 0.7
        ]

        if not template_learnings:
            return

        # Read the AI integration file
        ai_integration_path = os.path.join(src_dir, "gz_ai_integration.py")
        if not os.path.exists(ai_integration_path):
            return

        with open(ai_integration_path, 'r') as f:
            content = f.read()

        # Find the code templates section
        templates_pattern = r'self\.memory\["code_templates"\]\s*=\s*{([^}]*)}'
        match = re.search(templates_pattern, content, re.DOTALL)

        if not match:
            return

        # Generate new templates
        new_templates = "        self.memory[\"code_templates\"] = {\n"

        # Add existing templates
        existing_templates = match.group(1)
        new_templates += existing_templates

        # Add new templates from learnings
        for learning in template_learnings:
            template_data = learning["data"]
            if "name" in template_data and "code" in template_data:
                template_name = template_data["name"]

                # Check if template already exists
                if f'"{template_name}"' in existing_templates:
                    continue

                # Escape triple quotes in code
                template_code = template_data["code"].replace('"""', '\\"\\"\\"')

                new_templates += f',\n            "{template_name}": """\n{template_code}\n"""'

        new_templates += "\n        }"

        # Replace the templates section
        updated_content = re.sub(templates_pattern, new_templates, content, flags=re.DOTALL)

        # Write the updated file
        with open(ai_integration_path, 'w') as f:
            f.write(updated_content)

        logger.info("Updated code templates in AI integration module")

    def force_update(self):
        """Force an update to the GitHub repository"""
        logger.info("Forcing update to GitHub repository")

        # Update GitHub
        success = self._update_github()

        if success:
            # Reset improvement count
            self.memory["improvement_count"] = 0

            # Update last update time
            self.memory["last_update"] = time.time()

            # Add to update history
            self.memory["update_history"].append({
                "timestamp": time.time(),
                "improvements": self.stats["improvements_made"],
                "success": True
            })

            # Update statistics
            self.stats["updates_pushed"] += 1
            self.stats["last_update_time"] = time.time()

            # Save memory
            self._save_memory()

            return True

        return False

    def get_stats(self):
        """Get statistics about self-improvement"""
        stats = self.stats.copy()

        # Add memory statistics
        stats["memory"] = {
            "total_learnings": len(self.memory["collective_learnings"]),
            "improvement_count": self.memory["improvement_count"],
            "updates_pushed": len(self.memory["update_history"])
        }

        # Add learning type statistics
        learning_types = {}
        for learning_id, learning in self.memory["collective_learnings"].items():
            learning_type = learning["type"]
            if learning_type not in learning_types:
                learning_types[learning_type] = 0
            learning_types[learning_type] += 1

        stats["learning_types"] = learning_types

        return stats

# Example usage
if __name__ == "__main__":
    self_improvement = SelfImprovement()

    # Add a new learning
    learning_data = {
        "pattern": r"simula\s+(\w+)\s*\(",
        "replacement": r"simula \1 ",
        "explanation": "In GZ, function declarations don't use parentheses"
    }

    learning_id = self_improvement.add_learning("correction_rule", learning_data)
    print(f"Added learning: {learning_id}")

    # Force an update
    success = self_improvement.force_update()
    print(f"Update success: {success}")

    # Get stats
    stats = self_improvement.get_stats()
    print(f"Stats: {stats}")
