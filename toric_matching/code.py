from abc import ABC, abstractmethod


class Code(ABC):

    def __init__(self, dim, l):
        self.dim = dim
        self.l = l

    @abstractmethod
    def calculate_syndrome(self):
        pass

    @abstractmethod
    def generate_errors(self, p):
        pass

    @abstractmethod
    def build_matching_graph(self):
        pass

    @abstractmethod
    def apply_correction(self):
        pass

    @abstractmethod
    def check_correction(self):
        pass

    @abstractmethod
    def clear_errors(self):
        pass

    def one_run(self, p):
        self.generate_errors(p)
        self.calculate_syndrome()
        self.build_matching_graph()
        self.apply_correction()
        result = self.check_correction() 
        self.clear_errors()
        return result
