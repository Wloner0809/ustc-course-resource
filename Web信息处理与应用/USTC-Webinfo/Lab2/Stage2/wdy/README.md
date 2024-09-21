## 一点修正

在第一阶段的 result 里有一点需要修改的地方：

只有 2.png 的一部分内容。

原本的 2.png：

![](assets/2.png)

其中第二跳子图的生成没有问题，但是下面过滤后的计数有一点问题（是因为我当时修改了过滤的参数，但是改大了，导致最终过滤完的图中不包含原本 578 个电影的两个了）。

但是过滤后的文件 KG_filter_path_2.txt 没有问题，因为这个文件是我第一次调参（正确）之后的结果，调参调大了的那个结果我没有下载到本地，只是截了个图。

最终这个图片应当修改为：

第二跳共有三元组： 317217383 （没变）

第二跳共有实体： 50861749 （没变）

第二跳共有关系：1818 （没变）

第二跳过滤后共有三元组：544645

第二跳过滤后共有实体： 103041

第二跳过滤后共有关系： 110

## 我做的结果

![](assets/1.png)

kg_final.txt 实际上就是 第一阶段生成的 KG_filter_path_2.txt 的编号版，它将第一阶段生成的子图中的实体和关系对应到 id 上，便于之后的处理。其中第一阶段的 578 个电影实体分别映射到了 [0, 577] ，其它的实体依次往后添加，关系同理被映射到了 [0, 109]。

> 请先将 `wdy/Douban` 下的数据复制到 `stage2/data/Douban` 目录下

虽然 PPT 只要求生成 kg_final.txt ，但是我把实体关系与 kg_final.txt 中 id 的对应关系也保存了（防止需要使用）。如果需要使用，可以按下面的方式得到结构化的数据：

- kg_final.txt

  ```python
  # entities = set()
  # relations = set()
  with open('stage2/data/Douban/kg_final.txt', 'r') as f:
          for line in f:
              triplet = line.strip().split('\t')
              head = triplet[0]
              relation = triplet[1]
              tail = triplet[2]
              # entities.add(head)
              # entities.add(tail)
              # relations.add(relation)
  ```

- 以 entities2id.txt 为例，relations2id 同理

  注意这里的实体和关系均带有前缀。

  ```python
  # entities2id = {}
  with open('stage2/data/Douban/entities2id.txt', 'r') as f:
          for line in f:
              entity, _id = line.strip().split('\t')
              # entities2id[entity] = id
  ```

  