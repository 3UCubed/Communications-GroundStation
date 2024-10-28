def decode(input: bytes) -> bytes:
    read_index = 0
    output = []

    while (read_index < len(input) - 1):
        next_zero_pos = input[read_index]

        for i in range(read_index + 1, read_index + next_zero_pos):
            output.append(input[i])

        output.append(0)

        read_index = read_index + next_zero_pos

    # strip last zero because it is just a message delimiter
    if (len(output) > 1):
        output = output[:-1]

    return bytes(output)
