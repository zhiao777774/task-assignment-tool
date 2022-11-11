import argparse


def positive(value):
    val = int(value)
    if val <= 0:
        raise argparse.ArgumentTypeError(f'{value} is an invalid positive int value')
    return val


def parse_args():
    p = argparse.ArgumentParser()

    def a(*args, **kwargs):
        p.add_argument(*args, **kwargs)

    a('--input', '-i', type=str, default='data.csv', help='Data to use, please include the extension')
    a('--output', '-o', type=str, default='result.csv', help='output file name')
    a('--p-size', '-p', type=int, default=50, help='population size')
    a('--c-rate', '-c', type=float, default=0.2, help='Crossover rate')
    a('--m-rate', '-m', type=float, default=0.1, help='Mutation rate')
    a('--n-iter', '-n', type=int, default=1000, help='number of iterations')

    return p.parse_args()


def parse_gen_args():
    p = argparse.ArgumentParser()

    def a(*args, **kwargs):
        p.add_argument(*args, **kwargs)

    a('--output', '-o', type=str, default='simulated-data.csv', help='output file name')
    a('--n-tasks', '-nt', type=int, default=5, help='number of tasks (jobs)')
    a('--n-items', '-ni', type=int, default=10, help='number of items (persons, machines, etc.)')

    return p.parse_args()
