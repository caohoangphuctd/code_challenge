INPUT_ARR = [2, 7, 11, 10, 3, 15, 44, 12, -9, 3, 4]
SUM_TARGET = 6


def quick_sort(arr, start_idx, end_idx):
    if start_idx < end_idx:
        pivot = partition(arr, start_idx, end_idx)
        quick_sort(arr, start_idx, pivot - 1)
        quick_sort(arr, pivot + 1, end_idx)


def partition(arr, start_idx, end_idx):
    x = arr[end_idx]
    i = (start_idx - 1)
    for j in range(start_idx, end_idx):
        if arr[j] <= x:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[end_idx] = arr[end_idx], arr[i + 1]
    return i + 1


def get_terms_of_target(arr, sum_target):
    quick_sort(arr, 0, len(arr) - 1)
    left = 0
    right = len(arr) - 1
    res = []

    while left < right:
        if arr[left] + arr[right] == sum_target:
            res.append([arr[left], arr[right]])
            left += 1
            right -= 1
        elif arr[left] + arr[right] < sum_target:
            left += 1
        else:
            right -= 1

    return res


if __name__ == '__main__':
    print(get_terms_of_target(INPUT_ARR, SUM_TARGET))
