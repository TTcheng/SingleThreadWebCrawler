# 获取jikexueyuan.com/course前20页上的课程信息
# 包括课程名，课程介绍，课程时长，课程等级，学习人数
#
# requests 获取网页
# re.sub换页
# 正则表达式匹配内容

import re
import requests


# course list
courses = []

# course info dict
course = {'name':'courseName',
          'introduction':'courseIntroduction',
          'time':'courseTime',
          'level':'courseLevel',
          'learnersNum':'courseLearnersNum'
}


def saveInfo(courses):
    f = open('info.txt', 'a')
    for course in courses:
        f.writelines('课程名称:' + course['name'] + '\n')
        f.writelines('\t介绍:' + course['introduction'] + '\n')
        f.writelines('\t时长:' + course['time'] + '\n')
        f.writelines('\t等级:' + course['level'] + '\n')
        f.writelines('\t人数:' + course['learnersNum'] + '\n')
    f.close()

def process_url(url):
    print('processing %s...' %url)
    fullHtml = requests.get(url)
    largeInfo = re.search('<ul class="cf" style="display: block;">(.*?)</ul>', fullHtml.text, re.S).group(1)  # 先抓大
    # print(largeInfo)
    smallIofo = re.findall('lessonimg-box">(.*?)</li>', largeInfo, re.S)    # 再抓小
    # print(smallIofo)
    for info in smallIofo:
        # print(info)
        course['name'] = re.search('title="(.*?)" alt=',info,re.S).group(1)
        course['introduction'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>',info,re.S).group(1).replace('\t','').replace('\n','')

        timeandlevel = re.findall('<em>(.*?)</em>', info, re.S)
        course['time'] = timeandlevel[0].replace('\t','').replace('\n','')
        course['level'] = timeandlevel[1].replace('\t','').replace('\n','')
        # # xinhao-icon"></i><em>初级</em>
        # # xinhao-icon2"></i><em>中级</em>
        # # xinhao-icon3"></i><em>高级</em>
        course['learnersNum'] = re.search('number">(.*?)学习</em>',info,re.S).group(1)
        print(course)
        courses.append(course)


root_url = 'http://www.jikexueyuan.com/course/'
new_url = 'http://www.jikexueyuan.com/course/?pageNum=2'

process_url(root_url)

for i in range(2,20+1):
    new_url = re.sub('pageNum=\d+','pageNum=%d'%i,new_url,re.S)
    process_url(new_url)

saveInfo(courses)