from toric_matching.toric_code import manhattan_distance, ToricCode
import networkx as nx


def test_manhattan_distance():
    vertex_pairs = [((0, 0), (2, 2)), ((1, 1, 1), (0, 2, 4)),
                    ((0, 1, 2, 3), (3, 3, 3, 3))]
    ls = [3, 5, 4]
    distances = [2, 4, 4]
    for i in range(len(vertex_pairs)):
        assert(manhattan_distance(
            vertex_pairs[i][0], vertex_pairs[i][1], ls[i]) == distances[i])


def test_calculate_syndrome():
    for l in [3, 5]:
        # 2D test
        code = ToricCode(2, l)
        # Single qubit error
        code.lattice[(0, 0)][(0, 1)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0) or node == (0, 1):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Two qubit error
        code.lattice[(0, 1)][(1, 1)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0) or node == (1, 1):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Stabilizer error
        code.lattice[(0, 0)][(1, 0)]['qubit_state'] = 1
        code.lattice[(1, 0)][(1, 1)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            assert(code.lattice.node[node]['stabilizer_value'] == 0)

        # 3D test
        code = ToricCode(3, l)
        # Single qubit error
        code.lattice[(1, 1, 1)][(1, 1, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (1, 1, 1) or node == (1, 1, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Two qubit error
        code.lattice[(1, 1, 2)][(1, 2, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (1, 1, 1) or node == (1, 2, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Stabilizer error
        code.lattice[(1, 1, 1)][(1, 2, 1)]['qubit_state'] = 1
        code.lattice[(1, 2, 1)][(1, 2, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            assert(code.lattice.node[node]['stabilizer_value'] == 0)

        # 4D test
        code = ToricCode(4, l)
        # Single qubit error
        code.lattice[(0, 0, 0, 2)][(0, 0, 1, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0, 0, 2) or node == (0, 0, 1, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Two qubit error
        code.lattice[(0, 0, 1, 2)][(0, 1, 1, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0, 0, 2) or node == (0, 1, 1, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Stabilizer error
        code.lattice[(0, 1, 0, 2)][(0, 1, 1, 2)]['qubit_state'] = 1
        code.lattice[(0, 0, 0, 2)][(0, 1, 0, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            assert(code.lattice.node[node]['stabilizer_value'] == 0)


def test_generate_errors():
    code = ToricCode(4, 3)
    code.generate_errors(1)
    for edge in code.lattice.edges():
        assert(code.lattice[edge[0]][edge[1]]['qubit_state'] == 1)

    code = ToricCode(3, 5)
    code.generate_errors(0)
    for edge in code.lattice.edges():
        assert(code.lattice[edge[0]][edge[1]]['qubit_state'] == 0)


def test_build_matching_graph():
    code = ToricCode(2, 9)
    code.lattice.nodes[(1, 0)]['stabilizer_value'] = 1
    code.lattice.nodes[(4, 5)]['stabilizer_value'] = 1
    code.lattice.nodes[(7, 7)]['stabilizer_value'] = 1
    code.lattice.nodes[(6, 4)]['stabilizer_value'] = 1

    code.build_matching_graph()
    assert(len(code.matching_graph.nodes()) == 4)
    assert((1, 0) in code.matching_graph.nodes())
    assert((4, 5) in code.matching_graph.nodes())
    assert((7, 7) in code.matching_graph.nodes())
    assert((6, 4) in code.matching_graph.nodes())
    assert(len(code.matching_graph.edges()) == 6)
    assert(code.matching_graph[(1, 0)][(4, 5)]['weight'] == -7)
    assert(code.matching_graph[(1, 0)][(7, 7)]['weight'] == -5)
    assert(code.matching_graph[(1, 0)][6, 4]['weight'] == -8)
    assert(code.matching_graph[(4, 5)][(7, 7)]['weight'] == -5)
    assert(code.matching_graph[(4, 5)][(6, 4)]['weight'] == -3)
    assert(code.matching_graph[(7, 7)][(6, 4)]['weight'] == -4)


def test_apply_correction():
    code = ToricCode(4, 3)
    code.lattice[(1, 0, 0, 0)][(1, 0, 0, 1)]['qubit_state'] = 1
    code.lattice[(1, 0, 0, 0)][(1, 1, 0, 0)]['qubit_state'] = 1
    code.lattice[(1, 0, 0, 1)][(1, 1, 0, 1)]['qubit_state'] = 1
    code.calculate_syndrome()
    code.build_matching_graph()
    code.apply_correction()
    assert(code.lattice[(1, 0, 0, 0)][(1, 0, 0, 1)]['qubit_state'] == 1)
    assert(code.lattice[(1, 0, 0, 0)][(1, 1, 0, 0)]['qubit_state'] == 1)
    assert(code.lattice[(1, 0, 0, 1)][(1, 1, 0, 1)]['qubit_state'] == 1)
    assert(code.lattice[(1, 1, 0, 0)][(1, 1, 0, 1)]['qubit_state'] == 1)


def test_build_logicals():
    ls = [3, 5]
    dims = [2, 3, 4]
    for l in ls:
        for dim in dims:
            code = ToricCode(dim, l)
            assert(len(code.logicals) == dim)
            for logical in code.logicals:
                assert(len(logical) == l ** (dim - 1))


def test_check_correction():
    code = ToricCode(2, 3)
    # Z1 error
    code.lattice[(0, 0)][(1, 0)]['qubit_state'] = 1
    code.lattice[(1, 0)][(2, 0)]['qubit_state'] = 1
    code.lattice[(2, 0)][(0, 0)]['qubit_state'] = 1
    code.calculate_syndrome()
    for node in code.lattice.nodes():
        assert(code.lattice.node[node]['stabilizer_value'] == 0)
    assert(code.check_correction() == False)
    # Z2 error
    code.lattice[(0, 0)][(1, 0)]['qubit_state'] = 0
    code.lattice[(1, 0)][(2, 0)]['qubit_state'] = 0
    code.lattice[(2, 0)][(0, 0)]['qubit_state'] = 0
    code.lattice[(0, 0)][(0, 1)]['qubit_state'] = 1
    code.lattice[(0, 1)][(0, 2)]['qubit_state'] = 1
    code.lattice[(0, 2)][(0, 0)]['qubit_state'] = 1
    code.calculate_syndrome()
    for node in code.lattice.nodes():
        assert(code.lattice.node[node]['stabilizer_value'] == 0)
    assert(code.check_correction() == False)

    code = ToricCode(4, 3)
    # Z4 error
    code.lattice[(0, 0, 0, 0)][(0, 0, 0, 1)]['qubit_state'] = 1
    code.lattice[(0, 0, 0, 1)][(0, 0, 0, 2)]['qubit_state'] = 1
    code.lattice[(0, 0, 0, 2)][(0, 0, 1, 2)]['qubit_state'] = 1
    code.lattice[(0, 0, 1, 2)][(0, 0, 1, 0)]['qubit_state'] = 1
    code.lattice[(0, 0, 1, 0)][(0, 0, 0, 0)]['qubit_state'] = 1
    code.calculate_syndrome()
    for node in code.lattice.nodes():
        assert(code.lattice.node[node]['stabilizer_value'] == 0)
    assert(code.check_correction() == False)

    code = ToricCode(3, 5)
    # Stabilizer error
    code.lattice[(2, 2, 2)][(2, 2, 3)]['qubit_state'] = 1
    code.lattice[(2, 2, 2)][(2, 3, 2)]['qubit_state'] = 1
    code.lattice[(2, 2, 3)][(2, 3, 3)]['qubit_state'] = 1
    code.lattice[(2, 3, 2)][(2, 3, 3)]['qubit_state'] = 1
    code.calculate_syndrome()
    assert(code.check_correction() == True)


def test_decoding():
    # Toric code should correct any weight <= sqrt(l) error
    dims = [2, 3, 4]
    for dim in dims:
        code = ToricCode(dim, 3)
        for edge in code.lattice.edges():
            nx.set_edge_attributes(code.lattice, 0, 'qubit_state')
            code.lattice[edge[0]][edge[1]]['qubit_state'] = 1
            code.calculate_syndrome()
            code.build_matching_graph()
            code.apply_correction()
            assert(code.check_correction() == True)

    code = ToricCode(2, 5)
    for edge_i in code.lattice.edges():
        for edge_j in code.lattice.edges():
            if edge_i == edge_j:
                continue
            nx.set_edge_attributes(code.lattice, 0, 'qubit_state')
            code.lattice[edge_i[0]][edge_i[1]]['qubit_state'] = 1
            code.lattice[edge_j[0]][edge_j[1]]['qubit_state'] = 1
            code.calculate_syndrome()
            code.build_matching_graph()
            code.apply_correction()
            assert(code.check_correction() == True)
