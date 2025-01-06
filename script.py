import os
import json
from datetime import datetime, timezone
import pytz

# Define the current directory
photo_dir = os.getcwd()  

est = pytz.timezone("America/New_York")  # Correct timezone for Eastern Time

for filename in os.listdir(photo_dir):
    if filename.endswith(".json"):  # Process only .json files
        json_path = os.path.join(photo_dir, filename)
        
        with open(json_path, "r") as f:
            metadata = json.load(f)
        
        # Extract the 'photoTakenTime' timestamp
        photo_time = metadata.get("photoTakenTime", {}).get("timestamp")
        if not photo_time:
            print(f"No photoTakenTime found in {filename}")
            continue
        
        # Convert the timestamp to EST
        utc_time = datetime.fromtimestamp(int(photo_time), tz=timezone.utc)  # Use timezone.utc here
        est_time = utc_time.astimezone(est)
        formatted_date = est_time.strftime("%Y%m%d_%H%M%S")
        
        # Get the original file name from the 'title' field
        original_title = metadata.get("title", "")
        if not original_title:
            print(f"No title found in {filename}")
            continue
        
        # Find the corresponding media file
        media_path = os.path.join(photo_dir, original_title)
        if not os.path.exists(media_path):
            print(f"No media file found for {original_title}")
            continue
        
        # Create the new file name
        file_extension = os.path.splitext(original_title)[1]
        new_name = f"{formatted_date}{file_extension}"
        new_path = os.path.join(photo_dir, new_name)
        
        # Rename the file
        os.rename(media_path, new_path)
        print(f"Renamed {original_title} to {new_name}")
        
        # Delete the original JSON file
        os.remove(json_path)
        print(f"Deleted JSON file: {filename}")

