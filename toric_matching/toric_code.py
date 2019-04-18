import networkx as nx
import itertools
import random
from toric_matching.code import Code


def manhattan_distance(x, y, l):
    dist = 0
    for i in range(len(x)):
        dist_i = min((x[i] - y[i]) % l, (y[i] - x[i]) % l)
        dist += dist_i
    return dist


class Toric_Code(Code):

    def __init__(self, dim, l):
        Code.__init__(self, dim, l)
        self.lattice = nx.grid_graph(dim=([l] * dim), periodic=True)
        nx.set_edge_attributes(self.lattice, 0, 'qubit_state', )
        # using convention -1 ^ (stabilizer_value)
        nx.set_node_attributes(self.lattice, 0, 'stabilizer_value')
        self.build_pos()
        self.build_logicals()

    def build_pos(self):
        self.pos = {}
        if self.dim == 2:
            for perm in itertools.product(range(self.l), repeat=2):
                self.pos[perm] = [perm[0], perm[1]]
        elif self.dim == 3:
            for perm in itertools.product(range(self.l), repeat=3):
                self.pos[perm] = [perm[0] + 0.33 *
                                  perm[2], perm[1] + 0.33 * perm[2]]
        elif self.dim > 3:
            self.pos = nx.spring_layout(self.lattice)

    def draw(self):
        nx.draw(self.lattice, self.pos)
        # node_labels = nx.get_node_attributes(self.lattice, 'stabilizer_value')
        # nx.draw_networkx_labels(self.lattice, self.pos, labels=node_labels)
        # edge_labels = nx.get_edge_attributes(self.lattice, 'qubit_state')
        # nx.draw_networkx_edge_labels(
        #     self.lattice, self.pos, labels=edge_labels)

    def calculate_syndrome(self):
        for node in self.lattice.nodes():
            stabilizer_value = 0
            for neighbour in self.lattice[node]:
                stabilizer_value += self.lattice[node][neighbour]['qubit_state']
            stabilizer_value = stabilizer_value % 2
            self.lattice.node[node]['stabilizer_value'] = stabilizer_value

    def generate_errors(self, p):
        for edge in self.lattice.edges():
            if random.random() < p:
                self.lattice[edge[0]][edge[1]]['qubit_state'] = (
                    self.lattice[edge[0]][edge[1]]['qubit_state'] + 1) % 2

    def build_matching_graph(self):
        self.matching_graph = nx.Graph()
        for node in self.lattice.nodes():
            if self.lattice.nodes[node]['stabilizer_value'] == 1:
                self.matching_graph.add_node(node)
        for node in self.matching_graph.nodes():
            for neighbour in self.matching_graph.nodes():
                if node == neighbour:
                    continue
                # Use negative weights because nx calculates max weight matching
                self.matching_graph.add_edge(
                    node, neighbour, weight=-manhattan_distance(node, neighbour, self.l))

    def apply_correction(self):
        matching = nx.max_weight_matching(
            self.matching_graph, maxcardinality=True)
        matching_list = list(matching)
        for match in matching_list:
            correction_path = nx.shortest_path(
                self.lattice, match[0], match[1])
            for i in range(len(correction_path) - 1):
                self.lattice[correction_path[i]][correction_path[i + 1]]['qubit_state'] = (
                    self.lattice[correction_path[i]][correction_path[i + 1]]['qubit_state'] + 1) % 2

    def build_logicals(self):
        self.logicals = []
        seed = [1, ] + [0, ] * (self.dim - 1)
        unique_perms = set(list(itertools.permutations(seed)))
        while len(unique_perms) > 0:
            perm = list(unique_perms.pop())
            non_zero_index = 0
            for i in range(len(perm)):
                if perm[i] == 1:
                    non_zero_index = i
            logical = []
            for i in range(self.l):
                next_perm = perm.copy()
                next_perm[non_zero_index] = (
                    next_perm[non_zero_index] + 1) % self.l
                logical.append((tuple(perm), tuple(next_perm)))
                perm = next_perm.copy()
            self.logicals.append(logical)

    def check_correction(self):
        for logical in self.logicals:
            parity = 0
            for edge in logical:
                parity += self.lattice[edge[0]][edge[1]]['qubit_state']
            parity = parity % 2
            if parity == 1:
                return False
        return True

    def print_syndrome(self):
        # print('Stabilizer = Value')
        print('Unsatisfied stabilizers:')
        for node in self.lattice.nodes():
            if self.lattice.nodes[node]['stabilizer_value'] == 1:
                print(node)
            # print(node, '=', self.lattice.nodes[node]['stabilizer_value'])

    def print_errors(self):
        # print('Qubit = Error')
        print('Qubits with errors:')
        for edge in self.lattice.edges():
            if self.lattice[edge[0]][edge[1]]['qubit_state'] == 1:
                print(edge)
            # print(edge, '=', self.lattice[edge[0]][edge[1]]['qubit_state'])
