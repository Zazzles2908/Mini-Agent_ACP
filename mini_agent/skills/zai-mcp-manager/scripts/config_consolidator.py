#!/usr/bin/env python3
"""
Z.AI Configuration Consolidator
Removes redundant configuration files and creates unified setup
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ZAIConfigConsolidator:
    """Consolidate redundant Z.AI configuration files"""
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.backup_dir = self.workspace / "config_backup"
    
    def create_backup(self):
        """Create backup of existing configuration files"""
        self.backup_dir.mkdir(exist_ok=True)
        
        config_files = [
            ".mcp.json",
            "mini_agent/config/.mcp.json", 
            "mini_agent/config/z_mcp_servers.json"
        ]
        
        backed_up = []
        for config_file in config_files:
            source_path = self.workspace / config_file
            if source_path.exists():
                backup_path = self.backup_dir / f"{Path(config_file).name}.backup"
                backup_path.write_text(source_path.read_text())
                backed_up.append(config_file)
        
        print(f"[CHECK] Created backups in {self.backup_dir}: {backed_up}")
        return backed_up
    
    def consolidate_configurations(self):
        """Consolidate configuration files into optimal structure"""
        
        # Read existing configurations
        configs = {}
        
        # Main MCP config
        main_config_path = self.workspace / ".mcp.json"
        if main_config_path.exists():
            configs['main'] = json.loads(main_config_path.read_text())
        
        # Mini-Agent config  
        ma_config_path = self.workspace / "mini_agent/config/.mcp.json"
        if ma_config_path.exists():
            configs['mini_agent'] = json.loads(ma_config_path.read_text())
        
        # Z.AI specific config
        zai_config_path = self.workspace / "mini_agent/config/z_mcp_servers.json"
        if zai_config_path.exists():
            configs['zai'] = json.loads(zai_config_path.read_text())
        
        # Create consolidated configuration
        consolidated_config = self._merge_configurations(configs)
        
        # Write consolidated config
        consolidated_path = self.workspace / "zai_mcp_consolidated.json"
        with open(consolidated_path, 'w') as f:
            json.dump(consolidated_config, f, indent=2)
        
        print(f"[CHECK] Created consolidated config: {consolidated_path}")
        return consolidated_path, consolidated_config
    
    def _merge_configurations(self, configs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple configuration files into optimal structure"""
        
        # Start with main configuration structure
        merged = {
            "mcpServers": {},
            "monitoring": {
                "enabled": True,
                "health_check_interval": 300,
                "quota_check_interval": 3600
            },
            "security": {
                "enable_api_key_validation": True,
                "require_https": True
            }
        }
        
        # Merge MCP servers from all configs
        for config_name, config_data in configs.items():
            servers = config_data.get("mcpServers", {})
            for server_name, server_config in servers.items():
                # Merge server configuration
                if server_name not in merged["mcpServers"]:
                    merged["mcpServers"][server_name] = {}
                
                merged["mcpServers"][server_name].update(server_config)
        
        # Ensure Z.AI MCP servers are present
        zai_servers = {
            "zai-web-search": {
                "command": "remote",
                "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
                "headers": {
                    "Authorization": "Bearer ${ZAI_API_KEY}",
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                },
                "timeout": 30,
                "retry": {
                    "max_retries": 3,
                    "initial_delay": 1.0
                }
            },
            "zai-web-reader": {
                "command": "remote",
                "url": "https://api.z.ai/api/mcp/web_reader/mcp",
                "headers": {
                    "Authorization": "Bearer ${ZAI_API_KEY}",
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                },
                "timeout": 45,
                "retry": {
                    "max_retries": 3,
                    "initial_delay": 1.0
                }
            }
        }
        
        # Add Z.AI servers if not already present
        for server_name, server_config in zai_servers.items():
            if server_name not in merged["mcpServers"]:
                merged["mcpServers"][server_name] = server_config
        
        # Add optimization settings
        merged["optimization"] = {
            "enable_caching": True,
            "cache_ttl": 300,
            "batch_operations": True
        }
        
        return merged
    
    def create_optimal_config_file(self):
        """Create the optimal .mcp.json file"""
        _, consolidated_config = self.consolidate_configurations()
        
        # Create simplified .mcp.json for Mini-Agent
        optimal_config = {
            "mcpServers": {}
        }
        
        # Only include essential MCP servers for Mini-Agent
        for server_name, server_config in consolidated_config["mcpServers"].items():
            if "zai" in server_name.lower():
                optimal_config["mcpServers"][server_name] = {
                    "command": server_config["command"],
                    "url": server_config["url"],
                    "headers": server_config["headers"],
                    "timeout": server_config["timeout"]
                }
        
        # Write optimal config
        optimal_path = self.workspace / ".mcp.json"
        with open(optimal_path, 'w') as f:
            json.dump(optimal_config, f, indent=2)
        
        print(f"[CHECK] Created optimal .mcp.json: {optimal_path}")
        return optimal_path
    
    def cleanup_redundant_files(self, backed_up_files):
        """Clean up redundant configuration files"""
        
        redundant_files = [
            "mini_agent/config/.mcp.json",
            "mini_agent/config/z_mcp_servers.json"
        ]
        
        removed_files = []
        for file_path in redundant_files:
            full_path = self.workspace / file_path
            if full_path.exists():
                full_path.unlink()
                removed_files.append(file_path)
        
        print(f"[CHECK] Removed redundant files: {removed_files}")
        return removed_files
    
    def generate_consolidation_report(self):
        """Generate a report of the consolidation process"""
        
        config_files = ['.mcp.json', 'mini_agent/config/.mcp.json', 'mini_agent/config/z_mcp_servers.json']
        existing_configs = len([f for f in config_files if (self.workspace / f).exists()])
        
        report = f"""# Z.AI Configuration Consolidation Report

## Summary
Consolidated {existing_configs} configuration files into optimal structure.

## Changes Made
1. [CHECK] Created consolidated configuration: `zai_mcp_consolidated.json`
2. [CHECK] Updated `.mcp.json` with optimal settings
3. [CHECK] Removed redundant configuration files
4. [CHECK] Created backup of original files

## Benefits
- **Reduced Complexity**: Single source of truth for configuration
- **Easier Maintenance**: No need to update multiple files
- **Better Organization**: Logical configuration structure
- **Improved Performance**: Optimized MCP server settings

## Next Steps
1. Update any references to old config files
2. Test the new configuration with monitoring scripts
3. Remove backup directory after verification

## Backup Location
Original files backed up to: `{self.backup_dir}`
"""

        report_path = self.workspace / "config_consolidation_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[CHECK] Generated consolidation report: {report_path}")
        return report_path


