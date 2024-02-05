# YOLaT-VectorGraphicsRecognition
  
[![arXiv](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/abs/2111.03281)

Разработка базируется на [реализации](https://github.com/microsoft/YOLaT-VectorGraphicsRecognition) нейронной сети, описанной в статье ["Распознавание векторной графики без растеризации"](https://arxiv.org/abs/2111.03281).

## 1. Окружение для запуска
1. Подготовить linux-окружение для работы с PyTorch+CUDA по [инструкции](https://github.com/FahimFBA/CUDA-WSL2-Ubuntu).
2. Оптимизировать CUDA для работы с конкретными видеокартами с помощью команды
`export TORCH_CUDA_ARCH_LIST="6.1"`  
Выбрать версию по [таблице](https://stackoverflow.com/questions/68496906/pytorch-installation-for-different-cuda-architectures).
3. Установить все необходимые зависимости:  
`pip3 install torch torchvision torchaudio matplotlib thop fvcore h5py torch_geometric torch_scatter torch_sparse torch_cluster torch_spline_conv tensorboard requests tqdm ogb svgpathtools opencv-python`

## 2. Запуск
Все команды можно запускать дебаггером Visual Studio Code. Команды, представленные ниже, прописаны в конфигурационном файле `.vscode/launch.json`

### 2.1. Загрузка датасетов
Можно проверить работоспособность сети на двух датасетах:

#### Floorplans
- DСкачать и распаковать [Floorplans dataset](http://mathieu.delalandre.free.fr/projects/sesyd/symbols/floorplans.html) в папку `data/FloorPlansGraph5_iter`
- Запустить скрипт для предварительной обработки датасета.  
`python utils/svg_utils/build_graph_bbox.py`

#### Diagrams
- Скачать и распаковать [Diagrams dataset](http://mathieu.delalandre.free.fr/projects/sesyd/symbols/diagrams.html) в папку `data/diagrams`
- Запустить скрипт для предварительной обработки датасета.  
`python utils/svg_utils/build_graph_bbox_diagram.py`

### 2.2. Обучение

#### Floorplans
```sh
CUDA_VISIBLE_DEVICES=0 python -u cad_recognition/train.py --batch_size 4 --data_dir data/FloorPlansGraph5_iter --phase train --lr 2.5e-4 --lr_adjust_freq 9999999999999999999999999999999999999 --in_channels 5 --n_blocks 2 --n_blocks_out 2 --arch centernet3cc_rpn_gp_iter2  --graph bezier_cc_bb_iter --data_aug true  --weight_decay 1e-5 --postname run182_2 --dropout 0.0 --do_mixup 0 --bbox_sampling_step 10
```
#### Diagrams
```sh
CUDA_VISIBLE_DEVICES=0 python -u cad_recognition/train.py --batch_size 4 --data_dir data/diagrams --phase train --lr 2.5e-4 --lr_adjust_freq 9999999999999999999999999999999999999 --in_channels 5 --n_blocks 2 --n_blocks_out 2 --arch centernet3cc_rpn_gp_iter2  --graph bezier_cc_bb_iter --data_aug true  --weight_decay 1e-5 --postname run182_2 --dropout 0.0 --do_mixup 0 --bbox_sampling_step 5
```