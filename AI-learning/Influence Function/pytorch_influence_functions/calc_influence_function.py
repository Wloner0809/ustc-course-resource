#! /usr/bin/env python3

import torch
import time
import datetime
import numpy as np
import copy
import logging
from tqdm import tqdm

from torchvision.datasets import MNIST
from torchvision import transforms
from torch.utils.data import DataLoader, RandomSampler
from pathlib import Path
from pytorch_influence_functions.influence_function import s_test, grad_z
from pytorch_influence_functions.utils import save_json, display_progress


def calc_s_test_single(
    model,
    z_test,
    t_test,
    hessian_loader,
    gpu=-1,
    damp=0.01,
    scale=25,
    recursion_depth=5000,
    r=10,
):
    """Calculates s_test for a single test image taking into account the whole
    training dataset. s_test = invHessian * nabla(Loss(test_img, model params))

    Arguments:
        model: pytorch model, for which s_test should be calculated
        z_test: test image
        t_test: test image label
        hessian_loader: pytorch dataloader, which can load the train data
        gpu: int, device id to use for GPU, -1 for CPU (default)
        damp: float, influence function damping factor
        scale: float, influence calculation scaling factor
        recursion_depth: int, number of recursions to perform during s_test
            calculation, increases accuracy. r*recursion_depth should equal the
            training dataset size.
        r: int, number of iterations of which to take the avg.
            of the h_estimate calculation; r*recursion_depth should equal the
            training dataset size.

    Returns:
        s_test_vec: torch tensor, contains s_test for a single test image"""
    # TODO: hessian_loader should be different
    z_test = z_test.view(-1, 28 * 28)
    # z_test = z_test / 255.0
    all = s_test(
        z_test,
        t_test,
        model,
        hessian_loader,
        gpu=gpu,
        damp=damp,
        scale=scale,
        recursion_depth=recursion_depth,
    )
    for i in tqdm(range(1, r)):
        mnist_train = MNIST(
            "./data/train", train=True, download=True, transform=transforms.ToTensor()
        )
        hessian_loader = DataLoader(
            mnist_train,
            sampler=RandomSampler(
                mnist_train, replacement=True, num_samples=recursion_depth
            ),
        )
        current = s_test(
            z_test,
            t_test,
            model,
            hessian_loader,
            gpu=gpu,
            damp=damp,
            scale=scale,
            recursion_depth=recursion_depth,
        )
        all = [i + j for i, j in zip(all, current)]
        display_progress("Averaging r-times: ", i, r)
    s_test_vec = [i / r for i in all]
    return s_test_vec


def calc_s_test(
    model,
    test_loader,
    hessian_loader,
    save=False,
    gpu=-1,
    damp=0.01,
    scale=25,
    recursion_depth=5000,
    r=10,
    start=0,
):
    """Calculates s_test for the whole test dataset taking into account all
    training data images.

    Arguments:
        model: pytorch model, for which s_test should be calculated
        test_loader: pytorch dataloader, which can load the test data
        hessian_loader: pytorch dataloader, which can load the train data
        save: Path, path where to save the s_test files if desired. Omitting
            this argument will skip saving
        gpu: int, device id to use for GPU, -1 for CPU (default)
        damp: float, influence function damping factor
        scale: float, influence calculation scaling factor
        recursion_depth: int, number of recursions to perform during s_test
            calculation, increases accuracy. r*recursion_depth should equal the
            training dataset size.
        r: int, number of iterations of which to take the avg.
            of the h_estimate calculation; r*recursion_depth should equal the
            training dataset size.
        start: int, index of the first test index to use. default is 0

    Returns:
        s_tests: list of torch vectors, contain all s_test for the whole
            dataset. Can be huge.
        save: Path, path to the folder where the s_test files were saved to or
            False if they were not saved."""
    if save and not isinstance(save, Path):
        save = Path(save)
    if not save:
        logging.info("ATTENTION: not saving s_test files.")

    s_tests = []
    for i in tqdm(range(start, len(test_loader.dataset))):
        z_test, t_test = test_loader.dataset[i]
        z_test = test_loader.collate_fn([z_test])
        t_test = test_loader.collate_fn([t_test])

        s_test_vec = calc_s_test_single(
            model, z_test, t_test, hessian_loader, gpu, damp, scale, recursion_depth, r
        )

        if save:
            s_test_vec = [s.cpu() for s in s_test_vec]
            torch.save(
                s_test_vec, save.joinpath(f"{i}_recdep{recursion_depth}_r{r}.s_test")
            )
        else:
            s_tests.append(s_test_vec)
        display_progress(
            "Calc. z_test (s_test): ", i - start, len(test_loader.dataset) - start
        )

    return s_tests, save


