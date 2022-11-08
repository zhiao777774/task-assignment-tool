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
    a('--output', '-o', type=str, default='result.csv')
    a('--p-size', '-p', type=int, default=50)
    a('--c-rate', '-c', type=positive, default=0.2)
    a('--m-rate', '-m', type=positive, default=0.1)
    a('--n-expr', '-n', type=int, default=1000)

    return p.parse_args()


def parse_gen_args():
    p = argparse.ArgumentParser()

    def a(*args, **kwargs):
        p.add_argument(*args, **kwargs)

    a('--output', '-o', type=str, default='simulated-data.csv')
    a('--n-task', '-t', type=int, default=5)
    a('--n-item', '-i', type=int, default=10)

    return p.parse_args()
