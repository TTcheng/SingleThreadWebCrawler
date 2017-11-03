# 获取jikexueyuan.com/course前20页上的课程信息
# 包括课程名，课程介绍，课程时长，课程等级，学习人数
#
# requests 获取网页
# re.sub换页
# 正则表达式匹配内容

import re
import requests


class JikexueyuanCourseCrawler(object):
    def __init__(self,url):
        self.url = url          # 起始页
        self.courses = []       # 课程链表
        self.html = None        # 网页源码
        self.blocks = None      # 课程块表
        self.nowPageNum = 0     # 当前页码
        self.totalPageNum = 20

# 开始
    def start(self):
        print(r'start crawling ...')
        while self.nowPageNum < self.totalPageNum:
            self.refreshNowPageNum()
            self.getSourceCode()
            self.getCourseBlock()
            self.getCourseInfo()
            self.changePage()
        self.saveInfo()

# getSourceCode 用来获取网页源代码
    def getSourceCode(self):
        print('processing %s' % self.url)
        self.html = requests.get(self.url).text

# 获取当前页码
    def refreshNowPageNum(self):
        self.nowPageNum = int(re.search('pageNum=(\d+)', self.url, re.S).group(1))

# 实现翻页
    def changePage(self):
        self.url = re.sub('pageNum=\d+', 'pageNum=%d'%(self.nowPageNum+1), self.url, re.S)

# 抓取课程块
    def getCourseBlock(self):
        self.blocks = re.findall('lessonimg-box">(.*?)</li>', self.html, re.S)

# 抓取课程信息
    def getCourseInfo(self):
        for block in self.blocks:
            courseInfo = {}
            courseInfo['name'] = re.search('title="(.*?)" alt=', block, re.S).group(1)
            courseInfo['introduction'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>', block, re.S).group(1).replace('\t','').replace('\n','')
            timeandlevel = re.findall('<em>(.*?)</em>', block, re.S)
            courseInfo['time'] = timeandlevel[0].replace('\t','').replace('\n','')
            courseInfo['level'] = timeandlevel[1].replace('\t','').replace('\n','')
            courseInfo['learnersNum'] = re.search('"learn-number">(.*?)</em>', block, re.S).group(1)
            self.courses.append(courseInfo)
            # self.blocks = None  # 清空

# 保存信息到文本
    def saveInfo(self):
        f = open('info.txt', 'a')
        for course in self.courses:
            f.writelines('课程名称:' + course['name'] + '\n')
            f.writelines('\t介绍:' + course['introduction'] + '\n')
            f.writelines('\t时长:' + course['time'] + '\n')
            f.writelines('\t等级:' + course['level'] + '\n')
            f.writelines('\t人数:' + course['learnersNum'] + '\n')
        f.close()


if __name__ == '__main__':
    rootUrl = 'http://www.jikexueyuan.com/course/?pageNum=1'
    JikexueyuanCourseCrawler(rootUrl).start()


# course list
# courses = []
#
# # course info dict
# course = {'name':'courseName',
#           'introduction':'courseIntroduction',
#           'time':'courseTime',
#           'level':'courseLevel',
#           'learnersNum':'courseLearnersNum'
# }
#
#
# def saveInfo(courses):
#     f = open('info.txt', 'a')
#     for course in courses:
#         f.writelines('课程名称:' + course['name'] + '\n')
#         f.writelines('\t介绍:' + course['introduction'] + '\n')
#         f.writelines('\t时长:' + course['time'] + '\n')
#         f.writelines('\t等级:' + course['level'] + '\n')
#         f.writelines('\t人数:' + course['learnersNum'] + '\n')
#     f.close()
#
#
# def process_url(url):
#     print('processing %s...' %url)
#     fullHtml = requests.get(url)
#     largeInfo = re.search('<ul class="cf" style="display: block;">(.*?)</ul>', fullHtml.text, re.S).group(1)  # 先抓大
#     # print(largeInfo)
#     smallIofo = re.findall('lessonimg-box">(.*?)</li>', largeInfo, re.S)    # 再抓小
#     # print(smallIofo)
#     for info in smallIofo:
#         # print(info)
#         course['name'] = re.search('title="(.*?)" alt=',info,re.S).group(1)
#         course['introduction'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>',info,re.S).group(1).replace('\t','').replace('\n','')
#
#         timeandlevel = re.findall('<em>(.*?)</em>', info, re.S)
#         course['time'] = timeandlevel[0].replace('\t','').replace('\n','')
#         course['level'] = timeandlevel[1].replace('\t','').replace('\n','')
#         # # xinhao-icon"></i><em>初级</em>
#         # # xinhao-icon2"></i><em>中级</em>
#         # # xinhao-icon3"></i><em>高级</em>
#         course['learnersNum'] = re.search('number">(.*?)学习</em>',info,re.S).group(1)
#         print(course)
#         courses.append(course)
#
#
# root_url = 'http://www.jikexueyuan.com/course/'
# new_url = 'http://www.jikexueyuan.com/course/?pageNum=2'
#
# process_url(root_url)
#
# for i in range(2,20+1):
#     new_url = re.sub('pageNum=\d+','pageNum=%d'%i,new_url,re.S)
#     process_url(new_url)
# saveInfo(courses)