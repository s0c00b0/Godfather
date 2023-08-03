'''Generates reads after reading through the thread.'''

import torch
import torch.nn as nn

class Reader(nn.Module):
    
    def __init__(self, model) -> None:
        super().__init__()
        
        