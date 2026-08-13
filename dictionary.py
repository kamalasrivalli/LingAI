import re


def parse_wiktionary(content: str, word: str) -> str:

    # Find German section
    german_match = re.search(
        r"===\s*\{\{Sprache\|deutsch.*?\}\}\s*===\s*(.*?)(?=\n===|\Z)",
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not german_match:
        return f"No German entry found for '{word}'."

    section = german_match.group(1)

    # Extract meanings
    meanings = re.search(
        r"====?\s*Bedeutungen\s*====?\s*(.*?)(?=\n====?|\Z)",
        section,
        re.DOTALL
    )

    # Extract examples
    examples = re.search(
        r"====?\s*Beispiele\s*====?\s*(.*?)(?=\n====?|\Z)",
        section,
        re.DOTALL
    )

    # Remove common wiki markup
    def clean(text):
        text = re.sub(r"\{\{.*?\}\}", "", text)
        text = re.sub(
            r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]",
            r"\1",
            text
        )
        text = re.sub(r"'{2,}", "", text)
        text = re.sub(r"<.*?>", "", text)
        return text.strip()

    result = f"Word: {word}"

    if meanings:
        result += "\n\nMeanings:\n" + clean(meanings.group(1))

    if examples:
        result += "\n\nExamples:\n" + clean(examples.group(1))

    if not meanings and not examples:
        result += "\n\nNo meaning or example section found."

    return result