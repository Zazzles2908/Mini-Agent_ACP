"""
Mini-Agent System Visualizations
Generates multiple chart types for system understanding
Run with: uv run python documents/VISUALS/03_PYTHON_CHARTS/generate_all_charts.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Ensure output directory exists
OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)

# Color palette
COLORS = {
    'primary': '#6366F1',      # Indigo
    'secondary': '#EC4899',    # Pink
    'accent': '#10B981',       # Emerald
    'warning': '#F59E0B',      # Amber
    'info': '#3B82F6',         # Blue
    'light': '#F3F4F6',        # Gray 100
    'dark': '#374151',         # Gray 700
}

def chart_1_skill_distribution():
    """Pie chart showing skill categories"""
    categories = ['Document\nProcessing', 'Visual\nDesign', 'Development\nTools', 
                  'Utility\nSkills', 'Web\nIntegration']
    sizes = [4, 2, 2, 4, 2]  # docx/pdf/pptx/xlsx, canvas/algo, mcp/webapp, fact-check/slack/theme/skill-creator, web tools
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    explode = (0.05, 0.05, 0.05, 0.05, 0.05)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=categories,
                                       colors=colors, autopct='%1.0f%%',
                                       shadow=True, startangle=90)
    
    plt.setp(autotexts, size=10, weight='bold')
    plt.setp(texts, size=11)
    ax.set_title('Mini-Agent Skills Distribution\n14 Specialized Skills', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'skill_distribution.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Generated skill_distribution.png")

def chart_2_codebase_metrics():
    """Bar chart of codebase metrics"""
    categories = ['Core\nModules', 'Test\nScripts', 'Skills', 'Docs', 'Config\nFiles']
    values = [50, 85, 14, 100, 8]
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
              COLORS['warning'], COLORS['info']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
    
    # Add value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val}+' if val >= 50 else str(val),
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Mini-Agent Codebase Metrics', fontsize=14, fontweight='bold')
    ax.set_ylim(0, max(values) * 1.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'codebase_metrics.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Generated codebase_metrics.png")

def chart_3_system_layers():
    """Horizontal stacked bar showing system layers"""
    layers = ['User Interface', 'Skills Framework', 'LLM Integration', 
              'Tool Layer', 'Core Infrastructure']
    
    # Components per layer
    components = {
        'User Interface': ['CLI', 'VS Code Extension', 'Python API'],
        'Skills Framework': ['Skill Loader', 'Document Skills', 'Visual Skills', 'Dev Skills'],
        'LLM Integration': ['OpenAI', 'MiniMax GLM', 'Z.AI Client'],
        'Tool Layer': ['Web Search', 'Web Reader', 'File Ops', 'Git Ops'],
        'Core Infrastructure': ['Config Manager', 'Credit Protection', 'Utils']
    }
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    y_positions = range(len(layers))
    colors_cycle = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
                    COLORS['warning'], COLORS['info'], '#9333EA', '#DC2626']
    
    for i, (layer, comps) in enumerate(components.items()):
        x_offset = 0
        for j, comp in enumerate(comps):
            width = 1
            ax.barh(i, width, left=x_offset, 
                   color=colors_cycle[j % len(colors_cycle)],
                   edgecolor='white', linewidth=2, height=0.6)
            ax.text(x_offset + width/2, i, comp, ha='center', va='center', 
                   fontsize=9, color='white', fontweight='bold')
            x_offset += width
    
    ax.set_yticks(y_positions)
    ax.set_yticklabels(layers, fontsize=11)
    ax.set_xlabel('Components', fontsize=12)
    ax.set_title('Mini-Agent System Layers Architecture', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 5)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'system_layers.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Generated system_layers.png")

def chart_4_dependency_matrix():
    """Heat map showing component dependencies"""
    components = ['Config', 'LLM\nClient', 'Skills', 'Tools', 'Utils', 'CLI']
    
    # Dependency matrix (1 = depends on)
    matrix = np.array([
        [0, 0, 0, 0, 0, 0],  # Config depends on nothing
        [1, 0, 0, 0, 1, 0],  # LLM Client depends on Config, Utils
        [1, 1, 0, 1, 1, 0],  # Skills depend on Config, LLM, Tools, Utils
        [1, 0, 0, 0, 1, 0],  # Tools depend on Config, Utils
        [1, 0, 0, 0, 0, 0],  # Utils depend on Config
        [1, 1, 1, 1, 1, 0],  # CLI depends on everything
    ])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = plt.cm.Blues
    
    im = ax.imshow(matrix, cmap=cmap, aspect='auto')
    
    ax.set_xticks(range(len(components)))
    ax.set_yticks(range(len(components)))
    ax.set_xticklabels(components, fontsize=10)
    ax.set_yticklabels(components, fontsize=10)
    
    ax.set_xlabel('Depends On →', fontsize=12)
    ax.set_ylabel('Component ↓', fontsize=12)
    ax.set_title('Component Dependency Matrix\n(Row depends on Column)', fontsize=14, fontweight='bold')
    
    # Add grid
    for i in range(len(components)):
        for j in range(len(components)):
            text = '●' if matrix[i, j] == 1 else ''
            ax.text(j, i, text, ha='center', va='center', fontsize=14,
                   color='white' if matrix[i, j] == 1 else 'gray')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'dependency_matrix.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Generated dependency_matrix.png")

def chart_5_directory_treemap():
    """Treemap-style visualization of directory structure"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Main sections with sizes (proportional to importance/file count)
    sections = [
        ('mini_agent/', 0, 0, 6, 5, COLORS['primary'], 'Core Package\n50+ modules'),
        ('scripts/', 6.2, 0, 4, 5, COLORS['secondary'], 'Scripts\n85+ files'),
        ('documents/', 0, 5.2, 5, 3, COLORS['accent'], 'Documentation\n100+ files'),
        ('vscode-ext/', 5.2, 5.2, 3, 3, COLORS['warning'], 'VS Code\nExtension'),
        ('tests/', 8.4, 5.2, 2, 3, COLORS['info'], 'Tests\n16 files'),
        ('examples/', 10.4, 0, 1.6, 3, '#9333EA', 'Examples'),
        ('workspace/', 10.4, 3.2, 1.6, 2, '#DC2626', 'Workspace'),
    ]
    
    for name, x, y, w, h, color, label in sections:
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                        facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
               fontsize=10, color='white', fontweight='bold')
    
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 8.7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Mini-Agent Directory Structure (Treemap View)', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'directory_treemap.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Generated directory_treemap.png")

