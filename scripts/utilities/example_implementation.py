#!/usr/bin/env python3
"""
Example Implementation: Data Processing Script

This is an example implementation that will be fact-checked and validated
using our self-assessment system.
"""

import json
import csv
from typing import List, Dict, Any
from datetime import datetime
import os

class DataProcessor:
    """Simple data processing class for demonstration"""
    
    def __init__(self, data_file: str = None):
        self.data_file = data_file
        self.processed_data = []
        
    def load_data(self) -> List[Dict[str, Any]]:
        """Load data from file or create sample data"""
        if self.data_file and os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        else:
            # Create sample data for demonstration
            return [
                {"name": "John Doe", "age": 30, "score": 85.5},
                {"name": "Jane Smith", "age": 25, "score": 92.0},
                {"name": "Bob Johnson", "age": 35, "score": 78.3}
            ]
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and enhance the data"""
        processed = []
        for item in data:
            # Add processed fields
            processed_item = item.copy()
            processed_item["processed_at"] = datetime.now().isoformat()
            processed_item["score_category"] = self._categorize_score(item.get("score", 0))
            processed.append(processed_item)
        return processed
    
    def _categorize_score(self, score: float) -> str:
        """Categorize score into grade levels"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        else:
            return "D"
    
    def save_results(self, data: List[Dict[str, Any]], output_file: str):
        """Save processed data to file"""
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_summary(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not data:
            return {"error": "No data to process"}
        
        scores = [item.get("score", 0) for item in data if "score" in item]
        ages = [item.get("age", 0) for item in data if "age" in item]
        
        return {
            "total_records": len(data),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "average_age": sum(ages) / len(ages) if ages else 0,
            "score_distribution": self._get_score_distribution(scores)
        }
    
    def _get_score_distribution(self, scores: List[float]) -> Dict[str, int]:
        """Get distribution of scores by category"""
        distribution = {"A": 0, "B": 0, "C": 0, "D": 0}
        for score in scores:
            category = self._categorize_score(score)
            distribution[category] += 1
        return distribution

def main():
    """Main function to demonstrate the data processor"""
    processor = DataProcessor()
    
    # Load and process data
    print("📊 Data Processing Example")
    print("=" * 40)
    
    raw_data = processor.load_data()
    print(f"Loaded {len(raw_data)} records")
    
    processed_data = processor.process_data(raw_data)
    print("Data processed successfully")
    
    # Generate and display summary
    summary = processor.generate_summary(processed_data)
    print(f"\nSummary:")
    print(f"- Total records: {summary['total_records']}")
    print(f"- Average score: {summary['average_score']:.1f}")
    print(f"- Score range: {summary['min_score']:.1f} - {summary['max_score']:.1f}")
    print(f"- Average age: {summary['average_age']:.1f}")
    print(f"- Score distribution: {summary['score_distribution']}")
    
    # Save results
    output_file = "processed_data.json"
    processor.save_results(processed_data, output_file)
    print(f"\nResults saved to: {output_file}")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Data processing completed successfully!")
    else:
        print("\n❌ Data processing failed!")