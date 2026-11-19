def add(a, b):
    return a + b


def record(value, history=None):
    if history is None:
        history = []
    history.append(value)
    return history


def add_to_total(total, value):
    total = add(total, value)
    return total
