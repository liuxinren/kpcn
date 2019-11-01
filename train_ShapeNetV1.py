# Common libs
import time
import os
import sys

# Custom libs
from utils.config import Config
# from utils.trainer import ModelTrainer
# from models.KPFCNN_model import KernelPointFCNN

# Dataset
from datasets.ShapeNetV1 import ShapeNetV1Dataset


# ----------------------------------------------------------------------------------------------------------------------
#
#           Config Class
#       \******************/
#


class ShapeNetV1Config(Config):
    """
    Override the parameters you want to modify for this dataset
    """

    ####################
    # Dataset parameters
    ####################

    # Dataset name
    dataset = 'ShapeNetV1'

    # Number of categories in the dataset (This value is overwritten by dataset class when initiating input pipeline).
    num_categories = None

    # Type of task performed on this dataset (also overwritten)
    network_model = None

    # Number of CPU threads for the input pipeline
    input_threads = 8

    #########################
    # Architecture definition
    #########################

    # Define layers
    architecture = ['simple',
                    'resnetb',
                    'resnetb_strided',
                    'resnetb',
                    'resnetb_strided',
                    'resnetb_deformable',
                    'resnetb_deformable_strided',
                    'resnetb_deformable',
                    'resnetb_deformable_strided',
                    'resnetb_deformable',
                    'nearest_upsample',
                    'unary',
                    'nearest_upsample',
                    'unary',
                    'nearest_upsample',
                    'unary',
                    'nearest_upsample',
                    'unary']

    # KPConv specific parameters
    num_kernel_points = 15
    first_subsampling_dl = 0.02

    # Density of neighborhoods for deformable convs (which need bigger radiuses). For normal conv we use KP_extent
    density_parameter = 5.0

    # Influence function of KPConv in ('constant', 'linear', gaussian)
    KP_influence = 'linear'
    KP_extent = 1.0

    # Aggregation function of KPConv in ('closest', 'sum')
    convolution_mode = 'sum'

    # Can the network learn modulations in addition to deformations
    modulated = False

    # Offset loss
    # 'permissive' only constrains offsets inside the big radius
    # 'fitting' helps deformed kernels to adapt to the geometry by penalizing distance to input points
    offsets_loss = 'fitting'
    offsets_decay = 0.1

    # Choice of input features
    in_features_dim = 4

    # Batch normalization parameters
    use_batch_norm = True
    batch_norm_momentum = 0.98

    #####################
    # Training parameters
    #####################

    # Maximal number of epochs
    max_epoch = 500

    # Learning rate management
    learning_rate = 1e-2
    momentum = 0.98
    lr_decays = {i: 0.1 ** (1 / 80) for i in range(1, max_epoch)}
    grad_clip_norm = 100.0

    # Number of batch
    batch_num = 16

    # Number of steps per epochs (cannot be None for this dataset)
    epoch_steps = None

    # Number of validation examples per epoch
    validation_size = 50

    # Number of epoch between each snapshot
    snapshot_gap = 50

    # Augmentations
    augment_scale_anisotropic = True
    augment_symmetries = [False, False, False]
    augment_rotation = 'none'
    augment_scale_min = 0.9
    augment_scale_max = 1.1
    augment_noise = 0.001
    augment_occlusion = 'none'

    # Whether to use loss averaged on all points, or averaged per batch.
    batch_averaged_loss = False

    # Do we nee to save convergence
    saving = True
    saving_path = None


# ----------------------------------------------------------------------------------------------------------------------
#
#           Main Call
#       \***************/
#


if __name__ == '__main__':
    ##########################
    # Initiate the environment
    ##########################

    # Choose which gpu to use
    GPU_ID = '0'

    # Set GPU visible device
    os.environ['CUDA_VISIBLE_DEVICES'] = GPU_ID

    # Enable/Disable warnings (set level to '0'/'3')
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

    ###########################
    # Load the model parameters
    ###########################

    config = ShapeNetV1Config()

    ##############
    # Prepare Data
    ##############

    print()
    print('Dataset Preparation')
    print('*******************')

    # Create sub-sampled input clouds
    dataset = ShapeNetV1Dataset()
    dl0 = 0.02
    dataset.load_subsampled_clouds(dl0)

    # Initialize input pipelines
    dataset.init_input_pipeline(config)
