from calculator import add, add_to_total, broken_total, record


def test_add():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-2, 3) == 1


def test_record_starts_a_separate_history_for_each_call():
    assert record(12) == [12]
    assert record(8) == [8]


def test_record_uses_the_supplied_empty_history():
    history = []
    assert record(12, history) is history
    assert record(8, history) == [12, 8]


def test_add_to_total_updates_an_existing_total():
    assert add_to_total(12, 8) == 20


def test_repaired_broken_total_can_be_called():
    assert broken_total() == 20
