import requests
import json
import re

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

        return {
            "name": cleaned_name,
            "visits": game_data["visits"],
            "thumbnail": thumbnail_data["imageUrl"]
        }
    else:
        print("❌ Error fetching data. Check if the Universe ID is valid.")
        return None

# Prompt user for a Universe ID
universe_id = input("Enter the Roblox game's Universe ID: ")

# Get the game data
game_info = get_game_data(universe_id)

# Save data to a JSON file
if game_info:
    with open("game_data.json", "w") as json_file:
        json.dump(game_info, json_file, indent=4)
    print("✅ Game data saved to 'game_data.json'")