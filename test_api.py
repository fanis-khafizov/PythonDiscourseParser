import json
import urllib.request
import urllib.error
import sys

API_URL = "http://localhost:8000/parse"

TEST_CASES = [
    # 1. Simple single sentence (might be flat or have internal structure depending on parser)
    "The quick brown fox jumps over the lazy dog.",
    
    # 2. Elaboration / Background
    "On Saturday, Team India won against South Africa. The match was played in Barbados.",
    
    # 3. Contrast
    "Although it was raining, we decided to go for a hike.",
    
    # 4. Sequence
    "First, break the eggs. Then, whisk them vigorously. Finally, pour them into the hot pan.",
    
    # 5. Attribution (if supported)
    "The president stated that the economy is recovering."
]

def print_tree(node, indent=0):
    """Recursively prints the RST tree in a readable format."""
    prefix = "  " * indent
    # Relation and Nuclearity
    info = f"[{node.get('relation', 'span')}] ({node.get('nuclearity', 'flat')})"
    
    # Text content (EDU)
    text = node.get('text')
    if text:
        # Truncate long text for display
        display_text = (text[:60] + '...') if len(text) > 60 else text
        print(f"{prefix}{info} -> \"{display_text}\"")
    else:
        print(f"{prefix}{info}")
        for child in node.get('children', []):
            print_tree(child, indent + 1)

def run_tests():
    print(f"Targeting API: {API_URL}")
    print("Ensure the server is running with: python main.py\n")
    
    for i, text in enumerate(TEST_CASES, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input Text: {text.strip()}")
        
        payload = json.dumps({"text": text}).encode('utf-8')
        req = urllib.request.Request(
            API_URL, 
            data=payload, 
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    print(f"Error: Server returned status {response.status}")
                    continue
                    
                body = response.read().decode('utf-8')
                data = json.loads(body)
                
                print("\nParsed RST Tree:")
                if 'tree' in data:
                    print_tree(data['tree'])
                else:
                    print("No tree data received.")
                    
        except urllib.error.URLError as e:
            print(f"\nConnection Error: {e}")
            print("Is the server running?")
            sys.exit(1)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    run_tests()
