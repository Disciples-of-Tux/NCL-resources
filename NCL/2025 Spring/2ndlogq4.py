import re

def count_verified_users(file_path, max_verified_list=5):
    verified_count = 0
    verified_users = []
    match_count = 0
    
    # Regex: Capture email (1st value, quoted) and is_verified (6th value, true/false)
    pattern = r"values\s*\(\s*'([^']*)'\s*,\s*'[^']*'\s*,\s*\d+\s*,\s*\d+\s*,\s*'\d+'\s*,\s*(true|false)\s*,"
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip non-INSERT lines
                if not line.strip().startswith('insert into Hacked_data'):
                    continue
                
                # Extract email and is_verified
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    email = match.group(1)
                    is_verified = match.group(2).lower() == 'true'
                    match_count += 1
                    
                    if is_verified:
                        verified_count += 1
                        if len(verified_users) < max_verified_list:
                            verified_users.append(email)
        
        if match_count == 0:
            return f"No valid entries found in {match_count} matched lines.", 0, []
        
        # Format output
        result = f"Q4 - Number of verified users: {verified_count}\n"
        result += f"First {min(max_verified_list, len(verified_users))} verified users (by file order):\n"
        if verified_users:
            for i, email in enumerate(verified_users, 1):
                result += f"{i}. {email}\n"
        else:
            result += "None\n"
        result += f"Total matched lines: {match_count}"
        
        return result, verified_count, verified_users
    
    except FileNotFoundError:
        return "File not found. Please check the file path.", 0, []
    except Exception as e:
        return f"Error processing file: {e}", 0, []

# Example usage
file_path = 'social_data.sql'  # Replace with your file path
result, count, verified_list = count_verified_users(file_path)
print(result)