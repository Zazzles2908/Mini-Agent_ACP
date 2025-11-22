#!/usr/bin/env python3
"""
Z.AI Quota Tracker
=================
Tracks and monitors Z.AI Lite Plan quota usage.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any

class ZAIQuotaTracker:
    def __init__(self, data_file: str = "scripts/utilities/zai_quota_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
        
    def _load_data(self) -> Dict[str, Any]:
        """Load quota data from file"""
        try:
            if Path(self.data_file).exists():
                with open(self.data_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        # Initialize with fresh data
        return {
            'search_usage': 0,
            'reader_usage': 0,
            'last_reset': datetime.now().isoformat(),
            'usage_history': [],
            'alerts_sent': []
        }
    
    def _save_data(self):
        """Save quota data to file"""
        try:
            Path(self.data_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save quota data: {e}")
    
    def track_search_usage(self, count: int = 1):
        """Track search quota usage"""
        self.data['search_usage'] += count
        self._log_usage('search', count)
        self._check_alerts()
        self._save_data()
        
        print(f"📊 Search quota used: {self.data['search_usage']}/100")
    
    def track_reader_usage(self, count: int = 1):
        """Track reader quota usage"""
        self.data['reader_usage'] += count
        self._log_usage('reader', count)
        self._check_alerts()
        self._save_data()
        
        print(f"📊 Reader quota used: {self.data['reader_usage']}/100")
    
    def _log_usage(self, usage_type: str, count: int):
        """Log usage to history"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': usage_type,
            'count': count,
            'cumulative_search': self.data['search_usage'],
            'cumulative_reader': self.data['reader_usage']
        }
        self.data['usage_history'].append(log_entry)
        
        # Keep only last 100 entries
        if len(self.data['usage_history']) > 100:
            self.data['usage_history'] = self.data['usage_history'][-100:]
    
    def _check_alerts(self):
        """Check for quota usage alerts"""
        alerts = []
        
        # Check search quota
        search_pct = (self.data['search_usage'] / 100) * 100
        if search_pct >= 80 and search_pct not in self.data['alerts_sent']:
            alerts.append(f"Search quota at {search_pct:.1f}% (80+/100)")
        
        if search_pct >= 95:
            alerts.append(f"Search quota nearly exhausted! ({search_pct:.1f}%)")
        
        # Check reader quota
        reader_pct = (self.data['reader_usage'] / 100) * 100
        if reader_pct >= 80 and reader_pct not in self.data['alerts_sent']:
            alerts.append(f"Reader quota at {reader_pct:.1f}% (80+/100)")
        
        if reader_pct >= 95:
            alerts.append(f"Reader quota nearly exhausted! ({reader_pct:.1f}%)")
        
        # Send alerts
        for alert in alerts:
            self._send_alert(alert)
            self.data['alerts_sent'].append(alert)
    
    def _send_alert(self, message: str):
        """Send quota alert"""
        print(f"🚨 Z.AI QUOTA ALERT: {message}")
        
        # Create alert log
        alert_file = Path("scripts/utilities/zai_quota_alerts.log")
        with open(alert_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current quota status"""
        search_pct = (self.data['search_usage'] / 100) * 100
        reader_pct = (self.data['reader_usage'] / 100) * 100
        
        status = {
            'search': {
                'used': self.data['search_usage'],
                'remaining': 100 - self.data['search_usage'],
                'percentage': search_pct,
                'status': 'ok' if search_pct < 80 else 'warning' if search_pct < 95 else 'critical'
            },
            'reader': {
                'used': self.data['reader_usage'],
                'remaining': 100 - self.data['reader_usage'],
                'percentage': reader_pct,
                'status': 'ok' if reader_pct < 80 else 'warning' if reader_pct < 95 else 'critical'
            },
            'last_reset': self.data['last_reset'],
            'total_usage': self.data['search_usage'] + self.data['reader_usage']
        }
        
        return status
    
    def reset_quota(self):
        """Reset quota counters (for new cycle)"""
        self.data['search_usage'] = 0
        self.data['reader_usage'] = 0
        self.data['last_reset'] = datetime.now().isoformat()
        self.data['alerts_sent'] = []
        self._save_data()
        
        print("✅ Z.AI quota counters reset")

# Usage monitoring integration
class ZAIUsageMonitor:
    def __init__(self):
        self.tracker = ZAIQuotaTracker()
    
    def monitor_search_start(self, query: str):
        """Monitor search operation start"""
        status = self.tracker.get_status()
        if status['search']['remaining'] <= 0:
            print("🚨 Search quota exhausted! Consider switching to external API.")
            return False
        return True
    
    def monitor_search_complete(self, success: bool):
        """Monitor search operation completion"""
        if success:
            self.tracker.track_search_usage(1)
        return True
    
    def monitor_reader_start(self, url: str):
        """Monitor reader operation start"""
        status = self.tracker.get_status()
        if status['reader']['remaining'] <= 0:
            print("🚨 Reader quota exhausted! Consider switching to external API.")
            return False
        return True
    
    def monitor_reader_complete(self, success: bool):
        """Monitor reader operation completion"""
        if success:
            self.tracker.track_reader_usage(1)
        return True
    
    def get_usage_report(self) -> str:
        """Get formatted usage report"""
        status = self.tracker.get_status()
        
        report = f"""
Z.AI QUOTA USAGE REPORT
========================
Search Quota: {status['search']['used']}/100 ({status['search']['percentage']:.1f}%)
Reader Quota: {status['reader']['used']}/100 ({status['reader']['percentage']:.1f}%)
Total Usage: {status['total_usage']}/200 ({(status['total_usage']/200)*100:.1f}%)
Last Reset: {status['last_reset']}

Status: {status['search']['status'].upper()} (Search), {status['reader']['status'].upper()} (Reader)
"""
        return report

# Example usage
def main():
    monitor = ZAIUsageMonitor()
    print(monitor.get_usage_report())

if __name__ == "__main__":
    main()
