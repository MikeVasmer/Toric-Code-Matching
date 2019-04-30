from toric_matching.toric_code import ToricCode
import json
import time
import argparse


def generate_data(dim, l, p, trials):
    code = ToricCode(dim, l)

    data = {}
    successes = 0

    start_time = time.time()

    for _ in range(trials):
        result = code.one_run(p)
        successes += result

    elapsed_time = round(time.time() - start_time, 2)

    data['dimension'] = dim
    data['L'] = l
    data['p'] = p
    data['trials'] = trials
    data['runtime'] = elapsed_time
    data['successes'] = successes

    json_filename = 'L={}_p={:0.4f}_dim={}_trials={}.json'.format(l, p, dim, trials)

    with open(json_filename, 'w') as output:
        json.dump(data, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Minimum weight perfect matching decoder for D-dimensional toric codes.')
    parser.add_argument('dimension', type=int,
                        help='spatial dimension of the toric code lattice')
    parser.add_argument(
        'l', type=int, help='length of the shortest cycle in the lattice')
    parser.add_argument('p', type=float, help='qubit error probability')
    parser.add_argument('trials', type=int, help='number of trials')

    args = parser.parse_args()
    dim = args.dimension
    l = args.l
    p = args.p
    trials = args.trials

    generate_data(dim, l, p, trials)
