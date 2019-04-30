import data_generator

ls = [9, 13, 17, 23]
dim = 3
ps = [0.01, 0.02, 0.03, 0.04, 0.05]
trials = 100

for l in ls:
    for p in ps:
        data_generator.generate_data(dim, l, p, trials)
        