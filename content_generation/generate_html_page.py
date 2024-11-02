import json
import os
from datetime import datetime
import random
import re
from typing import List, Dict


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def load_json(file_path: str) -> List[Dict]:
    """Load JSON data from file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def load_template(file_path: str) -> str:
    """Load HTML template from file."""
    with open(file_path, 'r') as f:
        return f.read()


def save_html(file_path: str, content: str) -> None:
    """Save HTML content to file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)


def get_paragraph_html_first(title: str, description: str) -> str:
    """Generate HTML for a paragraph in the first section."""
    return f'''
    <div class="auto-layout-vertical-5 auto-layout-vertical-7">
                  <div class="auto-layout-vertical-6 auto-layout-vertical-7">
                    <div class="paragraph_1_title epilogue-medium-black-rock-46px">{title}</div>
                    <div class="paragraph_1_description epilogue-medium-black-rock-20px">{description}</div>
                  </div>
                </div>
'''


def get_paragraph_html_second(title: str, description: str) -> str:
    """Generate HTML for a paragraph in the second section."""
    return f'''
    <div class="auto-layout-vertical-12 auto-layout-vertical">
                  <div class="auto-layout-vertical-13 auto-layout-vertical">
                    <div class="paragraph_1_title-1 epilogue-medium-black-rock-26px">{title}</div>
                    <div class="paragraph_1_description-1 epilogue-medium-black-rock-18px">
                      {description}
                    </div>
                  </div>
                </div>
'''


def get_paragraph_html_third(title: str, description: str) -> str:
    """Generate HTML for a paragraph in the third section."""
    return f'''
    <div class="auto-layout-vertical-19 auto-layout-vertical">
                  <div class="auto-layout-vertical-20 auto-layout-vertical">
                    <div class="paragraph_1_title-2 epilogue-medium-black-rock-46px">{title}</div>
                    <div class="paragraph_1_description-2 epilogue-medium-black-rock-20px">
                      {description}
                    </div>
                  </div>
                </div>
'''


def construct_similar_posts(entries: List[Dict], current_entry: Dict) -> Dict:
    """Construct similar posts data."""
    other_entries = [e for e in entries if e != current_entry]
    similar_posts = random.sample(other_entries, min(3, len(other_entries)))

    result = {
        'links': [],
        'dates': [],
        'titles': []
    }

    for i in range(3):
        if i < len(similar_posts):
            post = similar_posts[i]
            slug = slugify(post.get('h1', ''))
            result['links'].append(f'/blog/{slug}')
            result['dates'].append(post.get('content', {}).get('date', ''))
            result['titles'].append(post.get('h1', ''))
        else:
            result['links'].append('')
            result['dates'].append('')
            result['titles'].append('')

    return result


def insert_paragraphs_after_intro(template: str, paragraphs: list, intro_class: str, get_paragraph_html_func) -> str:
    """Insert paragraphs after specified intro div."""
    intro_tag = f'<div class="{intro_class}">$INTRO</div>'
    if intro_tag not in template:
        return template

    parts = template.split(intro_tag)
    if len(parts) != 2:
        return template

    paragraphs_html = ''
    for paragraph in paragraphs:
        paragraphs_html += get_paragraph_html_func(
            paragraph.get('title', ''),
            paragraph.get('description', '')
        )

    return f'{parts[0]}{intro_tag}{paragraphs_html}{parts[1]}'


def replace_placeholders(template: str, entry: Dict, similar_posts: Dict) -> str:
    """Replace all placeholders in template with actual content."""
    content = entry['content']
    result = template

    # First, handle metadata replacements (these should only be replaced once)
    metadata_replacements = {
        '$METADATA_DESCRIPTION': content.get('metadata_description', ''),
        '$METADATA_TITLE': entry.get('metadata_title', '')
    }
    for placeholder, value in metadata_replacements.items():
        result = result.replace(placeholder, str(value))

    # Now handle the three breakpoints with their specific paragraph styles
    paragraphs = content.get('paragraphs', [])

    # First breakpoint
    result = insert_paragraphs_after_intro(
        result,
        paragraphs,
        "intro epilogue-medium-black-rock-20px",
        get_paragraph_html_first
    )

    # Second breakpoint
    result = insert_paragraphs_after_intro(
        result,
        paragraphs,
        "intro-1 epilogue-medium-black-rock-18px",
        get_paragraph_html_second
    )

    # Third breakpoint
    result = insert_paragraphs_after_intro(
        result,
        paragraphs,
        "intro-2 epilogue-medium-black-rock-20px",
        get_paragraph_html_third
    )

    # Handle remaining replacements - these need to be replaced for each section
    common_replacements = {
        '$TITLE': entry.get('h1', ''),
        '$DATE': content.get('date', ''),
        '$INTRO': content.get('intro', ''),
        '$EXAMPLE_TOPIC': entry.get('example_question', {}).get('topic', ''),
        '$EXAMPLE_QUESTION': entry.get('example_question', {}).get('question', ''),
        '$EXAMPLE_TITLE': entry.get('example_question', {}).get('title', '')
    }

    # Similar posts replacements
    for i in range(3):
        common_replacements[f'$SIMILAR_{i + 1}_LINK'] = similar_posts['links'][i]
        common_replacements[f'$SIMILAR_{i + 1}_DATE'] = similar_posts['dates'][i]
        common_replacements[f'$SIMILAR_{i + 1}_TITLE'] = similar_posts['titles'][i]

    # Apply all common replacements
    for placeholder, value in common_replacements.items():
        result = result.replace(placeholder, str(value))

    return result


def main():
    # Load data and template
    keywords = load_json('keywords.json')
    template = load_template('blog_template.html')

    # Process each entry
    for entry in keywords:
        if not entry.get('content'):
            continue

        slug = slugify(entry['h1'])
        similar_posts = construct_similar_posts(keywords, entry)
        html_content = replace_placeholders(template, entry, similar_posts)

        file_path = f'../public/blog/{slug}.html'
        save_html(file_path, html_content)
        print(f'Saved: {file_path}')


if __name__ == '__main__':
    main()