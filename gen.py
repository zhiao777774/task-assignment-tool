import csv
import random
import config
from args import parse_gen_args


def generate_simulation_data(n_task, n_item):
    data = []
    for i in range(n_item):
        scores = list(range(n_task))
        random.shuffle(scores)

        data.append(scores)

    return data


def main():
    args = parse_gen_args()
    n_task = args.n_task
    n_item = args.n_item
    assert n_item >= n_task, 'number of "item" must greater than or equal to "task"'

    data = generate_simulation_data(n_task, n_item)

    with open(config.IN_DIR / args.output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([f't{i + 1}' for i in range(n_task)])
        writer.writerows(data)


if __name__ == '__main__':
    main()
