import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Run KG_free.")

    parser.add_argument('--seed', type=int, default=2022,
                        help='Random seed.')

    parser.add_argument('--data_name', nargs='?', default='Douban',
                        help='Choose a dataset')
    parser.add_argument('--data_dir', nargs='?', default='data/',
                        help='Input data path.')
    
    parser.add_argument("--cuda", action='store_true',
                        help="use gpu or not")
    parser.add_argument("--gpu_id", type=int, default=0,
                        help="gpu id")

    parser.add_argument('--use_pretrain', type=int, default=0,
                        help='0: No pretrain, 1: Pretrain with stored model.')
    parser.add_argument('--pretrain_model_path', nargs='?', default='trained_model/KG_free.pth',
                        help='Path of stored model.')

    parser.add_argument('--embed_dim', type=int, default=32,
                        help='User / item Embedding size.')
    parser.add_argument('--l2loss_lambda', type=float, default=1e-4,
                        help='Lambda when calculating CF l2 loss.')

    parser.add_argument('--train_batch_size', type=int, default=1024,
                        help='Train batch size.')
    parser.add_argument('--test_batch_size', type=int, default=2048,
                        help='Test batch size (the number of users to test every batch).')

    parser.add_argument('--lr', type=float, default=1e-3,
                        help='Learning rate.')
    parser.add_argument('--n_epoch', type=int, default=1000,
                        help='Number of epoch.')
    parser.add_argument('--stopping_steps', type=int, default=10,
                        help='Number of epoch for early stopping')

    parser.add_argument('--print_every', type=int, default=1,
                        help='Iter interval of printing loss.')
    parser.add_argument('--evaluate_every', type=int, default=10,
                        help='Epoch interval of evaluating CF.')

    parser.add_argument('--Ks', nargs='?', default='[5, 10]',
                        help='Calculate metric@K when evaluating.')

    args = parser.parse_args()

    save_dir = 'trained_model/{}/KG_free/dim{}_lr{}_l2{}/'.format(
        args.data_name, args.embed_dim, args.lr, args.l2loss_lambda)
    args.save_dir = save_dir

    return args


