# Dark_Channel_Prior
使用Python實作[Single Image Haze Removal Using Dark Channel Prior](https://ieeexplore.ieee.org/document/5567108)此篇論文的影像去霧演算法


步驟
---
1. 計算輸入影像 $I$ 的Dark Channel $\rightarrow$ $D(x)$
    
    >$$D(x) = \min_{c \in \{r, g, b\}}(\min_{y \in \Omega(x)} (\frac{I^c(y)}{A^c}))$$
    >* $A^c$設定為 $[255,255,255]$
    >* 最小值濾波器(minimum filter)大小設定為 $15$ $\times$ $15$

2. 計算transmission map $\rightarrow$ $t(x)$
    
    >$$t(x) = 1-\omega\times D(x)$$
    >* $\omega$設定為 $0.95$


3. 使用[引導濾波器(guide filter)](https://ieeexplore.ieee.org/document/6319316)精煉、提煉(refine) $D(x)$ 得到新的 $D^{'}(x)$
    
    >$$D^{'}(x) = guided \ filter \lbrace	D(x) \rbrace$$
    >* $\sigma$ 設定為 $0.001$ ( $\sigma$ 為[引導濾波器(guide filter)](https://ieeexplore.ieee.org/document/6319316)使用參數)
    >* $r$ 設定為 $20$ ( $r$ 為[引導濾波器(guide filter)](https://ieeexplore.ieee.org/document/6319316)使用參數).

   $\color {red} {問題:作為guided的影像必須為0 \textasciitilde 255的資料型態，不能是0 \textasciitilde 1的資料型態，不知道是甚麼原因}$

4. 使用新得到的 $D^{'}(x)$ 根據步驟2計算新的transmission map $\rightarrow$ $t^{'}(x)$
    
    >$$t^{'}(x) = 1-\omega\times D^{'}(x)$$
    >* $\omega$設定為 $0.95$


5. 使用{\bf{D(x)}}計算Atomspheric Light
    >* 對 $D(x)$ 找前 $0.1\%$ 強度值的位置，再對應找輸入影像 $I$ 三個Channel相對位置的強度值，並計算平均
    >* $A$ 會為 $[$ $mean_B$ , $mean_G$ , $mean_R$ $]$


6. 計算去霧影像(haze-free image)
    
    >$$\mathbf{J}(x) = \frac{\mathbf{I}(x)-\mathbf{A}}{max(t^{'}(x),t_0)}+\mathbf{A}$$
    >* $t_0$設定為 $0.1$
    >* $\mathbf{J}$ 、 $\mathbf{I}$ 、 $\mathbf{A}$ 各代表三個Channel




參考網址
---
[Single Image Haze Removal Using Dark Channel Prior](https://ieeexplore.ieee.org/document/5567108)

[引導濾波器(guide filter)](https://ieeexplore.ieee.org/document/6319316)

[Single Image Haze Removal Using Dark Channel Prior 论文阅读与代码实现](https://blog.csdn.net/qq_40755643/article/details/83347135)
