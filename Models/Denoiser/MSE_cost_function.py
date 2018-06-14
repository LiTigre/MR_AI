import torch.nn as nn




def cost_function(prediction, target):
	criterion = nn.MSELoss()
    loss = criterion(prediction, target)
    return loss