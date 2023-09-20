1. numpy的数组类`ndarray`

   1. **数组创建**：

      1. **将array_like对象转换成数组**：Python中排列成array-like结构的数值数据可以通过使用array()函数转换为数组，例如**列表和元组**
      2. **numpy原生数组的创建**：函数`zeros`创建一个由0组成的数组，函数 `ones`创建一个完整的数组，函数`empty` 创建一个数组，其初始内容是随机的，取决于内存的状态。`arrange()`创建具有有规律递增值的数组。`linspace()` 将创建具有指定数量元素的数组，并在指定的开始值和结束值之间平均间隔。默认情况下，创建的数组的dtype是 `float64` 类型的。

      ```python
      >>> np.arange(2, 3, 0.1)
      array([ 2. , 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9])
      ```

   2. **打印数组**：

   ```python
   >>> c = np.arange(24).reshape(2,3,4)         # 3d array
   >>> print(c)
   [[[ 0  1  2  3]
     [ 4  5  6  7]
     [ 8  9 10 11]]
    [[12 13 14 15]
     [16 17 18 19]
     [20 21 22 23]]]
   ```

   3. **基本操作**：
      1. 数组上的算术运算符会应用到 *元素* 级别
      2. 乘积运算符`*`在NumPy数组中按元素进行运算。矩阵乘积可以使用`@`运算符或`dot`函数或方法执行 
      3. 当使用不同类型的数组进行操作时，结果数组的类型对应于更一般或更精确的数组（称为**向上转换**的行为）
      4. 通过指定`axis` 参数，您可以沿数组的指定轴应用操作
   4. **通函数**：NumPy提供熟悉的数学函数，例如sin，cos和exp等
   5. **索引、切片、迭代**：``b[i]` 方括号中的表达式 `i` 被视为后面紧跟着 `:` 的多个实例，用于表示剩余轴。NumPy也允许你使用三个点写为 `b[i,...]`。如果想要对数组中的每个元素执行操作，可以使用`flat`属性。

   ```python
   # 迭代
   >>> for row in b:
   ...     print(row)
   # 每个元素
   >>> for element in b.flat:
   ...     print(element)
   ```

   6. **形状操作**：

      1. 改变数组形状：方法`ravel()`、方法`reshape()`、方法`T`可以转置数组
      2. 堆叠数组：例如`np.vstack((a,b))`，`np.hstack((a,b))`可以堆叠两个数组
      3. 拆分数组：例如`np.hsplit(a,3)   # Split a into 3`，`np.hsplit(a,(3,4))   # Split a after the third and the fourth column`

   7. **拷贝、视图**：

      1. 完全不复制：`b = a            # no new object is created`
      2. 视图/浅拷贝：不同的数组对象可以共享相同的数据。该`view`方法创建一个**查看相同数据的新数组对象**

      ```python
      >>> c = a.view()
      >>> c is a
      False
      >>> c.base is a                        # c is a view of the data owned by a
      True
      >>> c.flags.owndata
      False
      ```

      3. 深拷贝：`copy`方法生成数组及其数据的完整副本

      ```python
      >>> d = a.copy()                          # a new array object with new data is created
      >>> d is a
      False
      >>> d.base is a                           # d doesn't share anything with a
      False
      ```

   8. **manuals**

      - **数组的创建（Array Creation）** - [arangeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.arange.html#numpy.arange), [arrayopen in new window](https://numpy.org/devdocs/reference/generated/numpy.array.html#numpy.array), [copyopen in new window](https://numpy.org/devdocs/reference/generated/numpy.copy.html#numpy.copy), [emptyopen in new window](https://numpy.org/devdocs/reference/generated/numpy.empty.html#numpy.empty), [empty_likeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.empty_like.html#numpy.empty_like), [eyeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.eye.html#numpy.eye), [fromfileopen in new window](https://numpy.org/devdocs/reference/generated/numpy.fromfile.html#numpy.fromfile), [fromfunctionopen in new window](https://numpy.org/devdocs/reference/generated/numpy.fromfunction.html#numpy.fromfunction), [identityopen in new window](https://numpy.org/devdocs/reference/generated/numpy.identity.html#numpy.identity), [linspaceopen in new window](https://numpy.org/devdocs/reference/generated/numpy.linspace.html#numpy.linspace), [logspaceopen in new window](https://numpy.org/devdocs/reference/generated/numpy.logspace.html#numpy.logspace), [mgridopen in new window](https://numpy.org/devdocs/reference/generated/numpy.mgrid.html#numpy.mgrid), [ogridopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ogrid.html#numpy.ogrid), [onesopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ones.html#numpy.ones), [ones_likeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ones_like.html#numpy.ones_like), [zerosopen in new window](https://numpy.org/devdocs/reference/generated/numpy.zeros.html#numpy.zeros), [zeros_likeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.zeros_like.html#numpy.zeros_like)
      - **转换和变换（Conversions）** - [ndarray.astypeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ndarray.astype.html#numpy.ndarray.astype), [atleast_1dopen in new window](https://numpy.org/devdocs/reference/generated/numpy.atleast_1d.html#numpy.atleast_1d), [atleast_2dopen in new window](https://numpy.org/devdocs/reference/generated/numpy.atleast_2d.html#numpy.atleast_2d), [atleast_3dopen in new window](https://numpy.org/devdocs/reference/generated/numpy.atleast_3d.html#numpy.atleast_3d), [matopen in new window](https://numpy.org/devdocs/reference/generated/numpy.mat.html#numpy.mat)
      - **操纵术（Manipulations）** - [array_splitopen in new window](https://numpy.org/devdocs/reference/generated/numpy.array_split.html#numpy.array_split), [column_stackopen in new window](https://numpy.org/devdocs/reference/generated/numpy.column_stack.html#numpy.column_stack), [concatenateopen in new window](https://numpy.org/devdocs/reference/generated/numpy.concatenate.html#numpy.concatenate), [diagonalopen in new window](https://numpy.org/devdocs/reference/generated/numpy.diagonal.html#numpy.diagonal), [dsplitopen in new window](https://numpy.org/devdocs/reference/generated/numpy.dsplit.html#numpy.dsplit), [dstackopen in new window](https://numpy.org/devdocs/reference/generated/numpy.dstack.html#numpy.dstack), [hsplitopen in new window](https://numpy.org/devdocs/reference/generated/numpy.hsplit.html#numpy.hsplit), [hstackopen in new window](https://numpy.org/devdocs/reference/generated/numpy.hstack.html#numpy.hstack), [ndarray.itemopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ndarray.item.html#numpy.ndarray.item), [newaxis](https://www.numpy.org.cn/reference/constants.html#numpy.newaxis), [ravelopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ravel.html#numpy.ravel), [repeatopen in new window](https://numpy.org/devdocs/reference/generated/numpy.repeat.html#numpy.repeat), [reshapeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.reshape.html#numpy.reshape), [resizeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.resize.html#numpy.resize), [squeezeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.squeeze.html#numpy.squeeze), [swapaxesopen in new window](https://numpy.org/devdocs/reference/generated/numpy.swapaxes.html#numpy.swapaxes), [takeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.take.html#numpy.take), [transposeopen in new window](https://numpy.org/devdocs/reference/generated/numpy.transpose.html#numpy.transpose), [vsplitopen in new window](https://numpy.org/devdocs/reference/generated/numpy.vsplit.html#numpy.vsplit), [vstackopen in new window](https://numpy.org/devdocs/reference/generated/numpy.vstack.html#numpy.vstack)
      - **询问（Questions）** - [allopen in new window](https://numpy.org/devdocs/reference/generated/numpy.all.html#numpy.all), [anyopen in new window](https://numpy.org/devdocs/reference/generated/numpy.any.html#numpy.any), [nonzeroopen in new window](https://numpy.org/devdocs/reference/generated/numpy.nonzero.html#numpy.nonzero), [whereopen in new window](https://numpy.org/devdocs/reference/generated/numpy.where.html#numpy.where),
      - **顺序（Ordering）** - [argmaxopen in new window](https://numpy.org/devdocs/reference/generated/numpy.argmax.html#numpy.argmax), [argminopen in new window](https://numpy.org/devdocs/reference/generated/numpy.argmin.html#numpy.argmin), [argsortopen in new window](https://numpy.org/devdocs/reference/generated/numpy.argsort.html#numpy.argsort), [maxopen in new window](https://docs.python.org/dev/library/functions.html#max), [minopen in new window](https://docs.python.org/dev/library/functions.html#min), [ptpopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ptp.html#numpy.ptp), [searchsortedopen in new window](https://numpy.org/devdocs/reference/generated/numpy.searchsorted.html#numpy.searchsorted), [sortopen in new window](https://numpy.org/devdocs/reference/generated/numpy.sort.html#numpy.sort)
      - **操作（Operations）** - [chooseopen in new window](https://numpy.org/devdocs/reference/generated/numpy.choose.html#numpy.choose), [compressopen in new window](https://numpy.org/devdocs/reference/generated/numpy.compress.html#numpy.compress), [cumprodopen in new window](https://numpy.org/devdocs/reference/generated/numpy.cumprod.html#numpy.cumprod), [cumsumopen in new window](https://numpy.org/devdocs/reference/generated/numpy.cumsum.html#numpy.cumsum), [inneropen in new window](https://numpy.org/devdocs/reference/generated/numpy.inner.html#numpy.inner), [ndarray.fillopen in new window](https://numpy.org/devdocs/reference/generated/numpy.ndarray.fill.html#numpy.ndarray.fill), [imagopen in new window](https://numpy.org/devdocs/reference/generated/numpy.imag.html#numpy.imag), [prodopen in new window](https://numpy.org/devdocs/reference/generated/numpy.prod.html#numpy.prod), [putopen in new window](https://numpy.org/devdocs/reference/generated/numpy.put.html#numpy.put), [putmaskopen in new window](https://numpy.org/devdocs/reference/generated/numpy.putmask.html#numpy.putmask), [realopen in new window](https://numpy.org/devdocs/reference/generated/numpy.real.html#numpy.real), [sumopen in new window](https://numpy.org/devdocs/reference/generated/numpy.sum.html#numpy.sum)
      - **基本统计（Basic Statistics）** - [covopen in new window](https://numpy.org/devdocs/reference/generated/numpy.cov.html#numpy.cov), [meanopen in new window](https://numpy.org/devdocs/reference/generated/numpy.mean.html#numpy.mean), [stdopen in new window](https://numpy.org/devdocs/reference/generated/numpy.std.html#numpy.std), [varopen in new window](https://numpy.org/devdocs/reference/generated/numpy.var.html#numpy.var)
      - **基本线性代数（Basic Linear Algebra）** - [crossopen in new window](https://numpy.org/devdocs/reference/generated/numpy.cross.html#numpy.cross), [dotopen in new window](https://numpy.org/devdocs/reference/generated/numpy.dot.html#numpy.dot), [outeropen in new window](https://numpy.org/devdocs/reference/generated/numpy.outer.html#numpy.outer), [linalg.svdopen in new window](https://numpy.org/devdocs/reference/generated/numpy.linalg.svd.html#numpy.linalg.svd), [vdotopen in new window](https://numpy.org/devdocs/reference/generated/numpy.vdot.html#numpy.vdot)

   9. **花式索引**：

      1. 使用索引数组：可以按顺序（比如列表）放入`i`，`j`然后使用列表进行索引

      ```python
      # example1
      >>> a = np.arange(12)**2                       # the first 12 square numbers
      >>> j = np.array( [ [ 3, 4], [ 9, 7 ] ] )      # a bidimensional array of indices
      >>> a[j]                                       # the same shape as j
      array([[ 9, 16],
             [81, 49]])
      # example2
      >>> a = np.arange(12).reshape(3,4)
      >>> a
      array([[ 0,  1,  2,  3],
             [ 4,  5,  6,  7],
             [ 8,  9, 10, 11]])
      >>> i = np.array( [ [0,1],                        # indices for the first dim of a
      ...                 [1,2] ] )
      >>> j = np.array( [ [2,1],                        # indices for the second dim
      ...                 [3,3] ] )
      >>>
      >>> a[i,j]                                     # i and j must have equal shape
      array([[ 2,  5],
             [ 7, 11]])
      # example3
      >>> l = [i,j]
      >>> a[l]                                       # equivalent to a[i,j]
      array([[ 2,  5],
             [ 7, 11]])
      ```

      2. 使用bool数组：使用与原始数组具有 *相同形状的* 布尔数组

      ```python
      >>> a = np.arange(12).reshape(3,4)
      >>> b1 = np.array([False,True,True])             # first dim selection
      >>> b2 = np.array([True,False,True,False])       # second dim selection
      >>>
      >>> a[b1,:]                                   # selecting rows
      array([[ 4,  5,  6,  7],
             [ 8,  9, 10, 11]])
      >>>
      >>> a[b1]                                     # same thing
      array([[ 4,  5,  6,  7],
             [ 8,  9, 10, 11]])
      >>>
      >>> a[:,b2]                                   # selecting columns
      array([[ 0,  2],
             [ 4,  6],
             [ 8, 10]])
      >>>
      >>> a[b1,b2]                                  # a weird thing to do
      array([ 4, 10])
      ```

      3. ix_()函数

      4. 为了便于数组形状与表达式和赋值的轻松匹配，可以在数组索引中使用`np.newaxis`对象来添加大小为1的新维度

         ```python
         >>> y.shape
         (5, 7)
         >>> y[:,np.newaxis,:].shape
         (5, 1, 7)
         ```

   10. **线性代数**：

      ```python
      >>> import numpy as np
      >>> a = np.array([[1.0, 2.0], [3.0, 4.0]])
      >>> print(a)
      [[ 1.  2.]
       [ 3.  4.]]
      
      >>> a.transpose()
      array([[ 1.,  3.],
             [ 2.,  4.]])
      
      >>> np.linalg.inv(a)
      array([[-2. ,  1. ],
             [ 1.5, -0.5]])
      
      >>> u = np.eye(2) # unit 2x2 matrix; "eye" represents "I"
      >>> u
      array([[ 1.,  0.],
             [ 0.,  1.]])
      >>> j = np.array([[0.0, -1.0], [1.0, 0.0]])
      
      >>> j @ j        # matrix product
      array([[-1.,  0.],
             [ 0., -1.]])
      
      >>> np.trace(u)  # trace
      2.0
      
      >>> y = np.array([[5.], [7.]])
      >>> np.linalg.solve(a, y)
      array([[-3.],
             [ 4.]])
      
      >>> np.linalg.eig(j)
      (array([ 0.+1.j,  0.-1.j]), array([[ 0.70710678+0.j        ,  0.70710678-0.j        ],
             [ 0.00000000-0.70710678j,  0.00000000+0.70710678j]]))
      ```

   11. **数据类型**：

      1. 转换数组的类型，使用 `.astype()` 方法（首选）或类型本身作为函数

      ```python
      >>> z.astype(float)                 
      array([  0.,  1.,  2.])
      >>> np.int8(z)
      array([0, 1, 2], dtype=int8)
      ```

      2. 查询数据类型：`np.issubdtype()`

   12. **广播**：描述了 numpy 如何在算术运算期间处理具有不同形状的数组

         1. 一般广播规则：在两个数组上运行时，NumPy会逐元素地比较它们的形状。它从尾随尺寸开始，并向前发展。两个尺寸兼容时
            1. 他们是平等的，或者
            2. 其中一个是1

         ```python
         # example
         A      (2d array):  5 x 4
         B      (1d array):      1
         Result (2d array):  5 x 4
         
         A      (2d array):  5 x 4
         B      (1d array):      4
         Result (2d array):  5 x 4
         
         A      (3d array):  15 x 3 x 5
         B      (3d array):  15 x 1 x 5
         Result (3d array):  15 x 3 x 5
         
         A      (3d array):  15 x 3 x 5
         B      (2d array):       3 x 5
         Result (3d array):  15 x 3 x 5
         
         A      (3d array):  15 x 3 x 5
         B      (2d array):       3 x 1
         Result (3d array):  15 x 3 x 5
         ```

   13. **结构化数组**：

         ```python
         # example
         >>> x = np.array([('Rex', 9, 81.0), ('Fido', 3, 27.0)],
         ...              dtype=[('name', 'U10'), ('age', 'i4'), ('weight', 'f4')])
         >>> x
         array([('Rex', 9, 81.), ('Fido', 3, 27.)],
               dtype=[('name', 'U10'), ('age', '<i4'), ('weight', '<f4')])
         
         ​```
         x 是一个长度为2的一维数组，其数据类型是一个包含三个字段的结构：
         长度为10或更少的字符串，名为“name”。
         一个32位整数，名为“age”。
         一个32位的名为'weight'的float类型。
         ​```
         ```

         1. 结构化数据类型：

            1. 结构化数据类型的创建：

               1. **元组列表，每个字段一个元组**。形式为`(fieldname, datatype, shape)`。`fieldname` 是字符串（如果使用标题，则为元组），` datatype` 可以是任何可转换为数据类型的对象，而 `shape` 是指定子数组形状的整数元组。如果 `fieldname` 是空字符串 `''` ，则将为字段指定格式为 `f#` 的默认名称， 其中 `#` 是字段的整数索引，从左侧开始从0开始计数。

               ```python
               # example
               >>> np.dtype([('x', 'f4'), ('y', np.float32), ('z', 'f4', (2, 2))])
               dtype([('x', '<f4'), ('y', '<f4'), ('z', '<f4', (2, 2))])
               ```

               2. **逗号分隔的数据类型规范字符串**。

               ```python
               # example
               >>> np.dtype('i8, f4, S3')
               dtype([('f0', '<i8'), ('f1', '<f4'), ('f2', 'S3')])
               >>> np.dtype('3int8, float32, (2, 3)float64')
               dtype([('f0', 'i1', (3,)), ('f1', '<f4'), ('f2', '<f8', (2, 3))])
               ```

               3. **字段参数组字典**。字典有两个必需键 “names” 和 “format”，以及四个可选键 “offsets”、“itemsize”、“Aligned” 和 “title”。 名称和格式的值应该分别是相同长度的字段名列表和dtype规范列表。 

                  可选的 “offsets” 值应该是整数字节偏移量的列表，结构中的每个字段都有一个偏移量。 如果未给出 “Offsets” ，则自动确定偏移量。可选的 “itemsize” 值应该是一个整数， 描述dtype的总大小（以字节为单位），它必须足够大以包含所有字段。可选的“Aligned”值可以设置为True，以使自动偏移计算使用对齐的偏移量。可选的 ‘titles’ 值应该是长度与 ‘names’ 相同的标题列表

               ```python
               # example
               >>> np.dtype({'names': ['col1', 'col2'],
               ...           'formats': ['i4', 'f4'],
               ...           'offsets': [0, 4],
               ...           'itemsize': 12})
               dtype({'names':['col1','col2'], 'formats':['<i4','<f4'], 'offsets':[0,4], 'itemsize':12})
               ```

         2. 显示结构化数据类型：

            1. `names` 在dtype对象的属性中找到结构化数据类型的字段名称列表

            ```python
            # example
            >>> d = np.dtype([('x', 'i8'), ('y', 'f4')])
            >>> d.names
            ('x', 'y')
            ```

            2. `fields`其键是字段名称，其值是包含每个字段的dtype和字节偏移量的元组

            ```python
            # example
            >>> d.fields
            mappingproxy({'x': (dtype('int64'), 0), 'y': (dtype('float32'), 8)})
            ```

            > 非结构化数组，`names`和`fields`属性都相同`None`

         3. 自动字节偏移与对齐：

         ```python
         # example1
         >>> print_offsets(np.dtype('u1, u1, i4, u1, i8, u2'))
         offsets: [0, 1, 2, 6, 7, 15]
         itemsize: 17
         ```

         > `align=True`设置了，numpy将以与许多C编译器填充C结构相同的方式填充结构

         ```python
         # example2
         >>> print_offsets(np.dtype('u1, u1, i4, u1, i8, u2', align=True))
         offsets: [0, 1, 4, 8, 16, 24]
         itemsize: 32
         ```
         4. 记录数组：
         
            1. 创建记录数组的最简单方法是`numpy.rec.array`，记录数组也使用特殊的数据类型，`numpy.record`允许通过属性对从数组中获取的结构化标量进行字段访问。
         
            ```python
            >>> recordarr = np.rec.array([(1, 2., 'Hello'), (2, 3., "World")],
            ...                    dtype=[('foo', 'i4'),('bar', 'f4'), ('baz', 'S10')])
            >>> recordarr.bar
            array([ 2.,  3.], dtype=float32)
            >>> recordarr[1:2]
            rec.array([(2, 3., b'World')],
                  dtype=[('foo', '<i4'), ('bar', '<f4'), ('baz', 'S10')])
            >>> recordarr[1:2].foo
            array([2], dtype=int32)
            >>> recordarr.foo[1:2]
            array([2], dtype=int32)
            >>> recordarr[1].baz
            b'World'
            ```
         
            2. `numpy.rec.array` 可以将各种参数转换为记录数组，包括结构化数组
         
            ```python
            >>> arr = np.array([(1, 2., 'Hello'), (2, 3., "World")],
            ...             dtype=[('foo', 'i4'), ('bar', 'f4'), ('baz', 'S10')])
            >>> recordarr = np.rec.array(arr)
            ```