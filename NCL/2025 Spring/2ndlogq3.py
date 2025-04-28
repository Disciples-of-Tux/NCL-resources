import re

def find_top_followers(file_path, top_n=5):
    accounts = []
    match_count = 0
    
    # Regex: Capture email (1st value, quoted) and followers_count (3rd value, number)
    pattern = r"values\s*\(\s*'([^']*)'\s*,\s*'[^']*'\s*,\s*(\d+)\s*,"
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip non-INSERT lines
                if not line.strip().startswith('insert into Hacked_data'):
                    continue
                
                # Extract email and followers_count
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    try:
                        email = match.group(1)
                        followers = int(match.group(2))
                        accounts.append((email, followers))
                        match_count += 1
                    except ValueError:
                        continue
        
        if not accounts:
            return f"No valid accounts found in {match_count} matched lines.", None, []
        
        # Sort by followers_count (descending)
        accounts.sort(key=lambda x: x[1], reverse=True)
        
        # Get top email (Q3)
        top_email = accounts[0][0]
        
        # Get top N (default 5)
        top_accounts = accounts[:top_n]
        
        # Format output
        result = f"Q3 - Email with most followers: {top_email} (Followers: {accounts[0][1]})\n"
        result += f"Top {top_n} accounts by followers:\n"
        for i, (email, followers) in enumerate(top_accounts, 1):
            result += f"{i}. {email}: {followers}\n"
        result += f"Total matched lines: {match_count}"
        
        return result, top_email, top_accounts
    
    except FileNotFoundError:
        return "File not found. Please check the file path.", None, []
    except Exception as e:
        return f"Error processing file: {e}", None, []

# Example usage
file_path = 'social_data.sql'  # Replace with your file path
result, top_email, top_accounts = find_top_followers(file_path)
print(result)