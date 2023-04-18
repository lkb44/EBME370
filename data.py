import random

def random_within_deviation(number, deviation):
    """Returns a random number between number-deviation and number+deviation."""
    lower_bound = round(number - deviation, 2)
    upper_bound = round(number + deviation, 2)
    return round(random.uniform(lower_bound, upper_bound), 2)

for i in range(3):
    print(random_within_deviation(296.45, 36.89))
for i in range(3):
    print(random_within_deviation(257.98, 38.24))
for i in range(3):
    print(random_within_deviation(251.28, 30.19))
for i in range(3):
    print(random_within_deviation(266.11, 38.53))
for i in range(3):
    print(random_within_deviation(229.47, 40.59))