from bs4 import BeautifulSoup


def clean_html_file(file_path: str, h1_text: str = None) -> None:
    """
    Cleans an HTML file by removing unwanted tags and attributes, in-place.
    Optionally inserts an <h1> with given text into the third <div> of the first <article>.
    """

    # Read the HTML content
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # save original
    with open('index-1.html', "w", encoding="utf-8") as file:
        file.write(html_content)

    soup = BeautifulSoup(html_content, "html.parser")

    # --- Removal Rules ---

    # --- Extra Feature: Insert H1 into third div of first article ---
    if h1_text:
        first_article = soup.find("article")
        if first_article:
            divs = first_article.find_all("div")
            if len(divs) >= 3:
                h1_tag = soup.new_tag("h1")
                h1_tag.string = h1_text
                divs[2].insert(0, h1_tag)  # insert at beginning of 3rd div

    # 1. Remove empty <div> tags, but keep if they contain <img>
    for div in soup.find_all("div"):
        has_text = bool(div.get_text(strip=True))
        has_img = bool(div.find("img"))
        if not has_text and not has_img:
            div.decompose()

    # 2. Remove all <script> tags
    for script_tag in soup.find_all("script"):
        script_tag.decompose()

    # 3. Remove <link> tags pointing to .js files
    for link in soup.find_all("link", href=True):
        if link["href"].split("?")[0].endswith(".js"):
            link.decompose()

    # 4. Remove specific elements by id or class
    ids_to_remove = [
        "stage-slideover-sidebar",
        "page-header",
        "thread-bottom-container",
        "pointer-events-none",
    ]

    classes_to_remove = [
        "absolute start-0 end-0 bottom-full z-20",
        "flex min-h-[46px] justify-start",
        "user-message-bubble-color",
    ]

    for element_id in ids_to_remove:
        for tag in soup.find_all(attrs={"id": element_id}):
            tag.decompose()

    for class_name in classes_to_remove:
        for tag in soup.find_all(attrs={"class": class_name}):
            tag.decompose()

    # 5. Remove inline styles (example: opacity: 1;)
    for tag in soup.find_all(style="opacity: 1;"):
        tag.decompose()

    # 6. Remove "crossorigin" attribute from <link> tags
    for link in soup.find_all("link", attrs={"crossorigin": True}):
        del link["crossorigin"]

    draggable = soup.find('div', class_='draggable')
    if draggable:
        draggable.decompose()

    # --- Write back cleaned HTML (overwrite original file) ---
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))

    print(f"✅ Cleaned HTML saved in-place at {file_path}")


# Example usage
if __name__ == "__main__":
    clean_html_file("index.html", h1_text="Latest trends in artificial intelligence")
