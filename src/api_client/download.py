
import pygame
import requests
from src.config import custom_events

from src.config import config

def download_by_set_id(set_id: str, artist: str, title: str) -> bool:
    response = requests.get(f"{config.api_download_url}/{set_id}", stream=True)

    if response.status_code in range(200, 400):
        filepath = config.external_packs_dir / f"{set_id} {artist} - {title}.osz"

        with open(filepath, "wb") as f:
            f.write(response.content)
        pygame.event.post(pygame.event.Event(custom_events.DOWNLOAD_PACK_COMPLETED, {"set_id": set_id}))
    else:
        print("Something went wrong. Status code =", response.status_code)
        try:
            error_data = response.json()
            error_message = error_data["error_message"]
            error_code = error_data["error_code"]
            print(f"Error: {error_message} (Code: {error_code})")
        except ValueError:
            print("Error parsing JSON content")
        except (requests.exceptions.JSONDecodeError, TypeError):
            print("JSONDecodeError")
