import pytest


test_data = [('madisonmay', None), ("tcr", ["tcr/something"])]
cache_data = [('torvalds', None), ("tcr", ["torvalds/linux"])]

expected_output = [('madisonmay', None), ("tcr", ["tcr/something"]), ("torvalds", ["torvalds/linux"])]

def get_full_path(partial_path, cache_data):
    data = partial_path + cache_data[::-1]
    # structure data such that the first item in every tuple is not repeated and
    for item in range(len(data)-2):
        if data[item][0] == data[item+1][0]:
            data[item+1] = (data[item+2][0], data[item+1][1])
    return data[:-1]

def test_get_full_path():
    full_path = get_full_path(test_data, cache_data)
    assert full_path == expected_output