import os
import re
from datetime import datetime


def update_html_license(directory, new_authors, new_date=None):
    if new_date is None:
        new_date = datetime.now().strftime(
            "%a %b %d %Y"
        )  # Current date in specified format

    # Patterns to match old content in HTML
    html_authors_pattern = re.compile(r"<!-- Copyright \(c\) \d{4} .* -->")
    html_date_pattern = re.compile(r"<!-- Created on .* -->")

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):  # Target only .html files
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Update copyright and date
                content = html_authors_pattern.sub(
                    f"<!-- Copyright (c) {datetime.now().year} {new_authors} -->",
                    content,
                )
                content = html_date_pattern.sub(
                    f"<!-- Created on {new_date} -->", content
                )

                # Write updated content back to the file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)


# Configuration
project_directory = "./"  # Path to the project root
updated_authors = (
    "Niharika Maruvanahalli Suresh , Diya Shetty, Sanjana Nanjangud Shreenivas"
)
update_html_license(project_directory, updated_authors)
