
#create dictionary for hyperparameters
#following Sumana's recommendations


params =  {
    
    #256, 256, 1
    'conv1': {
        'in_channel': 1,
#         'in_channel': 3,   #to change depending on input
        'out_channel': 8,
        'kernel_size': 5,
        'stride': 1
    },
    #254, 254, 8 
    'conv2': {
        'in_channel': 8, #refer to conv1_out_channel
        'out_channel': 16,
        'kernel_size': 5,
        'stride': 1
    },
    #252, 252, 16
    'conv3': {
        'in_channel': 16, #refer to conv1_out_channel
        'out_channel': 32,
        'kernel_size': 5,
        'stride': 1
    },
    #250, 250, 32
    'conv4': {
        'in_channel': 32, #refer to conv1_out_channel
        'out_channel': 64,
        'kernel_size': 5,
        'stride': 1
    },
    #248, 248, 64
    'conv5': {
        'in_channel': 64, #refer to conv1_out_channel
        'out_channel': 128,
        'kernel_size': 5,
        'stride': 1
    },
    'conv6': {
        'in_channel': 128, #refer to conv1_out_channel
        'out_channel': 128,
        'kernel_size': 5,
        'stride': 1
    },
    #12, 12, 128
    #maxpoll
    #6, 6, 128
    
}