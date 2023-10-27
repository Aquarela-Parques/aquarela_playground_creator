def add_numbers(*args):
    """
    Adds a variable number of numbers together and returns the sum.

    Parameters:
    *args (float or int): The numbers to be added together.

    Returns:
    float or int: The sum of the numbers.
    """
    result = 0
    for num in args:
        result += num
    return result


sum_result = add_numbers(1, 2, 3, 4, 5)
print(sum_result)  # Output: 15
