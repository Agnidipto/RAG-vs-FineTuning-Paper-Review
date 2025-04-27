import json
import os

def verify_json_files(directory, file_pattern="mmlu_*.json"):
    """Verify integrity of MMLU JSON files"""
    import glob
    
    files = glob.glob(os.path.join(directory, file_pattern))
    results = {}
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            record_count = len(data) if isinstance(data, list) else 1
            results[file_path] = {"valid": True, "records": record_count}
            
        except json.JSONDecodeError:
            results[file_path] = {"valid": False, "error": "Invalid JSON"}
        except Exception as e:
            results[file_path] = {"valid": False, "error": str(e)}
    
    return results

# Example usage
if __name__ == "__main__":
  results = verify_json_files("./mmlu_datasets")
  
  for file, status in results.items():
    print(f"{os.path.basename(file)}: {'✓' if status['valid'] else '✗'} ({status.get('records', 0)} records)")