def chart_6_llm_comparison():
    """Radar chart comparing LLM providers"""
    categories = ['Speed', 'Cost\nEfficiency', 'Quality', 'Web\nSearch', 'Quota']
    
    # Scores for each provider (1-5)
    providers = {
        'OpenAI GPT-4': [4, 2, 5, 3, 5],
        'MiniMax GLM': [5, 5, 4, 4, 4],
        'Z.AI Coding': [4, 4, 4, 5, 3]
    }
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    colors = [COLORS['primary'], COLORS['accent'], COLORS['warning']]
    
    for (name, values), color in zip(providers.items(), colors):
        values_closed = values + values[:1]
        ax.plot(angles, values_closed, 'o-', linewidth=2, label=name, color=color)
        ax.fill(angles, values_closed, alpha=0.25, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 5)
    ax.set_title('LLM Provider Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'llm_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Generated llm_comparison.png")

if __name__ == '__main__':
    print("\n🎨 Generating Python Chart Visualizations...\n")
    
    chart_1_skill_distribution()
    chart_2_codebase_metrics()
    chart_3_system_layers()
    chart_4_dependency_matrix()
    chart_5_directory_treemap()
    chart_6_llm_comparison()
    
    print(f"\n✅ All charts saved to: {OUTPUT_DIR}")
    print("\nGenerated files:")
    for f in OUTPUT_DIR.glob("*.png"):
        print(f"  • {f.name}")
