import tinycss2


def find_static_files_in_css(css_content: str) -> list[str]:
    files = []
    parsed_css = tinycss2.parse_stylesheet(
        css_content, skip_whitespace=True, skip_comments=True
    )

    for rule in parsed_css:
        # print(rule.type, "-", rule.content)
        if rule.type == "qualified-rule":
            for token in rule.content:
                if token.type == "function":
                    for token_string in token.arguments:
                        if (
                            token_string.type == "string"
                            and token_string.value.endswith("svg")
                        ):
                            if token_string.value not in files:
                                files.append(token_string.value)
                    # print(token)
        if rule.type == "at-rule":
            for token in rule.content:
                if token.type == "[] block":
                    for block in token.content:
                        if block.type == "string" and block.value.endswith(
                            "gif"
                        ):
                            if block.value not in files:
                                files.append(block.value)

    return files


if __name__ == "__main__":
    with open(
        "/Users/terrya/projects/test-django/static/news.css?opW4ZycEcIS5qqTkuJC2",
        "r",
    ) as f:
        css = f.read()
    print(find_static_files_in_css(css))
