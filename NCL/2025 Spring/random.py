from collections import Counter
import re

def get_third_most_frequent_domain(log_file):
    # Dictionary to store domain counts
    domain_counts = Counter()
    
    # Regular expression to extract domain from URLs or CONNECT requests
    domain_pattern = re.compile(r'https?://([^/]+)/|CONNECT\s+([^\s:]+):')
    
    try:
        with open(log_file, 'r') as file:
            for line in file:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Extract domain using regex
                match = domain_pattern.search(line)
                if match:
                    # Domain is in group 1 (http) or group 2 (CONNECT)
                    domain = match.group(1) or match.group(2)
                    domain_counts[domain] += 1
    
        # Get list of (domain, count) tuples sorted by count (descending) and domain (alphabetically)
        sorted_domains = sorted(domain_counts.items(), key=lambda x: (-x[1], x[0]))
        
        # Handle edge cases
        if len(sorted_domains) < 3:
            return "Not enough domains in the log"
        
        # Find the third distinct count value
        counts = [count for _, count in sorted_domains]
        unique_counts = sorted(set(counts), reverse=True)
        
        if len(unique_counts) < 3:
            # If fewer than 3 unique counts, pick the domain at index 2 if available
            return sorted_domains[2][0] if len(sorted_domains) > 2 else sorted_domains[-1][0]
        
        # Get domains with the third highest count
        third_count = unique_counts[2]
        third_count_domains = [domain for domain, count in sorted_domains if count == third_count]
        
        # Return the first domain alphabetically among those with the third count
        return third_count_domains[0]
    
    except FileNotFoundError:
        return "Log file not found"
    except Exception as e:
        return f"Error processing log: {str(e)}"

# Example usage
log_file = "access.log"  # Replace with your log file path
result = get_third_most_frequent_domain(log_file)
print(f"Third most frequently accessed domain: {result}")