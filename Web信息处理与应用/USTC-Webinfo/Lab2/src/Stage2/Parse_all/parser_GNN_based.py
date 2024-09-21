import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Run GNN_based.")

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
    parser.add_argument('--pretrain_model_path', nargs='?', default='trained_model/GNN_based.pth',
                        help='Path of stored model.')

    parser.add_argument('--cf_batch_size', type=int, default=1024,
                        help='CF batch size.')
    parser.add_argument('--kg_batch_size', type=int, default=2048,
                        help='KG batch size.')
    parser.add_argument('--test_batch_size', type=int, default=2048,
                        help='Test batch size (the user number to test every batch).')

    parser.add_argument('--embed_dim', type=int, default=32,
                        help='User / entity Embedding size.')
    parser.add_argument('--relation_dim', type=int, default=32,
                        help='Relation Embedding size.')

    parser.add_argument('--laplacian_type', type=str, default='random-walk',
                        help='Specify the type of the adjacency (laplacian) matrix from {symmetric, random-walk}.')

    parser.add_argument('--KG_embedding_type', type=str, default='TransR',
                        help='Specify the type of the KG embedding from {TransE, TransR}.')
    parser.add_argument('--aggregation_type', type=str, default='lightgcn',
                        help='Specify the type of the aggregation layer from {gcn, graphsage, lightgcn}.')

    parser.add_argument('--n_layers', type=int, default=2,
                        help='Number of GNN aggregation layers.')
    parser.add_argument('--mess_dropout', type=float, default=0.1,
                        help='Dropout probability w.r.t. message dropout for each GNN layer. 0: no dropout.')

    parser.add_argument('--kg_l2loss_lambda', type=float, default=1e-5,
                        help='Lambda when calculating KG l2 loss.')
    parser.add_argument('--cf_l2loss_lambda', type=float, default=1e-4,
                        help='Lambda when calculating CF l2 loss.')

    parser.add_argument('--lr', type=float, default=1e-3,
                        help='Learning rate.')
    parser.add_argument('--n_epoch', type=int, default=1000,
                        help='Number of epoch.')
    parser.add_argument('--stopping_steps', type=int, default=10,
                        help='Number of epoch for early stopping')

    parser.add_argument('--cf_print_every', type=int, default=1,
                        help='Iter interval of printing CF loss.')
    parser.add_argument('--kg_print_every', type=int, default=1,
                        help='Iter interval of printing KG loss.')
    parser.add_argument('--evaluate_every', type=int, default=10,
                        help='Epoch interval of evaluating CF.')

    parser.add_argument('--Ks', nargs='?', default='[5, 10]',
                        help='Calculate metric@K when evaluating.')

    args = parser.parse_args()

    save_dir = 'trained_model/{}/GNN_based/nlayer{}_dim{}_{}_{}'.format(
        args.data_name, args.n_layers, args.embed_dim, args.KG_embedding_type, args.aggregation_type)
    args.save_dir = save_dir

    return args


