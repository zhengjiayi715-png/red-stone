import re
import matplotlib.pyplot as plt
import networkx as nx

# ================= 1. 分割章回 =================
f = open('红楼梦.txt', 'r', encoding='utf-8') 
s = f.read()
f.close()

lst_chapter = []
chapter = re.findall("第[\u4E00-\u9FA5]+回", s)
for x in chapter:
    if x not in lst_chapter and len(x) <= 5:
        lst_chapter.append(x)

lst_start_chapterindex = []
for x in lst_chapter:
    lst_start_chapterindex.append(s.index(x))

lst_end_chapterindex = lst_start_chapterindex[1:] + [len(s)]
lst_chapterindex = list(zip(lst_start_chapterindex, lst_end_chapterindex))

# ================= 全局字体设置 =================
# 只需要在这里设置一次，后面的所有图都能正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ================= 2. 画悲喜图 =================
cnt_laugh = []
cnt_cry = []
# 优化：不要写死 range(120)，用实际长度
for ii in range(len(lst_chapterindex)): 
    start = lst_chapterindex[ii][0]
    end = lst_chapterindex[ii][1]
    cnt_laugh.append(s[start:end].count("笑") + s[start:end].count("喜"))
    cnt_cry.append(s[start:end].count("哭") + s[start:end].count("悲"))

plt.figure(figsize=(15, 4))
plt.plot(cnt_laugh, label="笑和喜", color='red', alpha=0.7)
plt.plot(cnt_cry, label="哭和悲", color='blue', alpha=0.7)
plt.xlabel("章节数")
plt.ylabel("出现次数")
plt.legend()
plt.title("《红楼梦》120回悲喜变化图")
plt.show()

# ================= 3. 刘姥姥三进荣国府 =================
cnt_liulaolao = []
for ii in range(len(lst_chapterindex)):
    start = lst_chapterindex[ii][0]
    end = lst_chapterindex[ii][1]
    cnt_liulaolao.append(s[start:end].count("刘姥姥"))

plt.figure(figsize=(15, 4))
plt.plot(cnt_liulaolao, label="刘姥姥出场次数", color='green')
plt.xlabel("章节数")
plt.ylabel("出现次数")
plt.legend()
plt.title("《红楼梦》——刘姥姥三进荣国府")
plt.show()

# ================= 4. 字长和段落数散点图 =================
cnt_chap = []
cnt_word = []
for ii in range(len(lst_chapterindex)):
    start = lst_chapterindex[ii][0]
    end = lst_chapterindex[ii][1]
    cnt_chap.append(s[start:end].count("\n"))
    cnt_word.append(len(s[start:end]))

plt.figure(figsize=(8, 6))
plt.scatter(cnt_chap, cnt_word, alpha=0.6)
for ii in range(len(lst_chapterindex)):
    plt.text(cnt_chap[ii] - 2, cnt_word[ii] + 100, lst_chapter[ii], size=7)
plt.xlabel("章节段数")
plt.ylabel("章节字数")
plt.title("《红楼梦》120回章节字数与段数关系")
plt.show()

# ================= 5. 生成人物关系网络图 =================
Names = ['宝玉', '凤姐', '贾母', '黛玉', '王夫人', '老太太', '袭人', '贾琏', '平儿', '宝钗', '薛姨妈', '探春', '鸳鸯',
         '贾政', '晴雯', '湘云', '刘姥姥', '邢夫人', '贾珍', '紫鹃', '香菱', '尤氏', '薛蟠', '贾赦']

relations = {}
lst_para = s.split('\n') 
for text in lst_para:
    for name1 in Names:
        if name1 in text:
            for name2 in Names:
                if name2 in text and name1 != name2 and (name2, name1) not in relations:
                    relations[(name1, name2)] = relations.get((name1, name2), 0) + 1

maxRela = max([v for k, v in relations.items()])
relations = {k: v / maxRela for k, v in relations.items()}

G = nx.Graph()
for k, v in relations.items():
    G.add_edge(k[0], k[1], weight=v)

elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.6]
emidle = [(u, v) for (u, v, d) in G.edges(data=True) if (d['weight'] > 0.3) & (d['weight'] <= 0.6)]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.3]

# ---- 第一张：弹簧布局 ----
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42) # 加上 seed 固定形状
nx.draw_networkx_nodes(G, pos, alpha=0.8, node_size=800, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2.5, alpha=0.9, edge_color='g')
nx.draw_networkx_edges(G, pos, edgelist=emidle, width=1.5, alpha=0.6, edge_color='y')
nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, alpha=0.4, edge_color='b', style='dashed')
nx.draw_networkx_labels(G, pos, font_size=12)
plt.axis('off')
plt.title("《红楼梦》主要人物社交关系网络图 (弹簧布局)")
plt.show()

# ---- 第二张：环形布局 ----
plt.figure(figsize=(12, 12))
pos = nx.circular_layout(G)
nx.draw_networkx_nodes(G, pos, alpha=0.8, node_size=800, node_color='lightgreen')
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2.5, alpha=0.9, edge_color='g')
nx.draw_networkx_edges(G, pos, edgelist=emidle, width=1.5, alpha=0.6, edge_color='y')
nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, alpha=0.2, edge_color='b', style='dashed')
nx.draw_networkx_labels(G, pos, font_size=12)
plt.axis('off')
plt.title("《红楼梦》主要人物社交关系网络图 (环形布局)")
plt.savefig("圈图.png", dpi=300, bbox_inches='tight')
plt.show()

# ================= 4.5 金陵十二钗出场次数堆积柱状图 =================
print("正在统计金陵十二钗数据...")
# 定义十二钗的核心称呼（用核心词能覆盖文本中的大部分称谓）
jlc_names = ['黛玉', '宝钗', '元春', '探春', '湘云', '妙玉',
             '迎春', '惜春', '凤姐', '巧姐', '李纨', '可卿']

# 初始化一个字典，用来存每个人的 120 回出场次数列表
jlc_counts = {name: [] for name in jlc_names}

# 遍历 120 回，统计每个人的出现次数
for ii in range(len(lst_chapterindex)):
    start = lst_chapterindex[ii][0]
    end = lst_chapterindex[ii][1]
    chapter_text = s[start:end]

    for name in jlc_names:
        # 统计该回中出现的次数，并存入对应人物的列表中
        jlc_counts[name].append(chapter_text.count(name))

# 开始绘图
plt.figure(figsize=(20, 8))  # 120回数据较多，画布需要宽一点

# 设置 x 轴（第 1 到 120 回）
x = range(1, len(lst_chapterindex) + 1)

# 初始化底部高度（用于堆积图）
bottom = [0] * len(lst_chapterindex)

# 准备一个好看的颜色列表（12种颜色）
colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
          '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff']

# 循环绘制每个人的柱子，并堆叠在一起
for idx, name in enumerate(jlc_names):
    counts = jlc_counts[name]
    plt.bar(x, counts, bottom=bottom, label=name, color=colors[idx], width=0.8)
    # 更新底部高度，下一次绘制会堆叠在当前柱子上方
    bottom = [bottom[i] + counts[i] for i in range(len(bottom))]

# 图表美化设置
plt.xlabel("章回 (1-120)")
plt.ylabel("出场次数")
plt.title("《红楼梦》金陵十二钗各章回出场次数堆积图")
# 将图例放在图表外侧，防止遮挡柱子
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', title="金陵十二钗")
plt.tight_layout()  # 自动调整布局防止图例被截断
plt.show()