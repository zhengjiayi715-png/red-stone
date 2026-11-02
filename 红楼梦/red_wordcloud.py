import matplotlib.pyplot as plt
import wordcloud

import imageio

bg_pic=imageio.imread('star.jpg')
f = open("红楼梦_词频.txt",'r')
text = f.read()
f.close()
wcloud=wordcloud.WordCloud(font_path ="simhei.ttf",
                             background_color = "white",width=1000,
                             max_words = 500,
                             mask = bg_pic, # mask参数设置词云形状
                             height = 860, margin = 2).generate(text)

wcloud.to_file("红楼梦cloud_star.png")   # 保存图片

#  显示词云图片
plt.imshow(wcloud)
plt.axis('off')
plt.show()
