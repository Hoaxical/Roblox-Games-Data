import requests
import json
import re
import os

# Ensure subfolder exists for thumbnails
SAVE_FOLDER = "game_thumbnails"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Function to remove emojis from the game name
def clean_game_name(name):
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric symbols
        "\U0001F800-\U0001F8FF"  # Supplemental symbols
        "\U0001F900-\U0001F9FF"  # Supplemental pictographs
        "\U0001FA00-\U0001FA6F"  # Symbols & pictographs extended
        "\U0001FA70-\U0001FAFF"  # More symbols
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub("", name)

# Function to round visits to the nearest thousand, million, or billion
def round_visits(visits):
    if visits >= 1_000_000_000:  # Billions
        return round(visits / 1_000_000_000) * 1_000_000_000
    elif visits >= 1_000_000:  # Millions
        return round(visits / 1_000_000) * 1_000_000
    elif visits >= 1_000:  # Thousands
        return round(visits / 1_000) * 1_000
    return visits  # If less than 1,000, keep as is

# Function to fetch game data from Roblox API
def get_game_data(universe_id):
    game_url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
    thumbnail_url = f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&size=150x150&format=Png&isCircular=false"

    # Fetch game details
    game_response = requests.get(game_url)
    thumbnail_response = requests.get(thumbnail_url)

    if game_response.status_code == 200 and thumbnail_response.status_code == 200:
        game_data = game_response.json()["data"][0]  # Extract game details
        thumbnail_data = thumbnail_response.json()["data"][0]  # Extract thumbnail

        cleaned_name = clean_game_name(game_data["name"])  # Remove emojis
        rounded_visits = round_visits(game_data["visits"])  # Round visits

        return {
            "name": cleaned_name,
            "universeId": universe_id,
            "visits": rounded_visits,
            "thumbnail": thumbnail_data["imageUrl"]
        }
    else:
        print(f"❌ Error fetching data for Universe ID: {universe_id}. Check if it is valid.")
        return None

# Function to download and save thumbnail in the "game_thumbnails" folder
def download_thumbnail(thumbnail_url, game_name):
    sanitized_name = "".join(c for c in game_name if c.isalnum() or c in (" ", "_")).strip()  # Clean filename
    save_path = os.path.join(SAVE_FOLDER, f"{sanitized_name}_thumbnail.png")

    response = requests.get(thumbnail_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"✅ Thumbnail saved at: {save_path}")
    else:
        print("❌ Failed to download thumbnail.")

# Function to load existing JSON file or create a new one
def load_game_data():
    json_file = "game_data.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            return json.load(file)
    return []  # Return empty list if no data exists

# Function to save game data immediately
def save_game_data(game_list):
    json_file = "game_data.json"
    with open(json_file, "w") as file:
        json.dump(game_list, file, indent=4)
    print(f"✅ Game data saved to '{json_file}'.")

# Function to read Universe IDs from `universe_ids.txt`
def load_universe_ids():
    txt_file = "universe_ids.txt"
    
    universe_ids = []

    if os.path.exists(txt_file):
        with open(txt_file, "r") as file:
            universe_ids = [line.strip() for line in file if line.strip().isdigit()]
            print("Loaded Universe IDs:", universe_ids)
    
    return universe_ids

# Main function to process all universe IDs from the text file
def process_universe_ids():
    universe_ids = load_universe_ids()  # Load Universe IDs from file
    game_data_list = load_game_data()  # Load existing games

    for universe_id in universe_ids:
        print(f"🔍 Processing Universe ID: {universe_id}")
        game_info = get_game_data(universe_id)

        if game_info:
            game_data_list.append(game_info)  # Append new game data
            print(f"🎮 Added: {game_info['name']} - Visits: {game_info['visits']}")

            # Download thumbnail for the game
            download_thumbnail(game_info["thumbnail"], game_info["name"])

            # Save JSON immediately after each game entry
            save_game_data(game_data_list)

    print("👋 All games processed successfully!")

# Run the script
process_universe_ids()