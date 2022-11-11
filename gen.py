import csv
import random
import config
from args import parse_gen_args


def generate_simulation_data(n_tasks, n_items):
    data = []
    for i in range(n_items):
        scores = list(range(n_tasks))
        random.shuffle(scores)

        data.append(scores)

    return data


def main():
    args = parse_gen_args()
    n_tasks = args.n_tasks
    n_items = args.n_items
    assert n_items >= n_tasks, 'number of "item" must greater than or equal to "task"'

    data = generate_simulation_data(n_tasks, n_items)

    with open(config.IN_DIR / args.output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([f't{i + 1}' for i in range(n_tasks)])
        writer.writerows(data)


if __name__ == '__main__':
    main()
