def print_info(**kwargs):
    """
    Print the key-value pairs in **kwargs.

    Parameters:
        **kwargs (dict): A dictionary of key-value pairs.

    Returns:
        None
    """
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_info(first="John", last="Doe", age=28, profession="Salesman")