def main():
    """Main consolidation process"""
    consolidator = ZAIConfigConsolidator()
    
    print("[TOOL] Starting Z.AI configuration consolidation...")
    print("=" * 50)
    
    # Step 1: Create backups
    print("\n[BOX] Step 1: Creating backups...")
    backed_up = consolidator.create_backup()
    
    # Step 2: Consolidate configurations
    print("\n[LINK] Step 2: Consolidating configurations...")
    consolidated_path, consolidated_config = consolidator.consolidate_configurations()
    
    # Step 3: Create optimal config file
    print("\n[LIGHTNING] Step 3: Creating optimal configuration...")
    optimal_path = consolidator.create_optimal_config_file()
    
    # Step 4: Clean up redundant files
    print("\n[BROOM] Step 4: Cleaning up redundant files...")
    removed = consolidator.cleanup_redundant_files(backed_up)
    
    # Step 5: Generate report
    print("\n[DOCUMENT] Step 5: Generating consolidation report...")
    report_path = consolidator.generate_consolidation_report()
    
    print("\n" + "=" * 50)
    print("[CHECK] Configuration consolidation completed successfully!")
    print(f"[FOLDER] Backup location: {consolidator.backup_dir}")
    print(f"[DOCUMENT] Report: {report_path}")
    print("\n[TARGET] Next: Test with monitoring scripts:")
    print("   python mini_agent/skills/zai-mcp-manager/scripts/config_validator.py")


if __name__ == "__main__":
    main()
