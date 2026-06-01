"""
Buggy NON-MODULAR snippet from keras, bug ID 40.
"""
def buggy_function(rs, data, freq=None):
            output_dim = self.cell.state_size[0]
                output_dim = self.cell.state_size
                state_shape = [(input_shape[0], output_dim) for _ in self.states]
    return rs
