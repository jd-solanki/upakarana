import json
from dataclasses import dataclass, field
from typing import List

# TODO: Add emoji group support


@dataclass
class Emoji:
    full_name: str
    unicode: str
    has_skin_tones: bool
    aliases: List[str] = field(default_factory=list)


def parse_file(filename: str) -> List[Emoji]:
    with open(filename, "r") as file:
        lines = file.readlines()

    emojis: list[Emoji] = []
    emoji_dict = {}
    for line in lines:
        if not line.startswith("#") and line.strip() != "":
            # Split sections
            parts = line.split(";")

            # Get unicode sequence
            code_points = parts[0].strip().split(" ")

            # Get full name of emoji
            full_name = parts[2].split("#")[0].strip().split(": ")[0]

            # Combine unicode sequence
            unicode_sequence = "".join(
                [
                    f"\\U{code_point.zfill(8)}"
                    for code_point in code_points
                    if "1F3F" not in code_point
                ]
            )

            # Check if emoji has skin tones
            has_skin_tones = any("1F3F" in code_point for code_point in code_points)

            # Add emoji to dictionary if not already present. This is because in raw data file, same emoji is listed multiple times with different skin tones
            if full_name not in emoji_dict:
                emoji = Emoji(
                    full_name=full_name,
                    unicode=unicode_sequence,
                    has_skin_tones=has_skin_tones,
                )
                emoji_dict[full_name] = emoji
            else:
                if has_skin_tones:
                    emoji_dict[full_name].has_skin_tones = True

    emojis = list(emoji_dict.values())
    return emojis


def write_to_json(emojis: List[Emoji], filename: str) -> None:
    with open(filename, "w") as file:
        json.dump([emoji.__dict__ for emoji in emojis], file, indent=4)


emojis = parse_file("emoji-zwj-sequences.txt")
write_to_json(emojis, "emojis.json")
