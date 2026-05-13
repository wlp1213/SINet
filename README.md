# SINet

## Installation
Code implementation for the paper "Structure-Guided Feature Fusion and Geometric Angle Supervision for Robust Lane Detection", to be published in *The Visual Computer*.
### Prerequisites

Only tested on Ubuntu 18.04 and 20.04 with:

- Python >= 3.8 (tested with Python 3.8)
- PyTorch >= 1.6 (tested with PyTorch 1.6)
- CUDA (tested with CUDA 10.2)
- Other dependencies described in `requirements.txt`

### Clone this repository
Clone this code to your workspace.
```bash
https://github.com/wlp1213/SINet
```

### Create a conda virtual environment and activate it (conda is optional)
```bash
conda create -n clrnet python=3.8 -y
conda activate clrnet
```

### Install dependencies
```bash
conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
pip install torch==1.8.0 torchvision==0.9.0
python setup.py build develop
```

### Data preparation
```bash
the Data Availability section of the reference paper
```

### Training
```bash
python main.py [configs/path_to_your_config] --gpus [gpu_num]
```

### Validation
```bash
python main.py [configs/path_to_your_config] --[test|validate] --load_from [path_to_your_model] --gpus [gpu_num]
```
Currently, this code can output the visualization result when testing, just add --view. We will get the visualization result in work_dirs/xxx/xxx/visualization.
