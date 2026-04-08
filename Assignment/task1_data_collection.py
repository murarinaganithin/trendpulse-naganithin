import requests
import time
import json
import os
from datetime import datetime

def main():
    # Identify our script so HackerNews doesn't block the request
    headers = {"User-Agent": "TrendPulse/1.0"}
    
    # Topics we want to find, and the keywords to trigger them
    categories = {
        "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
        "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
        "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
        "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
        "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
    }

    print("Fetching top 500 story IDs...")
    try:
        # Get the current trending list (returns just a list of IDs)
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", headers=headers)
        top_story_ids = response.json()[:500] # slice to get only the first 500
        print(f"Successfully fetched {len(top_story_ids)} story IDs.")
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        top_story_ids = []

    collected_stories = []
    
    # Dictionary to store stories we've already downloaded. 
    # This prevents us from fetching the exact same URL 5 times across the 5 category loops.
    story_cache = {}

    for category_name, keywords in categories.items():
        print(f"\n--- Searching for {category_name} stories ---")
        category_count = 0
        
        for story_id in top_story_ids:
            # Stop if we hit the 25-story limit for this specific category
            if category_count >= 25:
                break
                
            # If we haven't seen this story yet, fetch it from the API
            if story_id not in story_cache:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_resp = requests.get(story_url, headers=headers)
                    story_cache[story_id] = story_resp.json()
                except Exception as e:
                    print(f"Error fetching story {story_id}: {e}")
                    continue
            
            # Load from cache
            story = story_cache[story_id]
            
            # Safety check: skip if the API returned null or a deleted post with no title
            if not story or "title" not in story:
                continue
                
            # Convert to lowercase for case-insensitive matching
            title_lower = story["title"].lower()
            
            # If any keyword exists in the title, we have a match
            if any(keyword in title_lower for keyword in keywords):
                story_data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category_name,
                    # Use .get() with a default of 0/Unknown in case the field is missing
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "Unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                collected_stories.append(story_data)
                category_count += 1
                
                print(f"Found {category_name} story ({category_count}/25): {story.get('title')}")
                
        print(f"Finished {category_name}. Waiting 2 seconds before next category...")
        # Rate limiting: wait 2 seconds between category loops as per requirements
        time.sleep(2) 

    print("\nSaving data...")
    # Create the data folder if it doesn't exist yet
    os.makedirs("data", exist_ok=True)
    
    # Format today's date like 20240115 for the filename
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"

    # Dump the list of dictionaries into a JSON file, indented nicely
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"Collected {len(collected_stories)} stories. Saved to {filename}")

if __name__ == "__main__":
    main()