import json
import os
import time
from urllib.request import Request, urlopen, build_opener
BASE_URL = "https://api.nexusmods.com"
API_VERSION = "v1"
API_URL = f"{BASE_URL}/{API_VERSION}/games"
from env import API_KEY

# Docs: https://app.swaggerhub.com/apis-docs/NexusMods/nexus-mods_public_api_params_in_form_data/1.0

xEdits = {
    "TES4Edit": {
        "name": "TES4Edit",
        "game": "oblivion",
        "id": 11536,
    },
    "FO3Edit": {
        "name": "FO3Edit",
        "game": "fallout3",
        "id": 637,
    },
    "FNVEdit": {
        "name": "FNVEdit",
        "game": "newvegas",
        "id": 34703,
    },
    "TES5Edit": {
        "name": "TES5Edit",
        "game": "skyrim",
        "id": 25859,
    },
    "EnderalEdit": {
        "name": "EnderalEdit",
        "game": "enderal",
        "id": 23,
    },
    "SSEEdit": {
        "name": "SSEEdit",
        "game": "skyrimspecialedition",
        "id": 164,
    },
    "EnderalSEEdit": {
        "name": "EnderalSEEdit",
        "game": "enderalspecialedition",
        "id": 78,
    },
    "FO4Edit": {
        "name": "FO4Edit",
        "game": "fallout4",
        "id": 2737,
    },
    "FO76Edit": {
        "name": "FO76Edit",
        "game": "fallout76",
        "id": 30,
    }
}

def get_main_file_id(edit):
	request = Request(f"{API_URL}/{edit['game']}/mods/{edit['id']}/files.json", headers={"apikey": API_KEY})
	response = urlopen(request)
	data = json.loads(response.read())
	files_array = data["files"]
	for file in files_array:
		if file["is_primary"]:
			edit["version"] = file["version"] # Set version on edit
			edit["file_id"] = file["file_id"] # Set file_id on edit
			return file["file_id"] # Return file_id for use in download_link
	print("No main file found for ", edit["name"])

def get_download_link(edit):
	file_id = get_main_file_id(edit)
	request = Request(f"{API_URL}/{edit['game']}/mods/{edit['id']}/files/{file_id}/download_link.json", headers={"apikey": API_KEY})
	response = urlopen(request)
	data = json.loads(response.read())
	for cdn in data:
		if cdn["short_name"] == "Nexus CDN":
			return cdn["URI"]
	print("No download link found for ", edit["name"])

def download_file(edit):
	download_link = get_download_link(edit)
	# Rewrite spaces to %20
	download_link = download_link.replace(" ", "%20")
	opener = build_opener()
	print("Download link: ", download_link)
	opener.addheaders = [("apikey", API_KEY), ("User-Agent", "Mozilla/5.0")]
	filename = f"{edit['name']} {edit['version']}.7z"
	path = f"./downloads/{edit['name']}/{filename}"
	if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))
	# If file already exists, skip download
	if os.path.exists(path):
		print(f"File {filename} already exists, skipping download...")
		return
	with opener.open(download_link) as response:
		with open(path, "wb") as file:
			file.write(response.read())

for edit in xEdits:
	print(f"Downloading {edit}...")
	download_file(xEdits[edit])
	# Wait 1 second between downloads, to prevent rate limiting
	time.sleep(1)
