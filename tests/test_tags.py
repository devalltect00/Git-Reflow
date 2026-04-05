from app.core.tag_processor import TagProcessor


def test_valid_tag():
    tp = TagProcessor()
    assert tp.is_valid("v1.2.3")


def test_invalid_tag():
    tp = TagProcessor()
    assert not tp.is_valid("invalid-tag")