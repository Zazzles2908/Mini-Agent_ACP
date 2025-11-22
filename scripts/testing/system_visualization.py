#!/usr/bin/env python3
"""
Mini-Agent System Architecture Visualization
Creates comprehensive network and flow diagrams for the Mini-Agent system
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.patches import FancyBboxPatch

def create_network_visualization():
    """Create skills network and system architecture visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12))
    fig.suptitle('Mini-Agent System Architecture Visualization', fontsize=24, fontweight='bold')

    # === LEFT PANEL: Skills Network ===
    G = nx.Graph()

    # Define nodes with categories and properties
    skills_data = {
        # Document Skills
        'DOCX': {'category': 'document', 'pos': (0, 3)},
        'PDF': {'category': 'document', 'pos': (1, 3)},
        'PPTX': {'category': 'document', 'pos': (2, 3)},
        'XLSX': {'category': 'document', 'pos': (3, 3)},
        
        # Creative Skills
        'Canvas Design': {'category': 'creative', 'pos': (0, 1)},
        'Algorithmic Art': {'category': 'creative', 'pos': (1, 1)},
        
        # Quality Skills
        'Fact Check': {'category': 'quality', 'pos': (0, -1)},
        'Self Assessment': {'category': 'quality', 'pos': (1, -1)},
        
        # Development Skills
        'MCP Builder': {'category': 'development', 'pos': (3, 1)},
        'Skill Creator': {'category': 'development', 'pos': (4, 1)},
        
        # Integration Skills
        'VS Code': {'category': 'integration', 'pos': (2, -1)},
        'Theme Factory': {'category': 'integration', 'pos': (3, -1)},
        'Brand Guide': {'category': 'integration', 'pos': (4, -1)},
        
        # Utility Skills
        'Slack GIF': {'category': 'utility', 'pos': (5, 1)},
        'Template Skill': {'category': 'utility', 'pos': (5, 0)},
        'WebApp Testing': {'category': 'utility', 'pos': (5, -1)},
        
        # Core System
        'Core Framework': {'category': 'core', 'pos': (2, 0)}
    }

    # Add nodes to graph
    for skill, data in skills_data.items():
        G.add_node(skill, **data)

    # Define connections (edges)
    connections = [
        ('DOCX', 'Canvas Design'), ('PDF', 'Algorithmic Art'), ('PPTX', 'Canvas Design'),
        ('XLSX', 'Fact Check'), ('Canvas Design', 'Theme Factory'), ('Canvas Design', 'Brand Guide'),
        ('Algorithmic Art', 'Theme Factory'), ('Fact Check', 'Self Assessment'),
        ('MCP Builder', 'VS Code'), ('Skill Creator', 'VS Code'), ('Template Skill', 'Theme Factory'),
        ('Core Framework', 'DOCX'), ('Core Framework', 'Canvas Design'), ('Core Framework', 'MCP Builder'),
        ('Core Framework', 'Fact Check'), ('Core Framework', 'VS Code'), ('Core Framework', 'Slack GIF'),
        ('WebApp Testing', 'VS Code'), ('Theme Factory', 'Brand Guide')
    ]

    G.add_edges_from(connections)

    # Position nodes using the predefined positions
    pos = {skill: data['pos'] for skill, data in skills_data.items()}

    # Color map for categories
    category_colors = {
        'document': '#FF6B6B',    # Red
        'creative': '#4ECDC4',    # Teal
        'quality': '#45B7D1',     # Blue
        'development': '#96CEB4', # Green
        'integration': '#FFEAA7', # Yellow
        'utility': '#DDA0DD',     # Plum
        'core': '#FFB347'         # Orange
    }

    # Draw left network
    node_colors = [category_colors[G.nodes[node]['category']] for node in G.nodes()]
    node_sizes = [3000 if G.nodes[node]['category'] == 'core' else 1500 for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8, ax=ax1)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.6, width=2, ax=ax1)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=ax1)

    ax1.set_title('Skills Network Interconnection Map', fontsize=16, fontweight='bold')
    ax1.text(-1, -2, 'Red: Document | Teal: Creative | Blue: Quality\nGreen: Development | Yellow: Integration | Plum: Utility', 
             fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray'))
    ax1.set_xlim(-1, 6)
    ax1.set_ylim(-2, 4)
    ax1.axis('off')

    # === RIGHT PANEL: System Architecture Layers ===
    ax2.set_title('System Architecture Layers', fontsize=16, fontweight='bold')

    # Create layered visualization
    layers = [
        {'name': 'USER INTERFACE', 'y': 4, 'color': '#E3F2FD', 'components': ['CLI', 'Web Interface', 'API']},
        {'name': 'SKILL ROUTER', 'y': 3, 'color': '#F3E5F5', 'components': ['Document Skills', 'Creative Skills', 'Dev Tools']},
        {'name': 'CORE FRAMEWORK', 'y': 2, 'color': '#E8F5E8', 'components': ['ACP', 'LLM', 'Tools', 'Utils']},
        {'name': 'INTEGRATION LAYER', 'y': 1, 'color': '#FFF3E0', 'components': ['OpenAI', 'Z.AI', 'VS Code']},
        {'name': 'INFRASTRUCTURE', 'y': 0, 'color': '#FFECB3', 'components': ['Python', 'Configuration', 'Scripts']}
    ]

    # Draw layers
    for i, layer in enumerate(layers):
        # Main layer box
        rect = FancyBboxPatch((0, layer['y']-0.3), 10, 0.6, 
                             boxstyle='round,pad=0.05', 
                             facecolor=layer['color'], 
                             edgecolor='black', 
                             linewidth=1.5)
        ax2.add_patch(rect)
        
        # Layer name
        ax2.text(5, layer['y'], layer['name'], ha='center', va='center', 
                fontsize=12, fontweight='bold')
        
        # Components
        comp_width = 10 / len(layer['components'])
        for j, comp in enumerate(layer['components']):
            comp_x = (j + 0.5) * comp_width
            ax2.text(comp_x, layer['y']-0.15, comp, ha='center', va='center', 
                    fontsize=8, bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    # Add flow arrows
    for i in range(len(layers)-1):
        ax2.arrow(5, layers[i]['y']-0.4, 0, -0.2, head_width=0.3, head_length=0.05, 
                 fc='black', ec='black')

    ax2.set_xlim(-0.5, 10.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.axis('off')

    # Add legend for right panel
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, facecolor='#E3F2FD', edgecolor='black', label='User Interaction'),
        plt.Rectangle((0, 0), 1, 1, facecolor='#F3E5F5', edgecolor='black', label='Skill Processing'),
        plt.Rectangle((0, 0), 1, 1, facecolor='#E8F5E8', edgecolor='black', label='Core Logic'),
        plt.Rectangle((0, 0), 1, 1, facecolor='#FFF3E0', edgecolor='black', label='External APIs'),
        plt.Rectangle((0, 0), 1, 1, facecolor='#FFECB3', edgecolor='black', label='System Base')
    ]
    ax2.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.savefig('PYTHON_NETWORK_VISUALIZATION.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_data_flow_visualization():
    """Create data flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.suptitle('Mini-Agent Data Flow Architecture', fontsize=20, fontweight='bold')

    # Create flow diagram
    flow_components = {
        'input': {'pos': (1, 8), 'color': '#FFE0B2', 'size': (1.5, 1)},
        'router': {'pos': (3, 8), 'color': '#F3E5F5', 'size': (2, 1)},
        'skills': {'pos': (6, 8), 'color': '#E8F5E8', 'size': (3, 1)},
        'tools': {'pos': (10, 8), 'color': '#E3F2FD', 'size': (2, 1)},
        'output': {'pos': (13, 8), 'color': '#FFF3E0', 'size': (1.5, 1)},
        
        'docs': {'pos': (3, 5), 'color': '#FFCDD2', 'size': (2, 0.8)},
        'creative': {'pos': (6, 5), 'color': '#C8E6C9', 'size': (2, 0.8)},
        'quality': {'pos': (9, 5), 'color': '#BBDEFB', 'size': (2, 0.8)},
        'dev': {'pos': (12, 5), 'color': '#FFF9C4', 'size': (2, 0.8)},
        
        'config': {'pos': (1, 2), 'color': '#F8BBD9', 'size': (2, 0.8)},
        'schema': {'pos': (4, 2), 'color': '#C5CAE9', 'size': (2, 0.8)},
        'utils': {'pos': (7, 2), 'color': '#DCEDC8', 'size': (2, 0.8)},
        'acp': {'pos': (10, 2), 'color': '#FFE0B2', 'size': (2, 0.8)},
        'llm': {'pos': (13, 2), 'color': '#E1BEE7', 'size': (2, 0.8)},
    }

    # Draw flow components
    for comp_name, comp_data in flow_components.items():
        rect = FancyBboxPatch(
            (comp_data['pos'][0] - comp_data['size'][0]/2, comp_data['pos'][1] - comp_data['size'][1]/2),
            comp_data['size'][0], comp_data['size'][1],
            boxstyle='round,pad=0.1',
            facecolor=comp_data['color'],
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Add text
        ax.text(comp_data['pos'][0], comp_data['pos'][1], comp_name.upper(), 
               ha='center', va='center', fontweight='bold', fontsize=10)

    # Draw flow arrows
    flow_arrows = [
        ((1.75, 8), (2.25, 8)),      # input -> router
        ((4, 8), (5, 8)),           # router -> skills
        ((8.5, 8), (9.5, 8)),       # skills -> tools
        ((11, 8), (12.25, 8)),      # tools -> output
        
        ((3, 7.5), (3, 5.4)),       # router -> docs
        ((3, 7.5), (6, 5.4)),       # router -> creative
        ((3, 7.5), (9, 5.4)),       # router -> quality
        ((3, 7.5), (12, 5.4)),      # router -> dev
        
        ((3, 4.5), (1, 2.4)),       # docs -> config
        ((3, 4.5), (4, 2.4)),       # docs -> schema
        ((6, 4.5), (7, 2.4)),       # creative -> utils
        ((9, 4.5), (10, 2.4)),      # quality -> acp
        ((12, 4.5), (13, 2.4)),     # dev -> llm
        
        ((5, 2), (8, 8)),           # utils -> skills
        ((8, 2), (8, 8)),           # acp -> skills
        ((11, 2), (8, 8)),          # llm -> skills
    ]

    for start, end in flow_arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='#666666'))

    ax.set_xlim(0, 14)
    ax.set_ylim(1, 9)
    ax.axis('off')

    # Add title labels
    ax.text(7, 9.2, 'PRIMARY DATA FLOW', ha='center', fontsize=14, fontweight='bold')
    ax.text(7, 6.2, 'SKILL ROUTING', ha='center', fontsize=14, fontweight='bold')
    ax.text(7, 3.2, 'CORE COMPONENTS', ha='center', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('PYTHON_DATA_FLOW_VISUALIZATION.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("🎨 Creating Mini-Agent system visualizations...")
    create_network_visualization()
    create_data_flow_visualization()
    print("✅ Python visualizations created successfully!")
    print("📁 Files saved:")
    print("   - documents/VISUALS/PYTHON_NETWORK_VISUALIZATION.png")
    print("   - documents/VISUALS/PYTHON_DATA_FLOW_VISUALIZATION.png")