import requests
import json
import time
import os

# Disable proxies to avoid issues with localhost
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["no_proxy"] = "127.0.0.1,localhost"

def test_parser():
    url = "http://127.0.0.1:8000/parse"
    
    # Complex sentences to demonstrate discourse relations (Contrast, Cause, Condition, etc.)
    texts = [
        "Although it was raining heavily, we decided to go for a walk because we needed some fresh air.",
        "If the project is completed on time, we will receive a bonus; otherwise, we might face penalties.",
        "The market crashed yesterday. Consequently, many investors lost a significant amount of money.",
        "First, you need to mix the ingredients. Then, bake the cake for 45 minutes. Finally, let it cool down."
    ]

    print(f"Testing API at {url}...\n")

    for i, text in enumerate(texts, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input Text: {text}")
        
        payload = {"text": text}
        
        try:
            start_time = time.time()
            response = requests.post(url, json=payload)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"Status: Success ({duration:.2f}s)")
                print("Response Tree:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Status: Failed (Code {response.status_code})")
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the server. Make sure it is running on http://127.0.0.1:8000")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
        
        print("\n")

if __name__ == "__main__":
    test_parser()
