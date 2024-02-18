from fuzzywuzzy import fuzz
import math


def find_substring_position(article, target_substring):
    target_length = len(target_substring)
    curr_matching = None
    highest_sim = -math.inf

    for start_pos in range(len(article) - target_length + 1):
        end_pos = start_pos + target_length
        current_substring = article[start_pos:end_pos]

        similarity = fuzz.ratio(current_substring, target_substring)

        if similarity >= highest_sim:
            curr_matching = (start_pos, end_pos)
            highest_sim = similarity

    return curr_matching


if __name__ == "__main__":
    # Usage
    article_text = (
        "This is an example article text where we try to find a very similar substring."
    )
    substring = "example article text"
    start_pos, end_pos = find_substring_position(article_text, substring)

    print(f"Start: {start_pos}, End: {end_pos}")
    assert substring == article_text[start_pos:end_pos]
    print("Test Completed")
