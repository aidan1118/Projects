#!/usr/bin/env python3

import json
import csv

def convert_json_to_csv():
    """Convert JSON to CSV without pandas/excel dependencies"""
    
    try:
        # Read the JSON file
        with open('team_performance.json', 'r') as f:
            data = json.load(f)
        
        # Extract the data array
        if 'data' in data and len(data['data']) > 0:
            records = data['data']
            
            # Get all field names from first record
            fieldnames = list(records[0].keys())
            
            # Write to CSV
            with open('nfl_team_performance.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            
            print(f"✅ Converted {len(records)} records")
            print(f"📄 Created: nfl_team_performance.csv")
            print(f"\n🎯 Power BI Steps:")
            print(f"1. Get Data → Text/CSV")
            print(f"2. Select: nfl_team_performance.csv")
            print(f"3. Import and create visualizations!")
            
            print(f"\n📊 Fields available:")
            for field in fieldnames:
                print(f"   • {field}")
                
        else:
            print("❌ No data found in JSON file")
            
    except FileNotFoundError:
        print("❌ team_performance.json not found")
        print("💡 Run: curl -s 'http://localhost:5001/nfl/team-performance?year=2024' > team_performance.json")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    convert_json_to_csv()