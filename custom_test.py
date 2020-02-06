from options.test_options import TestOptions
from data import CreateDataLoader
from models import create_model

import matplotlib.pyplot as plt

if __name__ == "__main__":
    opt = TestOptions().parse()
    opt.nThreads = 1   # test code only supports nThreads = 1
    opt.batchSize = 1  # test code only supports batchSize = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    opt.display_id = -1  # no visdom display
    opt.nThreads = 1
    opt.dataroot = "datasets/cbct2ct"
    opt.input_nc = 1
    opt.output_nc = 1
    opt.dataset_mode = "cbct2ct"
    opt.model = "cycle_gan"
    
    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()
    model = create_model(opt)
    model.setup(opt)
    
    for data in dataset:
        model.set_input(data)
        model.test()
        
        fig = plt.figure()
        axes = fig.subplots(1, 4)
        
        visuals = model.get_current_visuals()
        axes[0].imshow(visuals["experiment_name_real_A"].detach().numpy()[0,0])
        axes[1].imshow(visuals["experiment_name_real_B"].detach().numpy()[0,0])
        axes[2].imshow(visuals["experiment_name_fake_A"].detach().numpy()[0,0])
        axes[3].imshow(visuals["experiment_name_fake_B"].detach().numpy()[0,0])
        break
        
        
        