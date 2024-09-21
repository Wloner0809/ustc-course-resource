#! /usr/bin/env python3

import torch
from tqdm import tqdm
from torch.nn import CrossEntropyLoss
from torch.autograd import grad

# from torch.autograd.functional import hvp, vhp
from pytorch_influence_functions.utils import display_progress


def s_test(
    z_test,
    t_test,
    model,
    hessian_loader,
    gpu=-1,
    damp=0.01,
    scale=25.0,
    recursion_depth=5000
):
    """s_test can be precomputed for each test point of interest, and then
    multiplied with grad_z to get the desired value for each training point.
    Here, stochastic estimation is used to calculate s_test. s_test is the
    Inverse Hessian Vector Product.

    Arguments:
        z_test: torch tensor, test data points, such as test images
        t_test: torch tensor, contains all test data labels
        model: torch NN, model used to evaluate the dataset
        hessian_loader: torch Dataloader, can load the training dataset,
            the size of dataset is recursion_depth
        gpu: int, GPU id to use if >=0 and -1 means use CPU
        damp: float, dampening factor
        scale: float, scaling factor

    Returns:
        h_estimate: list of torch tensors, s_test"""
    v = grad_z(z_test, t_test, model, gpu)
    h_estimate = v.copy()

    def hvp(y, w, v):
        """Multiply the Hessians of y and w by v.

        Arguments:
            y: scalar/tensor, for example the output of the loss function
            w: list of torch tensors, tensors over which the Hessian
                should be constructed
            v: list of torch tensors, same shape as w,
                will be multiplied with the Hessian

        Returns:
            return_grads: list of torch tensors, contains product of Hessian and v.

        Raises:
            ValueError: `y` and `w` have a different length."""
        if len(w) != len(v):
            raise (ValueError("w and v must have the same length."))
        # First backprop
        first_grads = grad(y, w, retain_graph=True, create_graph=True)
        # Elementwise products
        elemwise_products = 0
        for grad_elem, v_elem in zip(first_grads, v):
            elemwise_products += torch.sum(grad_elem * v_elem)
        # Second backprop
        return_grads = grad(elemwise_products, w, create_graph=True)
        return return_grads

    model.eval()
    for i, (x, t) in tqdm(enumerate(hessian_loader)):
        if gpu >= 0:
            x, t = x.cuda(), t.cuda()
            model = model.cuda()
        x = x.view(-1, 28 * 28)
        # x = x / 255.0
        y = model(x)
        loss = CrossEntropyLoss()(y, t)
        params = [p for p in model.parameters() if p.requires_grad]
        hv = hvp(loss, params, h_estimate)
        # Recursively caclulate h_estimate
        with torch.no_grad():
            h_estimate = [
                _v + (1 - damp) * _h_e - _hv / scale
                for _v, _h_e, _hv in zip(v, h_estimate, hv)
            ]
    display_progress("Calc. s_test recursions: ", i, recursion_depth)
    return h_estimate


def grad_z(z, t, model, gpu=-1):
    """Calculates the gradient z. One grad_z should be computed for each
    training sample.

    Arguments:
        z: torch tensor, training data points
            e.g. an image sample (batch_size, 3, 256, 256)
        t: torch tensor, training data labels
        model: torch NN, model used to evaluate the dataset
        gpu: int, device id to use for GPU, -1 for CPU

    Returns:
        grad_z: list of torch tensor, containing the gradients
            from model parameters to loss"""
    model.eval()
    # initialize
    if gpu >= 0:
        z, t = z.cuda(), t.cuda()
        model = model.cuda()
    z = z.view(-1, 28 * 28)
    # z = z / 255.0
    y = model(z)
    loss = CrossEntropyLoss()(y, t)
    # Compute sum of gradients from model parameters to loss
    params = [p for p in model.parameters() if p.requires_grad]
    return list(grad(loss, params, create_graph=True))
