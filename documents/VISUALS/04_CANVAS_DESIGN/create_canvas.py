"""
Mini-Agent System Architecture - Canvas Design
Following the "Modular Resonance" design philosophy
Creates a sophisticated visual representation of system components
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Circle
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

# Output configuration
OUTPUT_DIR = Path(__file__).parent
OUTPUT_FILE = OUTPUT_DIR / 'MINI_AGENT_SYSTEM_ARCHITECTURE_CANVAS.png'

# Design Philosophy Colors - Nature filtered through architecture
COLORS = {
    'infrastructure': '#4F46E5',  # Deep indigo - bedrock
    'core': '#6366F1',            # Indigo - foundation
    'user_interface': '#FB923C',  # Warm amber - invitation
    'skills': '#10B981',          # Verdant green - metabolism
    'integration': '#14B8A6',     # Teal - processing
    'tools': '#8B5CF6',           # Violet - capability
    'background': '#FAFAFA',      # Soft white
    'text': '#374151',            # Charcoal gray
}

def create_modular_node(ax, x, y, width, height, color, label, sublabels=None):
    """Create a rounded module with optional sub-elements"""
    # Main module with rounded corners
    module = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.03",
        facecolor=color,
        edgecolor='white',
        linewidth=2.5,
        alpha=0.92
    )
    ax.add_patch(module)
    
    # Main label
    ax.text(x + width/2, y + height - 0.15, label,
            ha='center', va='top',
            fontsize=9, color='white', fontweight='600',
            family='sans-serif')
    
    # Optional sublabels
    if sublabels:
        num_labels = len(sublabels)
        label_spacing = (height - 0.35) / (num_labels + 1)
        for i, sublabel in enumerate(sublabels):
            y_pos = y + height - 0.35 - (i + 1) * label_spacing
            # Small dots as visual markers
            ax.plot(x + 0.15, y_pos, 'o', color='white', markersize=3, alpha=0.7)
            ax.text(x + 0.25, y_pos, sublabel,
                    ha='left', va='center',
                    fontsize=6.5, color='white', alpha=0.9,
                    family='sans-serif')

def create_connection(ax, start_xy, end_xy, color, style='arc'):
    """Create organic connection lines between modules"""
    x1, y1 = start_xy
    x2, y2 = end_xy
    
    if style == 'arc':
        # Calculate control point for gentle curve
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        # Add perpendicular offset for curve
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        offset = 0.15  # Curve depth
        ctrl_x = mid_x + (-dy / length) * offset
        ctrl_y = mid_y + (dx / length) * offset
        
        # Quadratic bezier curve
        t = np.linspace(0, 1, 100)
        curve_x = (1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2
        curve_y = (1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2
        
        ax.plot(curve_x, curve_y, color=color, linewidth=1.8, alpha=0.35)
    else:
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=1.5, alpha=0.3)

# Create figure with design philosophy dimensions
fig, ax = plt.subplots(figsize=(16, 10), facecolor=COLORS['background'])
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

# Title - refined typographic gesture
ax.text(8, 9.3, 'M I N I - A G E N T', ha='center', va='top',
        fontsize=22, fontweight='700', color=COLORS['text'],
        family='sans-serif')
ax.text(8, 8.95, 'System Architecture', ha='center', va='top',
        fontsize=11, fontweight='300', color=COLORS['text'], alpha=0.7,
        family='sans-serif')

# ============ LAYER 1: Core Infrastructure (bottom) ============
create_modular_node(ax, 0.5, 0.5, 2.3, 1.8, COLORS['infrastructure'], 
                    'Configuration',
                    ['YAML Config', 'Environment', 'Secrets'])
create_modular_node(ax, 3.2, 0.5, 2.3, 1.8, COLORS['infrastructure'],
                    'Utilities', 
                    ['Credit Protection', 'File Ops', 'Logging'])

# ============ LAYER 2: LLM Integration ============
create_modular_node(ax, 6.2, 0.5, 2.0, 2.2, COLORS['integration'],
                    'OpenAI',
                    ['GPT-4', 'Web Tools'])
create_modular_node(ax, 8.5, 0.5, 2.0, 2.2, COLORS['integration'],
                    'MiniMax',
                    ['GLM-4.6', 'GLM-4.5'])
create_modular_node(ax, 10.8, 0.5, 2.0, 2.2, COLORS['integration'],
                    'Z.AI',
                    ['Coding Plan', 'Web Search'])

# ============ LAYER 3: Tools Layer ============
create_modular_node(ax, 0.5, 3.0, 2.0, 1.5, COLORS['tools'],
                    'Web Tools',
                    ['Search', 'Reader'])
create_modular_node(ax, 2.8, 3.0, 2.0, 1.5, COLORS['tools'],
                    'File System',
                    ['Read', 'Write'])
create_modular_node(ax, 5.1, 3.0, 2.0, 1.5, COLORS['tools'],
                    'Git Operations',
                    ['Status', 'Commit'])

# ============ LAYER 4: Skills Framework (Central metabolism) ============
# Document Skills
create_modular_node(ax, 7.8, 3.0, 1.5, 1.3, COLORS['skills'],
                    'PDF', ['Extract', 'Create'])
create_modular_node(ax, 9.5, 3.0, 1.5, 1.3, COLORS['skills'],
                    'DOCX', ['Edit', 'Format'])
create_modular_node(ax, 11.2, 3.0, 1.5, 1.3, COLORS['skills'],
                    'PPTX', ['Slides', 'Layout'])
create_modular_node(ax, 13.0, 3.0, 1.5, 1.3, COLORS['skills'],
                    'XLSX', ['Data', 'Formulas'])

# Visual & Creative Skills
create_modular_node(ax, 7.8, 4.6, 2.2, 1.4, COLORS['skills'],
                    'Canvas Design',
                    ['Philosophy', 'Aesthetics'])
create_modular_node(ax, 10.3, 4.6, 2.2, 1.4, COLORS['skills'],
                    'Algorithmic Art',
                    ['p5.js', 'Generative'])

# Development Skills
create_modular_node(ax, 12.8, 4.6, 2.2, 1.4, COLORS['skills'],
                    'MCP Builder',
                    ['Server', 'Tools'])

# Utility Skills
create_modular_node(ax, 0.5, 5.0, 2.0, 1.3, COLORS['skills'],
                    'Fact Checking',
                    ['Validation', 'QA'])
create_modular_node(ax, 2.8, 5.0, 2.0, 1.3, COLORS['skills'],
                    'Web Testing',
                    ['Playwright', 'Browser'])
create_modular_node(ax, 5.1, 5.0, 2.0, 1.3, COLORS['skills'],
                    'Theme Factory',
                    ['Styling', 'Themes'])

# ============ LAYER 5: Skill Orchestration ============
create_modular_node(ax, 3.5, 6.6, 5.5, 1.0, COLORS['core'],
                    'Skill Loading & Orchestration System',
                    ['Progressive Disclosure', 'Dynamic Loading', 'Tool Integration'])

# ============ LAYER 6: User Interface (top - invitation) ============
create_modular_node(ax, 0.8, 7.9, 2.8, 0.9, COLORS['user_interface'],
                    'CLI Interface', ['Command Line'])
create_modular_node(ax, 4.0, 7.9, 2.8, 0.9, COLORS['user_interface'],
                    'VS Code Extension', ['IDE Integration'])
create_modular_node(ax, 7.2, 7.9, 2.8, 0.9, COLORS['user_interface'],
                    'Python API', ['Direct Import'])

# ============ Organic Connections (mycelium network) ============

# Config/Utils → LLM Integration
for llm_x in [7.2, 9.5, 11.8]:
    create_connection(ax, (1.65, 2.3), (llm_x, 0.5), COLORS['infrastructure'])
    create_connection(ax, (4.35, 2.3), (llm_x, 0.5), COLORS['infrastructure'])

# LLM → Skills
for skill_x in [8.55, 10.25, 11.95, 13.75]:
    for llm_x in [7.2, 9.5, 11.8]:
        create_connection(ax, (llm_x, 2.7), (skill_x, 3.0), COLORS['integration'], 'arc')

for skill_x in [8.9, 11.4, 13.9]:
    for llm_x in [7.2, 9.5, 11.8]:
        create_connection(ax, (llm_x, 2.7), (skill_x, 4.6), COLORS['integration'], 'arc')

# Tools → Skills
for tool_x in [1.5, 3.8, 6.1]:
    for skill_x in [1.5, 3.8, 6.1]:
        create_connection(ax, (tool_x, 4.5), (skill_x, 5.0), COLORS['tools'], 'arc')

# Skills → Orchestration
for skill_x in [8.55, 10.25, 11.95, 13.75, 8.9, 11.4, 13.9, 1.5, 3.8, 6.1]:
    create_connection(ax, (skill_x, 5.0), (6.25, 6.6), COLORS['skills'], 'arc')

# Orchestration → UI
for ui_x in [2.2, 5.4, 8.6]:
    create_connection(ax, (6.25, 7.6), (ui_x, 7.9), COLORS['core'], 'arc')

# Add floating annotation labels (museum placard style)
annotations = [
    (0.3, 1.2, 'INFRASTRUCTURE', 5.5, COLORS['infrastructure']),
    (6.5, 1.5, 'LLM PROVIDERS', 5.5, COLORS['integration']),
    (0.3, 3.8, 'EXTERNAL TOOLS', 5.5, COLORS['tools']),
    (8.0, 5.8, 'SPECIALIZED SKILLS', 5.5, COLORS['skills']),
    (10.5, 7.2, 'ORCHESTRATION', 5.5, COLORS['core']),
    (3.5, 8.7, 'USER INTERACTION', 5.5, COLORS['user_interface']),
]

for x, y, text, size, color in annotations:
    ax.text(x, y, text, fontsize=size, color=color, alpha=0.5,
            fontweight='300', family='sans-serif',
            style='italic')

# Subtle footer annotation
ax.text(8, 0.15, 'Modular Resonance • System as Living Ecosystem', 
        ha='center', va='bottom',
        fontsize=7, color=COLORS['text'], alpha=0.4,
        family='sans-serif', style='italic')

plt.tight_layout(pad=0.5)
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', 
            facecolor=COLORS['background'], edgecolor='none')
print(f"✓ Canvas design created: {OUTPUT_FILE}")
print("  Following 'Modular Resonance' design philosophy")
print("  Expert-level craftsmanship • Museum-quality composition")
