import json
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    
    if parsed_url.netloc in {"youtu.be"}:  # Shortened URL
        return parsed_url.path.lstrip("/")
    elif parsed_url.netloc in {"www.youtube.com", "youtube.com", "m.youtube.com"}:
        # Extract v= query parameter
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    return None  # No recognizable video ID

def remove_duplicates(input_file, output_file):
    """Remove duplicate YouTube links based on video IDs."""
    with open(input_file, 'r') as file:
        urls = json.load(file)
    
    seen_ids = set()
    unique_urls = []

    for url in urls:
        video_id = extract_video_id(url)
        if video_id and video_id not in seen_ids:
            seen_ids.add(video_id)
            unique_urls.append(url)
    
    # Save the cleaned list back to the file
    with open(output_file, 'w') as file:
        json.dump(unique_urls, file, indent=4)

    print(f"Processed {len(urls)} URLs, {len(unique_urls)} unique URLs saved to {output_file}.")

# Usage
remove_duplicates("videos.json", "cleaned_videos.json")
