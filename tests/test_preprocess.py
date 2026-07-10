from utils.preprocess import clean_text


def test_clean_text_lowercases():
    assert clean_text("HELLO World") == "hello world"


def test_clean_text_removes_urls():
    assert clean_text("check this out http://example.com/page") == "check this out"


def test_clean_text_removes_punctuation_and_numbers():
    assert clean_text("Wow!! This is #1, great...") == "wow this is great"


def test_clean_text_collapses_whitespace():
    assert clean_text("too    many   spaces") == "too many spaces"


def test_clean_text_full_pipeline_on_realistic_tweet():
    tweet = "I LOVE this product!!! Check it out: https://t.co/abc123 #amazing @friend"
    assert clean_text(tweet) == "i love this product check it out amazing friend"


def test_clean_text_empty_string():
    assert clean_text("") == ""
