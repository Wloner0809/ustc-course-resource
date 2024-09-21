import jieba

sent = """安托万·德·圣埃克苏佩里（Antoine de Saint-Exupery, 1900-1944）1900年6月29日出生在法国里昂。他曾经有志于报考海军学院，未能如愿，却有幸成了空军的一员。1923年退役后，先后从事过各种不同的职业。 1926年，圣埃克苏佩里进入拉泰科埃尔航空公司。在此期间，出版小说《南方邮件》（1929）、《夜航》（1931），从此他在文学上声誉鹊起。1939年，又一部作品《人的大地》问世。 第二次世界大战期间他重入法国空军。后辗转去纽约开始流亡生活。在这期间，写出《空军飞行员》、《给一个人质的信》、《小王子》（1943）等作品。1944年返回同盟国地中海空军部队。在当年7月31日的一次飞行任务中，他驾驶飞机飞上湛蓝的天空，就此再也没有回来。"""

seg_list = jieba.cut(sent, cut_all=True)

print('\n全模式：      ', '/ '.join(seg_list))

seg_list = jieba.cut(sent, cut_all=False)
print('\n精确模式：    ', '/ '.join(seg_list))

seg_list = jieba.cut(sent)
print('\n默认精确模式：', '/ '.join(seg_list))

seg_list = jieba.cut_for_search(sent)
print('\n搜索引擎模式  ', '/ '.join(seg_list))
