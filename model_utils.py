import sys
import torch
import pt_networks
import torch.optim as optim
import losses
import pt_networks.segnet
import pt_networks.SegNet_Attnt
import pt_networks.SegNet_Attnt_reformat
import pt_networks.segnet_opencv_filters
import torchvision.models as models

import pt_networks.unet


def get_model(model_type, device='cpu', load_pre_trained_weights=False):
    if model_type == 'baseline':
        model = pt_networks.segnet.Segnet().to(device)
        vgg16 = models.vgg16(pretrained=True).to(device)
        model.vgg16_init(vgg16)
        if load_pre_trained_weights:
            model.load_state_dict(torch.load('Segnet3task3layer.pt'))
        optimizer = optim.Adam(model.parameters(), lr=5e-6)  # todo: update
        loss_fn = losses.BaselineLoss(True, True, True)

    elif model_type == 'baseline_unet':
        model = pt_networks.unet.UNet().to(device)
        optimizer = optim.Adam(model.parameters(), lr=0.00001)
        loss_fn = losses.BaselineLoss(flag_labels=False, flag_segmentations=True, flag_bboxes=False)

    elif model_type == 'mlt_attention':
        model = pt_networks.SegNet_Attnt_reformat.SegNet().to(device)
        vgg16 = models.vgg16(pretrained=True).to(device)
        model.vgg_pretrained(vgg16)
        optimizer = optim.Adam(model.parameters(), lr=1e-3)
        loss_fn = losses.BaselineLoss(True, True, True)  # todo: update

    elif model_type == 'opencv_filter':
        model = pt_networks.segnet_opencv_filters.SegnetOpencv().to(device)
        vgg16 = models.vgg16(pretrained=True).to(device)
        model.vgg16_init(vgg16)
        if load_pre_trained_weights:
            model.load_state_dict(torch.load('Segnet3task3layer.pt'))
        optimizer = optim.Adam(model.parameters(), lr=5e-6)  # todo: update
        loss_fn = losses.OpencvFilterLoss(flag_labels=True, flag_segmentations=True, flag_bboxes=True,
                                          flag_filters=True)

    elif model_type == 'mlt_hard':
        model, optimizer, loss_fn = 1, 2, 3  # todo: update

    elif model_type == 'mlt_gscnn':
        model, optimizer, loss_fn = pt_networks.GSCNN(), 2, 3  # todo: update
    else:
        sys.exit(f'Model Type: {model_type} is not implemented.')

    return model, optimizer, loss_fn


def load_model(model_path):
    model = 1  # todo: update
    return model


def save_model(model, model_path):
    # todo: save model
    pass
