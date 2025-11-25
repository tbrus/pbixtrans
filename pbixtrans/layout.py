import json
import os
from typing import Any

from pbixtrans.translator import translate


def get_layout(extract_folder: str) -> dict[str, Any]:
    """Loads and returns the Power BI Layout JSON from an extracted PBIX folder.

    The Layout file defines report pages, visuals, textbox content,
    and metadata. It is stored UTF-16LE encoded inside:

        <extract_folder>/Report/Layout

    Args:
        extract_folder (str): Path to the folder containing the extracted PBIX.

    Returns:
        dict[str, Any]: Parsed JSON object representing the report layout.

    Raises:
        FileNotFoundError: If the Layout file does not exist.
        JSONDecodeError: If the Layout file is not valid JSON.
    """
    layout_path = os.path.join(extract_folder, "Report/Layout")
    with open(layout_path, 'r', encoding='utf-16le') as f:
        layout = json.load(f)
    return layout


def translate_layout(layout: dict[str, Any], dst_lng: str) -> dict[str, Any]:
    """Translates all translatable text inside the PBIX Layout object.

    This function updates:
      - Section (page) display names
      - Text inside visual textboxes

    Args:
        layout (dict[str, Any]): The parsed Power BI layout JSON object.
        dst_lng (str): Target language code (ISO 639-1).

    Returns:
        dict[str, Any]: The modified layout object with translated text.
    """
    print(f"Translating to '{dst_lng}'")
    
    sections = layout.get('sections', [])
    print(f"Found {len(sections)} sections")

    for section in sections:
        # Translate section/page name
        if 'displayName' in section:
            original = section['displayName']
            translated = translate(original, dst_lng)
            section['displayName'] = translated
            print(f"Section: '{original}' -> '{translated}'")

        # Get all visual containers in the section (e.g. shapes, textboxes, charts)
        for vc in section.get('visualContainers', []):
            config_str = vc['config']
            if isinstance(config_str, str):
                vc_config = json.loads(config_str)
            else:
                vc_config = config_str
            single_visual = vc_config.get('singleVisual', {})

            # Translate textbox
            if single_visual.get('visualType') == "textbox":
                for gen_object in single_visual.get('objects', {}).get('general', []):
                    paragraphs = gen_object.get('properties', {}).get('paragraphs', [])
                    for paragraph in paragraphs:
                        for text_run in paragraph.get("textRuns", []):
                            val = text_run.get("value", "")
                            if isinstance(val, str) and val.strip():
                                translated_val = translate(val, dst_lng)
                                print(f"Textbox: '{val}' -> '{translated_val}'")
                                text_run["value"] = translated_val
            
            # Translate other visual types as needed here...

            vc['config'] = json.dumps(vc_config, ensure_ascii=False, separators=(',', ':'))

    return layout


def save_layout(layout: dict[str, Any], extract_folder: str) -> dict[str, Any]:
    """Saves the modified layout JSON back to the extracted PBIX folder.

    The Layout file must be saved using UTF-16LE encoding,
    otherwise Power BI Desktop will refuse to load the PBIX.

    Args:
        layout (dict[str, Any]): Updated layout JSON object.
        extract_folder (str): Path to the extracted PBIX folder.

    Returns:
        dict[str, Any]: The same layout object (returned for convenience).

    Raises:
        FileNotFoundError: If the target directory does not exist.
    """
    layout_path = os.path.join(extract_folder, "Report/Layout")
    json_str = json.dumps(layout, ensure_ascii=False, separators=(',', ':'))
    with open(layout_path, 'w', encoding='utf-16le') as f:
        f.write(json_str)
    return layout