import re

def find_top_10_lowest_timestamps(file_path):
    timestamps = []
    match_count = 0
    
    # Regex: Capture join_date (5th value) as digits, quoted or not
    # Matches: ...values(..., ..., 799, 204, '1742814687000', ... or unquoted
    pattern = r"values\s*\(\s*'[^']*'\s*,\s*'[^']*'\s*,\s*\d+\s*,\s*\d+\s*,\s*(?:'?)(\d+)(?:'?),"
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip non-INSERT lines
                if not line.strip().startswith('insert into Hacked_data'):
                    continue
                
                # Extract join_date
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    try:
                        timestamp = int(match.group(1))
                        # Basic validation: timestamp should be in a reasonable range (e.g., post-2000)
                        if timestamp > 946684800000:  # After Jan 1, 2000 in ms
                            timestamps.append(timestamp)
                            match_count += 1
                    except ValueError:
                        continue
        
        if not timestamps:
            return f"No valid timestamps found in {match_count} matched lines.", []
        
        # Sort and get top 10 lowest
        timestamps.sort()
        top_10 = timestamps[:10]
        
        return f"Top 10 lowest Unix timestamps (milliseconds):\n" + \
               "\n".join(str(ts) for ts in top_10) + \
               f"\nTotal matched lines: {match_count}", top_10
    
    except FileNotFoundError:
        return "File not found. Please check the file path.", []
    except Exception as e:
        return f"Error processing file: {e}", []

# Example usage
file_path = 'social_data.sql'  # Replace with your file path
result, timestamps = find_top_10_lowest_timestamps(file_path)
print(result)