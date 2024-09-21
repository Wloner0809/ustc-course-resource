<font color=red>Attention：有一些改动/说明如下</font>

1. `new_kg_final.csv`是我处理过`kg_final.txt`之后的结果，因为之前的文件读取会出问题
2. 接1，所以我在`loader_base.py`这个文件里略作改动(不过对最后的评测没影响就是了，改了改文件读取部分)

```python
self.kg_file = os.path.join(self.data_dir, "new_kg_final.csv")


def load_kg(self, filename):
        kg_data = pd.read_csv(filename, sep=',', engine='python')
        kg_data = kg_data.drop_duplicates()
        return kg_data
```

3. 输出的一些参数什么都在`trained_model`这个文件夹下(包括KG_free、Embedding_based)，可以看看评测结果……
4. embedding我暂时是直接相乘处理的，可以试试相加/连接
5. 运行的参数我完全没调，可以调这部分参数(直接改default或者写个shell脚本)