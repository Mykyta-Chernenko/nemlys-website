import csv
import json
import re


def parse_list_items(text):
    """Parse items from text that contains HTML break tags and bullet points."""
    if not text:
        return []

    # Remove HTML break tags and convert to list
    items = re.split(r'<br>|<br/>', text)
    # Clean up items and remove empty ones
    items = [re.sub(r'^[-•\s]*|^\d+\.\s*', '', item.strip()) for item in items]
    return [item for item in items if item]


def determine_content_type(title, h2s):
    """Determine if the content is questions or guide based on title and h2s."""
    questions_indicators = ['questions', 'quizzes', 'ask', 'game']
    title_lower = title.lower()

    # If it contains specific words related to services, it's likely a guide
    if any(word in title_lower for word in ['therapy', 'counseling', 'guide']):
        return "guide"

    # If it contains questions-related words, it's likely questions
    if any(word in title_lower for word in questions_indicators):
        return "questions"

    return "questions"  # Default to questions as most content is questions-based


def get_secondary_keywords(row):
    """Extract all non-empty secondary keywords from the row."""
    keywords = []
    for i in range(1, 15):  # Secondary keywords 1-14
        key = f'Secondary keyword {i}'
        if key in row and row[key].strip():
            keywords.append(row[key].strip())
    return keywords


def convert_csv_to_json(csv_file_path, json_file_path):
    """Convert CSV to specified JSON structure."""
    data = []

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # Parse H2s
            h2s = parse_list_items(row['H2s'])
            # Create paragraphs structure from H2s
            paragraphs = [
                {
                    "title": h2_title,
                    "description": None
                }
                for h2_title in h2s
            ]

            # Create entry
            entry = {
                "metadata_title": row['Title (visible in the web search)'],
                "h1": row['H1 (visible on the web page)'],
                "keyword_main": row['Primary keyword'],
                "other_keywords": get_secondary_keywords(row),
                "content": {
                    "type": determine_content_type(row['Title (visible in the web search)'], h2s),
                    "metadata_description": None,
                    "intro": None,
                    "paragraphs": paragraphs
                },
                "example_question": {
                    "title": None,
                    "example_question": None,
                    "topic": None,
                }
            }

            data.append(entry)

    # Write to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return data


# Example usage
if __name__ == "__main__":
    input_csv = "./keywords.csv"
    output_json = "./keywords.json"

    try:
        data = convert_csv_to_json(input_csv, output_json)
        print(f"Successfully converted CSV to JSON. Output saved to {output_json}")
        print(f"Processed {len(data)} entries.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