def calc_influence_single(
    model,
    hessian_loader,
    train_loader,
    test_loader,
    test_id_num,
    gpu,
    recursion_depth,
    r,
    s_test_vec=None,
    time_logging=False,
):
    """Calculates the influences of all training data points on a single
    test dataset image.

    Arugments:
        model: pytorch model
        hessian_loader: DataLoader, loads the uniformly sampled training dataset
        train_loader: DataLoader, loads the training dataset
        test_loader: DataLoader, loads the test dataset
        test_id_num: int, id of the test sample for which to calculate the
            influence function
        gpu: int, identifies the gpu id, -1 for cpu
        recursion_depth: int, number of recursions to perform during s_test
            calculation, increases accuracy. r*recursion_depth should equal the
            training dataset size.
        r: int, number of iterations of which to take the avg.
            of the h_estimate calculation; r*recursion_depth should equal the
            training dataset size.
        s_test_vec: list of torch tensor, contains s_test vectors. If left
            empty it will also be calculated

    Returns:
        influence: list of float, influences of all training data samples
            for one test sample
        harmful: list of float, influences sorted by harmfulness
        helpful: list of float, influences sorted by helpfulness
        test_id_num: int, the number of the test dataset point
            the influence was calculated for"""
    # Calculate s_test vectors if not provided
    if not s_test_vec:
        z_test, t_test = test_loader.dataset[test_id_num]
        z_test = test_loader.collate_fn([z_test])
        t_test = test_loader.collate_fn([t_test])
        s_test_vec = calc_s_test_single(
            model,
            z_test,
            t_test,
            hessian_loader,
            gpu,
            recursion_depth=recursion_depth,
            r=r,
        )

    # Calculate the influence function
    train_dataset_size = len(train_loader.dataset)
    influences = []
    for i in tqdm(range(train_dataset_size)):
        z, t = train_loader.dataset[i]
        z = train_loader.collate_fn([z])
        t = train_loader.collate_fn([t])
        z = z.view(-1, 28 * 28)
        # z = z / 255.0
        if time_logging:
            time_a = datetime.datetime.now()
        grad_z_vec = grad_z(z, t, model, gpu=gpu)
        if time_logging:
            time_b = datetime.datetime.now()
            time_delta = time_b - time_a
            logging.info(
                f"Time for grad_z iter:" f" {time_delta.total_seconds() * 1000}"
            )
        tmp_influence = (
            -sum([-torch.sum(k * j).data for k, j in zip(s_test_vec, grad_z_vec)])
            / train_dataset_size
        )
        print(tmp_influence)
        influences.append(tmp_influence)
        display_progress("Calc. influence function: ", i, train_dataset_size)

    influence_np = []
    for i in influences:
        influence_np.append(i.cpu().numpy())
    # NOTE: return abs(influences)
    influence_np = np.abs(influence_np)
    max_abs_influence = np.argsort(influence_np)

    return influences, max_abs_influence.tolist(), test_id_num


def calc_img_wise(config, model, hessian_loader, train_loader, test_loader):
    """Calculates the influence function one test point at a time. Calculates
    the `s_test` and `grad_z` values on the fly and discards them afterwards."""

    def get_wrongly_classified_sample(model, test_loader):
        wrong_classified_list = []
        model.eval()
        with torch.no_grad():
            for i in range(len(test_loader.dataset)):
                z, t = test_loader.dataset[i]
                z = test_loader.collate_fn([z])
                t = test_loader.collate_fn([t])
                z = z.view(-1, 28 * 28)
                # z = z / 255.0
                "keep the device consistent with the model's device"
                z = z.to(config["gpu"])
                t = t.to(config["gpu"])
                model = model.to(config["gpu"])
                outputs = model(z)
                _, predicted = torch.max(outputs.data, 1)
                if predicted != t:
                    wrong_classified_list.append(i)
        if len(wrong_classified_list) == 0:
            raise ValueError("No wrongly classified samples found.")
        return np.random.choice(wrong_classified_list)

    influences_meta = copy.deepcopy(config)
    outdir = Path(config["outdir"])
    outdir.mkdir(exist_ok=True, parents=True)
    save_json(
        influences_meta, outdir.joinpath("influence_meta_sgd_retrain.json")
    )

    # get test id
    test_id_num = get_wrongly_classified_sample(model, test_loader)

    influences = {}
    start_time = time.time()
    influence, max_abs_influence, _ = calc_influence_single(
        model,
        hessian_loader,
        train_loader,
        test_loader,
        test_id_num=test_id_num,
        gpu=config["gpu"],
        recursion_depth=config["recursion_depth"],
        r=config["r_averaging"],
    )
    end_time = time.time()

    influences[str(test_id_num)] = {}
    _, label = test_loader.dataset[test_id_num]
    influences[str(test_id_num)]["test_id"] = int(test_id_num)
    influences[str(test_id_num)]["label"] = label
    influences[str(test_id_num)]["time_calc_influence_s"] = end_time - start_time
    infl = [x.cpu().numpy().tolist() for x in influence]
    influences[str(test_id_num)]["influence"] = infl
    influences[str(test_id_num)]["max_abs_influence_id"] = max_abs_influence[-500:]
    influences[str(test_id_num)]["max_abs_influence"] = [
        infl[i] for i in max_abs_influence[-500:]
    ]

    save_json(
        influences, outdir.joinpath("influence_results_sgd_retrain.json")
    )
    logging.info(f"The results for this run are:")
    logging.info("Influences: ")
    logging.info(influence[:3])
    logging.info("Most large abs_influence img IDs: ")
    logging.info(max_abs_influence[-3:])

    return influences, test_id_num
