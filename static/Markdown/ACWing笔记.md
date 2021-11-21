# 基础算法

## 排序

### 快速排序

主要思想：分治

步骤：

1. 确定分界点：

   A. 取左边界：`q[l]` 

   B. 取右边界：`q[r]`

   C. 取中间值：`q[(l+r)>>1]`

   D. 随机值：`q[rand()%len]`

2. 调整区间：左边值小于等于X，右边值大于等于X

   A. 令指针 `i=l-1`，`j=r+1`

   B. `i`、`j` 向中间移动，直到 `q[i]>X`、`q[j]<X`

   C. `if(i<j)` 交换 `q[i]` 和 `q[j]` 的值

   D. 重复操作，直到 `i` 和 `j` 指针相遇

3. 递归处理子区间

代码：

```c++
#include <iostream>

using namespace std;

const int N = 100010;

int q[N];

void quick_sort(int q[], int l, int r)
{
    if (l >= r) return;

    int i = l - 1, j = r + 1, x = q[l + r >> 1];
    while (i < j)
    {
        do i ++ ; while (q[i] < x);
        do j -- ; while (q[j] > x);
        if (i < j) swap(q[i], q[j]);
    }

    quick_sort(q, l, j);
    quick_sort(q, j + 1, r);
}

int main()
{
    int n;
    scanf("%d", &n);

    for (int i = 0; i < n; i ++ ) scanf("%d", &q[i]);

    quick_sort(q, 0, n - 1);

    for (int i = 0; i < n; i ++ ) printf("%d ", q[i]);

    return 0;
}

作者：yxc
链接：https://www.acwing.com/activity/content/code/content/39784/
来源：AcWing
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

