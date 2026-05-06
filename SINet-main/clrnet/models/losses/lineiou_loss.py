import torch

def line_iou(pred, target, img_w, length=15, aligned=True):
    '''
    Calculate the line iou value between predictions and targets
    Args:
        pred: lane predictions, shape: (num_pred, 72)
        target: ground truth, shape: (num_target, 72)
        img_w: image width
        length: extended radius
        aligned: True for iou loss calculation, False for pair-wise ious in assign
    '''
    px1 = pred - length
    px2 = pred + length
    tx1 = target - length
    tx2 = target + length
    if aligned:
        invalid_mask = target
        ovr = torch.min(px2, tx2) - torch.max(px1, tx1)
        union = torch.max(px2, tx2) - torch.min(px1, tx1)
    else:
        num_pred = pred.shape[0]
        invalid_mask = target.repeat(num_pred, 1, 1)
        ovr = (torch.min(px2[:, None, :], tx2[None, ...]) -
               torch.max(px1[:, None, :], tx1[None, ...]))
        union = (torch.max(px2[:, None, :], tx2[None, ...]) -
                 torch.min(px1[:, None, :], tx1[None, ...]))

    invalid_masks = (invalid_mask < 0) | (invalid_mask >= img_w)
    ovr[invalid_masks] = 0.
    union[invalid_masks] = 0.
    iou = ovr.sum(dim=-1) / (union.sum(dim=-1) + 1e-9)
    return iou


def angle_loss(pred, target, img_h):

    x_pred = pred  
    x_target = target
    
    num_points = x_pred.shape[1]
    y = torch.linspace(0, img_h - 1, steps=num_points).to(pred.device)  

    #delta_x_pred = x_pred[:, 1:] - x_pred[:, [0]]  
    #delta_x_target = x_target[:, 1:] - x_target[:, [0]]  
    #delta_y = y[1:] - y[0]
    
    delta_x_pred = x_pred[:, 24:] - x_pred[:, [0]]  
    delta_x_target = x_target[:, 24:] - x_target[:, [0]]
    delta_y = y[24:] - y[0]

    angles_pred = torch.atan2(delta_y, delta_x_pred) 
    angles_target = torch.atan2(delta_y, delta_x_target)  

    angle_diff = angles_pred - angles_target  
    angle_diff = torch.atan2(torch.sin(angle_diff), torch.cos(angle_diff))
    angle_loss = (angle_diff ** 2).mean() 

    return angle_loss


def liou_loss(pred, target, img_w, img_h, length=15):
    return (1 - line_iou(pred, target, img_w, length)).mean() + 0.03 * angle_loss(pred, target, img_h)