import json

# Load the existing JSON file
file_path = "game_data.json"  # Update this to your actual file path

try:
    with open(file_path, "r") as file:
        games_data = json.load(file)
except FileNotFoundError:
    print("Error: JSON file not found.")
    exit()

# Add the new field to each game object
for game in games_data:
    game["thumbnail_imageID"] = ""

# Save the updated JSON file
with open(file_path, "w") as file:
    json.dump(games_data, file, indent=4)

print("\n✅ JSON file updated successfully!")