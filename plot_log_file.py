import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import re
import os
from os.path import join as opj

enums = {
    'Loss': 0,
    'Recon_loss': 1,
    'Margin_loss': 2,
    'Flow_loss': 3,
    'Grad_loss': 4,
    'PSNR': 5,
    'AUC': 6
}
enums_reverse = {
    0: 'Loss',
    1: 'Recon_loss',
    2: 'Margin_loss',
    3: 'Flow_loss',
    4: 'Grad_loss',
    5: 'PSNR',
    6: 'AUC'
}
tolerate = 0

def parse_loss(losses):
    loss_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
    # pattern = r'\[P\] Iteration \[(\d{1})/\d{1}\] in Epoch (\d{1}), Loss:(\d{1}\.\d{4}), Recon:(\d{1}\.\d{4}), Margin:(\d{1}\.\d{4}),Flow:(\d{1}\.\d{4}), Grad:(\d{1}\.\d{4}), PSNR:(\d{1}\.\d{4}), in \d{1}m:\d{1}s'
    # pattern = r'\[P\] Iteration \[\d+\/\d+\] in Epoch \d+, Loss:(\d+[.]\d+), Recon:(\d+[.]\d+), Margin:(\d+[.]\d+),Flow:(\d+[.]\d+), Grad:(\d+[.]\d+), PSNR:(\d+[.]\d+), in \d+m:\d+s'
    pattern = 'some pattern to match'
    for los in losses:
        matching = re.match(pattern, los)
        for cnt in range(1,7):
            loss_dict[cnt-1].append(float(matching.group(cnt)))
    return loss_dict

def parse_auc(aucs):
    auc_dict = {6: []}
    pattern = r'\[P\] AUC for epoch \d+ is (\d+[.]\d+) in \d+m:\d+s'
    for auc in aucs:
        matching = re.match(pattern, auc)
        auc_dict[6].append(float('{:.4f}'.format(float(matching.group(1)))))
    return auc_dict

def get_dict(root):
    log_path = opj(root, 'log.txt')

    with open(log_path, 'r') as f:
        data = f.readlines()
    loss_lst = []
    auc_lst = []
    for da in data:
        if da.startswith('[P] Iteration'):
            loss_lst.append(da)
        elif da.startswith('[P] AUC'):
            auc_lst.append(da)
    losses = parse_loss(loss_lst)
    auc = parse_auc(auc_lst)
    print('Maximum for AUC is {} on epoch {}'.format(max(auc[6]), np.argmax(auc[6])))
    losses.update(auc)

    return losses

def plot_figs(root, fig_dict):
    fig_path = opj(root, 'result_figs')
    os.makedirs(fig_path, exist_ok=True)
    for key, value in fig_dict.items():
        plt.subplot(7,1,key+1)
        plt.plot(range(len(value[tolerate:])), value[tolerate:])

        plt.ylabel('{}'.format(enums_reverse[key]))
        plt.grid(True)

    plt.savefig(opj(fig_path, 'losses.jpg'))

    plt.clf();plt.cla();plt.close()

    for key, value in fig_dict.items():
        plt.plot(range(len(value[tolerate:])), value[tolerate:])
        plt.grid(True)
        plt.savefig(opj(fig_path, '{}.jpg'.format(enums_reverse[key])))

        plt.clf();plt.cla();plt.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', '-r', default=None, type=str, help='time stamp path in run directory')
    opt = parser.parse_args()

    loss_dict = get_dict(opt.root)
    plot_figs(opt.root, loss_dict)
    print('[I] Plotting figures done')
