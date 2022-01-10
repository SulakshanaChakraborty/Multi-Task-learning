from sklearn.metrics import jaccard_score,f1_score
import torch
import numpy as np
from metrics import eval_metrics

def evaluate_model_on_data(test_loader, model, device, loss_criterion, model_name=""):
    # todo: implement test scheme.
    test_loss = []
    test_accuracy = []
    test_iou = []
    test_bbox_loss = []
    test_segmentation_loss = []
    test_label_loss = []
    test_jaca = []
    test_f1_arr = []

    # Evaluate model
    # Compute Testing metrics
    for i, batch_data in enumerate(test_loader, 1):
        # TODO: recognise denoiing, colour,
        #TODO recognise the metrics for which model
        with torch.no_grad():
            inputs, labels = batch_data
            inputs = inputs.to(device)
            mask = torch.squeeze(labels['mask'].to(device))
            mask = mask.to(torch.long)
            binary = torch.squeeze(labels['classification'].to(device))
            binary = binary.to(torch.long)
            bbox = labels['bbox'].to(device)
            bbox = bbox.float()
    
            classes, boxes, segmask = model(inputs)

            loss, labels_loss, segmentation_loss, bboxes_loss = loss_criterion(input_labels=classes,
                                                                               input_segmentations=segmask, \
                                                                               input_bboxes=boxes, target_labels=binary,
                                                                               target_segmentations=mask,
                                                                               target_bboxes=bbox)

            pred_ax = np.argmax(classes.detach().cpu().numpy(), axis=1)
            test_accuracy.append(np.sum((binary.detach().cpu().numpy() == pred_ax).astype(int)) / len(binary))
            test_loss.append(loss.item())

            test_label_loss.append(labels_loss.data.item())
            test_segmentation_loss.append(segmentation_loss.data.item())
            target_segmentation = torch.argmax(segmask, 1)

            test_mask_array = np.array(mask.cpu()).ravel()
            test_predicted_array = np.array(target_segmentation.cpu().ravel())

            iou = (eval_metrics(mask.cpu(), target_segmentation.cpu(), 2))
            #  print(round(iou.item(),3),"iou")

            test_jac = jaccard_score(test_mask_array, test_predicted_array, average='weighted')
            val_f1 = f1_score(test_mask_array, test_predicted_array)

            test_jaca.append(test_jac)
            test_f1_arr.append(val_f1)

            test_iou.append(iou.item())
          
            test_bbox_loss.append(bboxes_loss.data.item())
          

    print("-----------------------Testing Metrics-------------------------------------------")
    file = open("output.txt", "a")
    print("Model Name: "+str(model_name),file=file)
    print("Loss: ", round(np.mean(test_loss), 3), "Test Accu: ", round(np.mean(test_accuracy), 3), file=file)
    print("IOU: ", round(np.mean(test_iou), 3), file=file)
    print("BBOX-loss: ", round(np.mean(test_bbox_loss), 3), file=file)
    print("Segmnetaiton-loss", round(np.mean(test_segmentation_loss), 3), file=file)
    print("Label-loss", round(np.mean(test_label_loss), 3), file=file)
    print("Jac", round(np.mean(test_jaca), 3), file=file)
    print("F1s", round(np.mean(test_f1_arr), 3), file=file)
    file.close()
    # loss = 1
    # metrics = 2
    # return loss, metrics

    #if its segnet,

