#!/usr/bin/python3
import numpy as np


class NumpyDemo(object):

    def __init__(self):
        self.type = 0

    def test(self):
        self.base_data_type()
        self.array_property()
        self.create_array()

    def base_data_type(self):
        print("---NumpyDemo base_data_type--- create")
        # 使用标量类型
        dt = np.dtype(np.int32)
        print("int:", dt)

        # int8, int16, int32, int64 四种数据类型可以使用字符串 'i1', 'i2','i4','i8' 代替
        dt = np.dtype('i4')
        print(dt)

        #
        dt = np.dtype([("age", np.int16)])
        print(dt)

        dt = np.dtype([('age', np.int8)])
        a = np.array([(10,), (20,), (30,)], dtype=dt)
        print(a)

        # 类型字段名可以用于存取实际的age列
        dt = np.dtype([('age', np.int8)])
        a = np.array([(10,), (20,), (30,)], dtype=dt)
        print(a['age'])

        # 结构化数据类型 student，包含字符串字段 name，整数字段 age，及浮点字段 marks，并将这个 dtype 应用到 ndarray 对象。
        student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])
        print("student:", student)

        a = np.array([('abc', 21, 50), ('xyz', 18, 75)], dtype=student)
        print(a)

    def array_property(self):
        print("---NumpyDemo array_property---")
        # 一个基本的三维数组可以使用 numpy 模块的 array 函数创建，其形状为 (depth, height, width)。例如，以下是创建一个 324 的三维数组的示例代码：
        a = np.arange(24)
        print("a 维度：", a.ndim, "\na:", a)

        b = a.reshape(2, 3, 4)

        print("b 维度：", b.ndim, "\nb:", b)

        b = a.reshape(3, 2, 4)

        print("b 维度：", b.ndim, "\nb:", b)

        print("b第一个深度层的所有元素", b[0, :, :])  # 获取第一个深度层的所有元素
        print("b获取所有深度层和所有宽度上索引为 1 的元素", b[:, 1, :])  # 获取所有深度层和所有宽度上索引为 1 的元素
        print("b获取所有深度层和所有高度、宽度上索引为 2 到 4 的元素", b[:, :, 2:4])  # 获取所有深度层和所有高度、宽度上索引为 2 到 4 的元素

        b = a.reshape(3, 4, 2)

        print("b 维度：", b.ndim, "\nb:", b)
        print("b shape", b.shape)
        print("b itemsize", b.itemsize)
        print("b flags", b.flags)

    def create_array(self):
        print("---NumpyDemo createArray---")
        a = np.array([1, 2, 3, 4, 5])
        print(a)

        # 数据类型或 dtype，描述在数组中的固定大小值的格子
        aa = np.array(a, dtype=complex)
        print(aa)

        print("---二维数组")
        b = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
        print(b)
        print("---三维数组")
        c = np.array([
            [[1, 2, 3, 4], [5, 6, 7, 8]],
            [[9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24]]
        ])
        print(c)

        # numpy.empty 方法用来创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组

        x = np.empty([3, 2], dtype=int)
        print("x:", x, "itemsize:", x.itemsize)

        x = np.ones(7)

        print("x:", x, "itemsize:", x.itemsize)

        x = np.ones([3, 3], dtype=int)

        print("x:", x, "itemsize:", x.itemsize)

        # create 3*3 array

        x = np.arange(12)
        x.shape = (3, 4)

        y = np.ones_like(x)

        print("y:", y)

        # 从已有的数组创建数组
        # 将列表转换为 ndarray:
        x = [1, 2, 3, 4, 5]
        y = np.asarray(x)
        print("y:", y)

        # 将元组转换为 ndarray
        x = (1, 2, 3, 4, 5)
        y = np.asarray(x, dtype=float)
        print("y:", y)

        # numpy.frombuffer
        #
        # numpy.frombuffer 用于实现动态数组。

        x = b'Hello word'

        y = np.frombuffer(x, dtype='S2')
        print('y', y)

        x = b'Hello word'

        y = np.frombuffer(x, dtype='int8')
        print('y', y)

        # numpy.fromiter 方法从可迭代对象中建立 ndarray 对象，返回一维数组
        # 使用 range 函数创建列表对象
        mylist = range(10)
        it = iter(mylist)

        # 使用迭代器创建 ndarray
        x = np.fromiter(it, dtype=int)
        print("x:", x)

        # NumPy 从数值范围创建数组
        x = np.arange(10, dtype=float)
        print("np.arange(10):", x)

        x = np.arange(1, 20, 2)
        print("np.arange设置了起始值、终止值及步长:", x)

        # numpy.linspace 函数用于创建一个一维数组，数组是一个等差数列构成的，格式如下：
        #
        # np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)

        x = np.linspace(1, 20, 10)
        print("np.linspace(1, 20, 10):", x)

        x = np.linspace(1, 1, 10)
        print("np.linspace(1, 1, 10):", x)

        x = np.linspace(10, 20, 5)
        print("np.linspace(10, 20, 5):", x)

        x = np.linspace(10, 20, 5, endpoint=False)
        print("np.linspace(10, 20, 5,  endpoint = False):", x)
