def count_nonblank(lines):
    count = 0
    for line in lines:
        if line.strip():
            count += 1
    return count


def sum_even(numbers):
    total = 0
    for number in numbers:
        if number % 2 == 0:
            total += number
    return total
