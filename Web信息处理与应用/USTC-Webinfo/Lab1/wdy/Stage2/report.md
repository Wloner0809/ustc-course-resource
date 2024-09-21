# report

## Stage1_2



## Stage2

第一步首先对助教所提供的代码进行小幅改动。考虑到时间因素的影响，我们采取了以下的修正方式。

可以理解的是，评分时间对用户评分的有效性有较为关键的影响因素。时间越久远的评分，其分数的可信度也有一定的下降。为了表征这一下降幅度，我们给评分加入了时间权重：

- 取所有评分时间的最大值 $max$ 和最小值 $min$。

- 将评分时间 $time$ 做如下操作：
  $$
  time\_value = (time - min) / (max - min)
  $$

- 将 $time\_value$ 作为权重加入 $rate$ ：
  $$
  rating = rating * time
  $$

做出如上修正之后，训练结果中 $loss$ 和 $ndcg$ 分别有如下变化：

- 未作时间修正

  ![](assets/notime.png)

- 时间修正

  ![](assets/time.png)

可以看到，加入时间修正之后，平均 $ndcg$ 有小幅降低，但是 $Train\space loss$ 和 $Test\space loss$ 有显著降低，说明模型的泛化能力得到了提高。