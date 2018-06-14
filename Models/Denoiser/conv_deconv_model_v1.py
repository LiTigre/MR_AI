#import the params dictionary
import torch.nn as nn



class ConvNet(nn.Module):
    def __init__(self):
      
        super(ConvNet, self).__init__()
        
        # Convolution layers
        # torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True)[source]
        self.conv1 = nn.Conv2d(in_channels = params1['conv1']['in_channel'], 
                               out_channels = params1['conv1']['out_channel'], 
                               kernel_size = params1['conv1']['kernel_size'], 
                               stride=params1['conv1']['stride'])
        
        self.batch1 = nn.BatchNorm2d(params1['conv1']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv2 = nn.Conv2d(in_channels = params1['conv2']['in_channel'], 
                               out_channels = params1['conv2']['out_channel'], 
                               kernel_size = params1['conv2']['kernel_size'], 
                               stride=params1['conv2']['stride'])
        
        self.batch2 = nn.BatchNorm2d(params1['conv2']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv3 = nn.Conv2d(in_channels = params1['conv3']['in_channel'], 
                               out_channels = params1['conv3']['out_channel'], 
                               kernel_size = params1['conv3']['kernel_size'], 
                               stride=params1['conv3']['stride'])
        
        self.batch3 = nn.BatchNorm2d(params1['conv3']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv4 = nn.Conv2d(in_channels = params1['conv4']['in_channel'], 
                               out_channels = params1['conv4']['out_channel'], 
                               kernel_size = params1['conv4']['kernel_size'], 
                               stride=params1['conv4']['stride'])

        self.batch4 = nn.BatchNorm2d(params1['conv4']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv5 = nn.Conv2d(in_channels = params1['conv5']['in_channel'], 
                               out_channels = params1['conv5']['out_channel'], 
                               kernel_size = params1['conv5']['kernel_size'], 
                               stride=params1['conv5']['stride'])
        
        self.batch5 = nn.BatchNorm2d(params1['conv5']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
     
        self.conv6 = nn.Conv2d(in_channels = params1['conv6']['in_channel'], 
                               out_channels = params1['conv6']['out_channel'], 
                               kernel_size = params1['conv6']['kernel_size'], 
                               stride=params1['conv6']['stride'])
        
        self.batch6 = nn.BatchNorm2d(params1['conv6']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
     

        self.unconv1 = nn.ConvTranspose2d(in_channels = params1['conv6']['out_channel'], 
                                           out_channels = params1['conv6']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv2 = nn.ConvTranspose2d(in_channels = params1['conv5']['out_channel'], 
                                           out_channels = params1['conv5']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv3 = nn.ConvTranspose2d(in_channels = params1['conv4']['out_channel'], 
                                           out_channels = params1['conv4']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv4 = nn.ConvTranspose2d(in_channels = params1['conv3']['out_channel'], 
                                           out_channels = params1['conv3']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv5 = nn.ConvTranspose2d(in_channels = params1['conv2']['out_channel'], 
                                           out_channels = params1['conv2']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv6 = nn.ConvTranspose2d(in_channels = params1['conv1']['out_channel'], 
                                           out_channels = params1['conv1']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        


        # Pooling layers
        #class torch.nn.MaxPool2d(kernel_size, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False)
        self.max2d = nn.MaxPool2d(kernel_size= 2)
        # class torch.nn.AvgPool2d(kernel_size, stride=None, padding=0, ceil_mode=False, count_include_pad=True)
        self.avgpool2d = nn.AvgPool2d(kernel_size = 2)
        
        # Non-linear activations
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax()
        self.sigmoid = nn.Sigmoid()
        
        for m in self.modules():
          if isinstance(m, nn.Conv2d):
            nn.init.xavier_uniform(m.weight.data)
            nn.init.constant(m.bias.data, 0.01)
          elif isinstance(m, nn.Linear):
            nn.init.xavier_uniform(m.weight.data)
            nn.init.constant(m.bias.data, 0.01)
         
          

    def forward(self, x):
        # out = self.relu(self.conv1(x))
        # out = self.relu(self.conv2(out))
        # out = self.relu(self.conv3(out))
        # out = self.relu(self.conv4(out))
        # out = self.relu(self.conv5(out))
        # out = self.relu(self.conv6(out))

        # out = x/255
        out = self.relu(self.batch1(self.conv1(x)))
        out = self.relu(self.batch2(self.conv2(out)))
        out = self.relu(self.batch3(self.conv3(out)))
        out = self.relu(self.batch4(self.conv4(out)))
        out = self.relu(self.batch5(self.conv5(out)))
        out = self.relu(self.batch6(self.conv6(out)))
        # print(out.shape)
        out = self.relu(self.unconv1(out))
        out = self.relu(self.unconv2(out))
        out = self.relu(self.unconv3(out))
        out = self.relu(self.unconv4(out))
        out = self.relu(self.unconv5(out))
        out = self.relu(self.unconv6(out))
        # print(out.shape)
        out = self.sigmoid(out)
        return out




