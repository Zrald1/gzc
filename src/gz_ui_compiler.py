#!/usr/bin/env python3
"""
GZ UI Compiler
This module provides UI compilation capabilities for the GZ programming language.
"""

import os
import sys
import re
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gz_ui_compiler.log"),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger("GZ-UI-Compiler")

class UICompiler:
    """Compiler for GZ UI code"""
    
    def __init__(self):
        self.ui_elements = {}
        self.ui_layouts = {}
        self.ui_styles = {}
        self.ui_events = {}
        self.ui_code = ""
    
    def compile(self, code):
        """Compile UI code in GZ"""
        self.ui_code = code
        
        # Extract UI sections
        ui_sections = self._extract_ui_sections(code)
        
        if not ui_sections:
            logger.warning("No UI sections found in code")
            return {
                "success": True,
                "processed_code": code,
                "ui_elements": {},
                "ui_layouts": {},
                "ui_styles": {},
                "ui_events": {}
            }
        
        # Process each UI section
        for section_type, section_content in ui_sections:
            if section_type == "ui_element":
                self._process_ui_element(section_content)
            elif section_type == "ui_layout":
                self._process_ui_layout(section_content)
            elif section_type == "ui_style":
                self._process_ui_style(section_content)
            elif section_type == "ui_event":
                self._process_ui_event(section_content)
        
        # Generate code for UI elements
        generated_code = self._generate_ui_code()
        
        # Replace UI sections with generated code
        processed_code = self._replace_ui_sections(code, generated_code)
        
        return {
            "success": True,
            "processed_code": processed_code,
            "ui_elements": self.ui_elements,
            "ui_layouts": self.ui_layouts,
            "ui_styles": self.ui_styles,
            "ui_events": self.ui_events
        }
    
    def _extract_ui_sections(self, code):
        """Extract UI sections from code"""
        sections = []
        
        # Match UI element sections
        element_pattern = r'ui_element\s+(\w+)\s*{([^}]*)}'
        for match in re.finditer(element_pattern, code, re.DOTALL):
            element_name = match.group(1)
            element_content = match.group(2)
            sections.append(("ui_element", (element_name, element_content)))
        
        # Match UI layout sections
        layout_pattern = r'ui_layout\s+(\w+)\s*{([^}]*)}'
        for match in re.finditer(layout_pattern, code, re.DOTALL):
            layout_name = match.group(1)
            layout_content = match.group(2)
            sections.append(("ui_layout", (layout_name, layout_content)))
        
        # Match UI style sections
        style_pattern = r'ui_style\s+(\w+)\s*{([^}]*)}'
        for match in re.finditer(style_pattern, code, re.DOTALL):
            style_name = match.group(1)
            style_content = match.group(2)
            sections.append(("ui_style", (style_name, style_content)))
        
        # Match UI event sections
        event_pattern = r'ui_event\s+(\w+)\s*{([^}]*)}'
        for match in re.finditer(event_pattern, code, re.DOTALL):
            event_name = match.group(1)
            event_content = match.group(2)
            sections.append(("ui_event", (event_name, event_content)))
        
        return sections
    
    def _process_ui_element(self, element_data):
        """Process a UI element section"""
        element_name, element_content = element_data
        
        # Parse element properties
        properties = {}
        for line in element_content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            if ':' in line:
                key, value = line.split(':', 1)
                properties[key.strip()] = value.strip().rstrip(';')
        
        # Store the element
        self.ui_elements[element_name] = properties
        
        logger.info(f"Processed UI element: {element_name}")
    
    def _process_ui_layout(self, layout_data):
        """Process a UI layout section"""
        layout_name, layout_content = layout_data
        
        # Parse layout structure
        layout = []
        for line in layout_content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            # Handle element placement
            if '->' in line:
                parent, child = line.split('->', 1)
                layout.append({
                    "type": "child",
                    "parent": parent.strip(),
                    "child": child.strip().rstrip(';')
                })
            # Handle element positioning
            elif '@' in line:
                element, position = line.split('@', 1)
                layout.append({
                    "type": "position",
                    "element": element.strip(),
                    "position": position.strip().rstrip(';')
                })
        
        # Store the layout
        self.ui_layouts[layout_name] = layout
        
        logger.info(f"Processed UI layout: {layout_name}")
    
    def _process_ui_style(self, style_data):
        """Process a UI style section"""
        style_name, style_content = style_data
        
        # Parse style properties
        properties = {}
        for line in style_content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            if ':' in line:
                key, value = line.split(':', 1)
                properties[key.strip()] = value.strip().rstrip(';')
        
        # Store the style
        self.ui_styles[style_name] = properties
        
        logger.info(f"Processed UI style: {style_name}")
    
    def _process_ui_event(self, event_data):
        """Process a UI event section"""
        event_name, event_content = event_data
        
        # Parse event handlers
        handlers = []
        current_handler = None
        
        for line in event_content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            # Handle event definition
            if 'on' in line and ':' in line:
                parts = line.split(':', 1)
                event_def = parts[0].strip()
                action = parts[1].strip().rstrip(';')
                
                # Parse event definition
                if 'on' in event_def:
                    element, event_type = event_def.split('on', 1)
                    handlers.append({
                        "element": element.strip(),
                        "event": f"on{event_type.strip()}",
                        "action": action
                    })
        
        # Store the events
        self.ui_events[event_name] = handlers
        
        logger.info(f"Processed UI events: {event_name}")
    
    def _generate_ui_code(self):
        """Generate code for UI elements"""
        # In a real implementation, this would generate platform-specific UI code
        # For now, we'll generate GZ code that creates a simple UI
        
        code = []
        
        # Generate code for UI initialization
        code.append("// Generated UI code")
        code.append("simula init_ui")
        
        # Create UI elements
        for element_name, properties in self.ui_elements.items():
            element_type = properties.get("type", "window")
            code.append(f"    // Create {element_name}")
            code.append(f"    {element_name} = create_ui_element(\"{element_type}\")")
            
            # Set properties
            for prop_name, prop_value in properties.items():
                if prop_name != "type":
                    code.append(f"    set_property({element_name}, \"{prop_name}\", \"{prop_value}\")")
        
        # Apply layouts
        for layout_name, layout in self.ui_layouts.items():
            code.append(f"    // Apply layout {layout_name}")
            for item in layout:
                if item["type"] == "child":
                    code.append(f"    add_child({item['parent']}, {item['child']})")
                elif item["type"] == "position":
                    code.append(f"    set_position({item['element']}, \"{item['position']}\")")
        
        # Apply styles
        for style_name, properties in self.ui_styles.items():
            code.append(f"    // Apply style {style_name}")
            for element_name in self.ui_elements:
                code.append(f"    apply_style({element_name}, \"{style_name}\")")
        
        # Register event handlers
        for event_group, handlers in self.ui_events.items():
            code.append(f"    // Register events for {event_group}")
            for handler in handlers:
                code.append(f"    register_event({handler['element']}, \"{handler['event']}\", {handler['action']})")
        
        code.append("    balik tama")
        
        # Generate event handler functions
        for event_group, handlers in self.ui_events.items():
            for handler in handlers:
                action = handler["action"]
                if action.startswith("function_"):
                    code.append(f"simula {action}")
                    code.append(f"    // Event handler for {handler['element']} {handler['event']}")
                    code.append(f"    sulat \"Event {handler['event']} triggered on {handler['element']}\"")
                    code.append(f"    balik tama")
        
        return "\n".join(code)
    
    def _replace_ui_sections(self, original_code, generated_code):
        """Replace UI sections with generated code"""
        # Remove all UI sections
        processed_code = original_code
        
        # Remove UI element sections
        processed_code = re.sub(r'ui_element\s+\w+\s*{[^}]*}', '', processed_code)
        
        # Remove UI layout sections
        processed_code = re.sub(r'ui_layout\s+\w+\s*{[^}]*}', '', processed_code)
        
        # Remove UI style sections
        processed_code = re.sub(r'ui_style\s+\w+\s*{[^}]*}', '', processed_code)
        
        # Remove UI event sections
        processed_code = re.sub(r'ui_event\s+\w+\s*{[^}]*}', '', processed_code)
        
        # Add generated code at the end
        processed_code += "\n\n" + generated_code
        
        return processed_code

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gz_ui_compiler.py <source_file>", file=sys.stderr)
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
    
    # Compile UI code
    compiler = UICompiler()
    result = compiler.compile(code)
    
    if result["success"]:
        print(result["processed_code"])
    else:
        print(f"Error: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
