def get_integer_input(message):

    try:

        value = int(
            input(message)
        )

        if value < 0:

            raise ValueError

        return value

    except ValueError:

        print(
            "Please enter a valid "
            "positive number."
        )

        return None


def get_float_input(message):

    try:

        value = float(
            input(message)
        )

        if value < 0:

            raise ValueError

        return value

    except ValueError:

        print(
            "Please enter a valid "
            "positive number."
        )

        return None