import json
import re

with open('./keywords.json', 'r') as file:
    blog_keywords = json.load(file)

# Step 3: Create new HTML files and collect URLs for sitemap
urls = []

# Step 4: Update sitemap.xml
sitemap_header = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
    <url>
        <loc>https://nemlys.com/</loc>
        <priority>1.0</priority>
        <changefreq>monthly</changefreq>
    </url>
    <url>
        <loc>https://nemlys.com/policy</loc>
        <priority>1.0</priority>
        <changefreq>monthly</changefreq>
    </url>
    <url>
        <loc>https://nemlys.com/terms</loc>
        <priority>1.0</priority>
        <changefreq>monthly</changefreq>
    </url>
    <url>
        <loc>https://nemlys.com/delete_account</loc>
        <priority>0.5</priority>
        <changefreq>monthly</changefreq>
    </url>'''
sitemap_footer = '''
</urlset>'''

# Add new city URLs
sitemap_urls = ''
for url in urls:
    sitemap_urls += f'''
    <url>
        <loc>{url}</loc>
        <priority>0.9</priority>
        <changefreq>monthly</changefreq>
    </url>'''


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


for keyword in blog_keywords:
    if keyword.get('content', None):
        url = f'https://nemlys.com/blog/{slugify(keyword["h1"])}'
        sitemap_urls += f'''
        <url>
            <loc>{url}</loc>
            <priority>0.9</priority>
            <changefreq>monthly</changefreq>
        </url>'''

# Combine parts and save sitemap.xml
sitemap_content = sitemap_header + sitemap_urls + sitemap_footer
with open('../public/sitemap.xml', 'w') as sitemap_file:
    sitemap_file.write(sitemap_content)

print("sitemap.xml have been created successfully.")
