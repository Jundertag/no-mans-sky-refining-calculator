import sys
import math

def calculate_most_restricted_item(inputs: list[tuple[int, str, int]]) -> tuple[int, str, int]:
    least_item: tuple[int, str, int] = (inputs[0][0], inputs[0][1], inputs[0][2])

    for i in range(1,len(inputs)):
        least_item_num = least_item[2] * least_item[0]
        iter_num = inputs[i][2] * inputs[i][0]

        if least_item_num > iter_num:
            least_item = inputs[i]
    
    return least_item

input_len = int(input("how many inputs for this refining recipe?: "))

print("for each ingredient, type the amount per tick first, then the ingredient name, then the amount you have, all separated by space, then enter for the next ingredient.")

inputs: list[str] = []
for n in range(input_len):
    inputs.append(input(f"slot {n} would be? (num ingredient amount): "))

format_inputs: list[tuple[int, str, int]] = []

for i in range(len(inputs)):
    in_i = inputs[i].split(" ")
    format_inputs.append((int(in_i[0]), in_i[1], int(in_i[2])))

output = input("output would be? (num ingredient): ")

split_output = output.split(" ")

format_output: tuple[int, str] = (int(split_output[0]), split_output[1])

time_per_unit = float(input("the amount of seconds per unit of output?: "))

num_refineries = int(input("how many refineries would you like to use?: "))

restricted_item = calculate_most_restricted_item(format_inputs)

restricted_item_num = restricted_item[2] * restricted_item[0]

time_total = (time_per_unit / format_output[0]) * (restricted_item[2] * restricted_item[0])

max_output = (restricted_item_num * format_output[0])

inputs_per_machine: list[int] = []
for i in range(len(inputs)):
    inputs_per_machine.append(math.floor(restricted_item_num * format_inputs[i][0]))

print(f"You can make a total of {max_output} {format_output[1]} using {num_refineries} refineries by putting")

for i in range(len(format_inputs)):
    print(f"{(restricted_item[2] * format_inputs[i][0]) / num_refineries} {format_inputs[i][1]}")

print(f"in each refinery, taking a total of {time_total / num_refineries} seconds")