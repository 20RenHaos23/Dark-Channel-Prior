import cv2
import numpy as np

def dehaze(I,A,t, clip_min=0.1, clip_max=999):
   
    I = np.float32(I) / 255
 
    J = np.zeros_like(I)

    for c in range(3):
        J[:, :, c] = (I[:, :, c] - A[0, c]) / np.clip(t, clip_min, clip_max) + A[0, c]
    
    
    cv2.imshow("haze_free_image",J)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    
    return J
    
def est_atomspheric_light(img, d_c):

    h,w,c = img.shape
    
    img = np.float32(img) / 255
    
    # 先計算總共要找幾個pixels
    brightest = int(np.ceil(0.001*h*w))
    #np.ceil無條件進位
    
    #reshaped d_c變成一維的
    d_c_1D = d_c.reshape(1,-1)
    
    
    #從小排到大
    d_c_index = np.argsort(d_c_1D)
    
    
    img_reshape = img.reshape(1, h*w, 3)#reshaped img變成一維的
    img_red = img.copy()#標記最亮的點為紅色 #複製一份
   
    img_brightest = np.zeros((1, brightest, 3), dtype=np.float32)
        
    for i in range(brightest):
        x = d_c_index[0,h*w-1-i]#為第i個最亮的值的位置值
        img_red[int(x/w), int(x%w), 0] = 0
        img_red[int(x/w), int(x%w), 1] = 0
        img_red[int(x/w), int(x%w), 2] = 1
        #將那個位置變成紅色的
        img_brightest[0, i, :] = img_reshape[0, x, :]
        
    
    A = np.mean(img_brightest, axis=1)
    print('atmospheric light:{}'.format(A))

    
    cv2.imshow("img_red",img_red)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    
    return A


def dark_channel(img, size=15):
    
    img = np.float32(img) / 255

    b, g, r = cv2.split(img)
    
    #從RGB找最小值
    dark = cv2.min(r, cv2.min(g, b))
    #dark = cv2.min(b, g, r)#這個也有一樣的結果
    

    #使用最小值濾波器
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    dark_min = cv2.erode(dark, kernel)
    #dark_min = scipy.ndimage.minimum_filter(dark, 15)#這個也有一樣的結果
    cv2.imshow("dark_channel",dark_min)
    #cv2.waitKey(1000)
    #cv2.destroyAllWindows()
    
    #計算transmission map
    transmission_map = 1 - 0.95*dark_min
    cv2.imshow("transmission_map",transmission_map)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    
    
    return dark_min,transmission_map

def guided_filter(guide,img,radius,eps):
    refined_dark_channel = cv2.ximgproc.guidedFilter(guide=guide, src=img, radius=radius, eps=eps) #問題:為甚麼guide輸入影像必為uint8的，不能是0~1之間的
    cv2.imshow("refined_dark_channel",refined_dark_channel)
    
    
    refined_transmission_map = 1 - 0.95*refined_dark_channel
    cv2.imshow("refined_transmission_map",refined_transmission_map)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    
    return refined_dark_channel,refined_transmission_map
    
    

def main():
    
    #輸入影像路徑
    img_path = "影像路徑"
    
    #-----------------------------------------------------
    #參數設定
    min_filer_size = 15 #最小值濾波器大小 paper有給資訊   
    guided_filter_r = 20 #引導濾波器半徑為2*r+1 因為半徑大小必須為奇數 paper有給資訊
    epsilon = 10**-3 #引導濾波器epsilon的值  paper有給資訊
    #------------------------------------------------------
    
    
    #讀取影像
    I = cv2.imread(img_path)
    cv2.imshow("I",I)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    
    #計算原始的dark channel與原始的transmission map
    d_c_raw,t_raw = dark_channel(I,min_filer_size)
    
    #對原始的dark channel進行引導濾波器濾波，計算refined的dark channel與transmission map
    d_c_guide,t_guide =  guided_filter(I,d_c_raw,guided_filter_r,epsilon)
    
    #計算atmospheric light
    A = est_atomspheric_light(I, d_c_raw)
   
    #除霧
    J = dehaze(I, A, t_guide)
    cv2.imwrite("haze-free.png", J*255)
    
if __name__ == '__main__':
    main()
    
    