def get_first_non_repeating_character(string):
    chars = list(string)
    count = {}
    for c in chars:
        if c in count:
            count[c] += 1
        else:
            count[c] = 1
    for i, c in enumerate(chars, 0):
        if count[c] == 1:
            return i
    return -1


if __name__ == '__main__':
    print(get_first_non_repeating_character('sseemless'))
