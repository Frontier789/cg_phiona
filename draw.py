class draw:
    def __init__(self, vao, vert_count, Ka = None, Kd = None, Ks = None):
        self.vao = vao
        self.vert_count = vert_count
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks