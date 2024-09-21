import torch
import torch.nn as nn
import torch.nn.functional as F


def _L2_loss_mean(x):
    return torch.mean(torch.sum(torch.pow(x, 2), dim=1, keepdim=False) / 2.)


class Aggregator(nn.Module):

    def __init__(self, embed_dim, dropout, aggregator_type):
        super(Aggregator, self).__init__()
        self.embed_dim = embed_dim
        self.dropout = dropout
        self.aggregator_type = aggregator_type

        self.message_dropout = nn.Dropout(dropout)
        self.activation = nn.LeakyReLU()

        if self.aggregator_type == 'gcn':
            self.linear = nn.Linear(self.embed_dim, self.embed_dim)             # W in Equation (6)
            nn.init.xavier_uniform_(self.linear.weight)

        elif self.aggregator_type == 'graphsage':
            self.linear = nn.Linear(self.embed_dim * 2, self.embed_dim)         # W in Equation (7)
            nn.init.xavier_uniform_(self.linear.weight)


    def forward(self, ego_embeddings, A_in):
        """
        ego_embeddings:  (n_users + n_entities, embed_dim)
        A_in:            (n_users + n_entities, n_users + n_entities), torch.sparse.FloatTensor
        """
        # 1. Equation (3) 得到一跳邻域的表征 side_embeddings
        side_embeddings =                                                       # (n_users + n_entities, embed_dim)

        if self.aggregator_type == 'gcn':
            # 2. Equation (6) 将中心节点表征和一跳邻域表征相加，再进行线性变换和非线性激活
            embeddings =                                                        # (n_users + n_entities, embed_dim)
            embeddings =                                                        # (n_users + n_entities, embed_dim)

        elif self.aggregator_type == 'graphsage':
            # 3. Equation (7) 将中心节点表征和一跳邻域表征拼接，再进行线性变换和非线性激活
            embeddings =                                                        # (n_users + n_entities, embed_dim * 2)
            embeddings =                                                        # (n_users + n_entities, embed_dim)

        elif self.aggregator_type == 'lightgcn':
            # 4. Equation (8) 简单地将中心节点表征和一跳邻域表征相加
            embeddings = 

        embeddings = self.message_dropout(embeddings)                           # (n_users + n_entities, out_dim)
        return embeddings


class GNN_based(nn.Module):

    def __init__(self, args, n_users, n_entities, n_relations, A_in):

        super(GNN_based, self).__init__()
        self.device = torch.device("cuda:" + str(args.gpu_id)) if args.cuda else torch.device("cpu")

        self.n_users = n_users
        self.n_entities = n_entities
        self.n_relations = n_relations
        self.A_in = A_in.to(self.device)

        self.embed_dim = args.embed_dim
        self.relation_dim = args.relation_dim

        self.aggregation_type = args.aggregation_type
        self.n_layers = args.n_layers
        self.mess_dropout = args.mess_dropout

        self.kg_l2loss_lambda = args.kg_l2loss_lambda
        self.cf_l2loss_lambda = args.cf_l2loss_lambda

        self.entity_user_embed = nn.Embedding(self.n_entities + self.n_users, self.embed_dim)
        self.relation_embed = nn.Embedding(self.n_relations, self.relation_dim)
        nn.init.xavier_uniform_(self.entity_user_embed.weight)
        nn.init.xavier_uniform_(self.relation_embed.weight)

        # TransR
        self.trans_M = nn.Parameter(torch.Tensor(self.n_relations, self.embed_dim, self.relation_dim))
        nn.init.xavier_uniform_(self.trans_M)

        self.aggregator_layers = nn.ModuleList()
        for k in range(self.n_layers):
            self.aggregator_layers.append(Aggregator(self.embed_dim, self.mess_dropout, self.aggregation_type))


    def calc_cf_embeddings(self):
        ego_embed = self.entity_user_embed.weight                               # (n_users + n_entities, embed_dim)
        all_embed = [ego_embed]

        # 5. 迭代地计算每一层卷积层的实体（包含用户）嵌入，将其L2范数归一化后，append到all_embed中
        for idx, layer in enumerate(self.aggregator_layers):
                                                                                # (n_users + n_entities, embed_dim)
        
        

        # 无需修改，将每层的输出加起来形成最终的实体（包含用户）嵌入，并保存在all_embed中
        all_embed = torch.sum(torch.stack(all_embed), dim=0)                    # (n_users + n_entities, embed_dim)
        
        return all_embed


    def calc_cf_loss(self, user_ids, item_pos_ids, item_neg_ids):
        """
        user_ids:       (cf_batch_size)
        item_pos_ids:   (cf_batch_size)
        item_neg_ids:   (cf_batch_size)
        """
        all_embed = self.calc_cf_embeddings()                                   # (n_users + n_entities, embed_dim)
        user_embed = all_embed[user_ids]                                        # (cf_batch_size, embed_dim)
        item_pos_embed = all_embed[item_pos_ids]                                # (cf_batch_size, embed_dim)
        item_neg_embed = all_embed[item_neg_ids]                                # (cf_batch_size, embed_dim)

        pos_score = torch.sum(user_embed * item_pos_embed, dim=1)               # (cf_batch_size)
        neg_score = torch.sum(user_embed * item_neg_embed, dim=1)               # (cf_batch_size)

        # BPR Loss
        cf_loss = (-1.0) * F.logsigmoid(pos_score - neg_score)
        cf_loss = torch.mean(cf_loss)

        # L2 Loss
        l2_loss = _L2_loss_mean(user_embed) + _L2_loss_mean(item_pos_embed) + _L2_loss_mean(item_neg_embed)

        loss = cf_loss + self.cf_l2loss_lambda * l2_loss
        return loss


    def calc_kg_loss_TransR(self, h, r, pos_t, neg_t):
        """
        h:      (kg_batch_size)
        r:      (kg_batch_size)
        pos_t:  (kg_batch_size)
        neg_t:  (kg_batch_size)
        """
        r_embed = self.relation_embed(r)                                                # (kg_batch_size, relation_dim)
        W_r = self.trans_M[r]                                                           # (kg_batch_size, embed_dim, relation_dim)

        h_embed = self.entity_user_embed(h)                                             # (kg_batch_size, embed_dim)
        pos_t_embed = self.entity_user_embed(pos_t)                                     # (kg_batch_size, embed_dim)
        neg_t_embed = self.entity_user_embed(neg_t)                                     # (kg_batch_size, embed_dim)

        # 7. 计算头实体，尾实体和负采样的尾实体在对应关系空间中的投影嵌入
        r_mul_h =                                                                       # (kg_batch_size, relation_dim)
        r_mul_pos_t =                                                                   # (kg_batch_size, relation_dim)
        r_mul_neg_t =                                                                   # (kg_batch_size, relation_dim)

        # 8. 对关系嵌入，头实体嵌入，尾实体嵌入，负采样的尾实体嵌入进行L2范数归一化
        r_embed = 
        r_mul_h = 
        r_mul_pos_t = 
        r_mul_neg_t = 

        # 9. 分别计算正样本三元组 (h_embed, r_embed, pos_t_embed) 和负样本三元组 (h_embed, r_embed, neg_t_embed) 的得分
        pos_score =                                                                     # (kg_batch_size)
        neg_score =                                                                     # (kg_batch_size)

        # 10. 使用 BPR Loss 进行优化，尽可能使负样本的得分大于正样本的得分
        kg_loss = 

        l2_loss = _L2_loss_mean(r_mul_h) + _L2_loss_mean(r_embed) + _L2_loss_mean(r_mul_pos_t) + _L2_loss_mean(r_mul_neg_t)
        loss = kg_loss + self.kg_l2loss_lambda * l2_loss
        return loss


    def calc_kg_loss_TransE(self, h, r, pos_t, neg_t):
        """
        h:      (kg_batch_size)
        r:      (kg_batch_size)
        pos_t:  (kg_batch_size)
        neg_t:  (kg_batch_size)
        """
        r_embed = self.relation_embed(r)                                                # (kg_batch_size, relation_dim)
        
        h_embed = self.entity_user_embed(h)                                             # (kg_batch_size, embed_dim)
        pos_t_embed = self.entity_user_embed(pos_t)                                     # (kg_batch_size, embed_dim)
        neg_t_embed = self.entity_user_embed(neg_t)                                     # (kg_batch_size, embed_dim)

        # 11. 对关系嵌入，头实体嵌入，尾实体嵌入，负采样的尾实体嵌入进行L2范数归一化
        r_embed = 
        h_embed = 
        pos_t_embed = 
        neg_t_embed = 

        # 12. 分别计算正样本三元组 (h_embed, r_embed, pos_t_embed) 和负样本三元组 (h_embed, r_embed, neg_t_embed) 的得分
        pos_score =                                                                      # (kg_batch_size)
        neg_score =                                                                      # (kg_batch_size)

        # 13. 使用 BPR Loss 进行优化，尽可能使负样本的得分大于正样本的得分
        kg_loss = 

        l2_loss = _L2_loss_mean(h_embed) + _L2_loss_mean(r_embed) + _L2_loss_mean(pos_t_embed) + _L2_loss_mean(neg_t_embed)
        loss = kg_loss + self.kg_l2loss_lambda * l2_loss
        return loss


    def calc_score(self, user_ids, item_ids):
        """
        user_ids:  (n_users)
        item_ids:  (n_items)
        """
        all_embed = self.calc_cf_embeddings()                                       # (n_users + n_entities, concat_dim)
        user_embed = all_embed[user_ids]                                            # (n_users, concat_dim)
        item_embed = all_embed[item_ids]                                            # (n_items, concat_dim)

        cf_score = torch.matmul(user_embed, item_embed.transpose(0, 1))             # (n_users, n_items)
        return cf_score


    def forward(self, *input, mode):
        if mode == 'train_cf':
            return self.calc_cf_loss(*input)
        if mode == 'TransR':
            return self.calc_kg_loss_TransR(*input)
        if mode == 'TransE':
            return self.calc_kg_loss_TransE(*input)
        if mode == 'predict':
            return self.calc_score(*input)
