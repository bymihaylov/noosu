import requests

from src.config import config


def search_beatmap(text: str, amount: int = 5) -> list[tuple[str, str, str, str]]:
    """
    Queries the beatmap API to search for beatmaps based on a given text query.

    Args:
        text (str): The text query to search for in the beatmap database.
        amount (int, optional): The maximum number of results to retrieve. Defaults to 5.

    Returns:
        list[tuple[str, str, str, str]]: A list of tuples containing the following information about each beatmap:
            - Title: The title of the beatmap as a string.
            - Artist: The artist of the beatmap as a string.
            - Difficulty: The difficulty of the beatmap as a string.
            - Set_Id: The set ID of the beatmap as a string.

    Raises:
        ValueError: If the API response does not contain the expected data structure.
    """
    req = requests.get(config.api_search_url, params={"query": text, "amount": amount})
    data = req.json().get("data", [])

    if not data:
        raise ValueError("No data found in API response.")


    beatmap_info_list = []

    for beatmap_info in data:
        title = beatmap_info.get("Title", "")
        artist = beatmap_info.get("Artist", "")
        difficulty = beatmap_info["ChildrenBeatmaps"][0]["DiffName"] if beatmap_info["ChildrenBeatmaps"] else "Unknown"
        set_id = str(beatmap_info.get("SetId", ""))
        beatmap_info_list.append((title, artist, difficulty, set_id))

    return beatmap_info_list

