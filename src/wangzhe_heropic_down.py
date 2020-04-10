# 爬取王者荣耀英雄图片
# 导入所需模块
import json

import requests
#import re
import os
import sys
#import os.path

# 查看编码
print(sys.getdefaultencoding())

# 重设编码
# from imp import reload
# reload(sys)
# sys.setdefaultencoding('gbk')#python3无法运行，只能在python2上运行

# 导入json文件（里面有所有英雄的名字及数字）

url = 'http://pvp.qq.com/web201605/js/herolist.json'  # 英雄的名字json

head = {'User-Agent': 'XiaoJihua-Heros'}
html = requests.get(url, headers=head)
print(html.raise_for_status())
print(html.status_code)
#html.encoding = 'GBK'
html = requests.get(url)
print(type(html))
html_json = html.json()
print(type(html_json))
# 提取英雄名字和数字
# title
# "new_type": 0,
# "hero_type": 1,
#"hero_type2": 4,
#"skin_name":

hero_name=list(map(lambda x:x['cname'],html_json)) #名字
hero_number=list(map(lambda x:x['ename'],html_json)) #编号
hero_skin=list(map(lambda x:x.get('skin_name'),html_json)) #皮肤
hero_title=list(map(lambda x:x['title'],html_json)) #title
hero_type=list(map(lambda x:x['hero_type'],html_json)) #title
hero_type2=list(map(lambda x:x.get('hero_type2'),html_json)) #title
hero_new_type=list(map(lambda x:x['title'],html_json)) #title

#print(hero_skin)
print(hero_title)
print(hero_type)
#print(hero_type2)
print(hero_new_type)

hero_type_dict={}
hero_type2_dict={}
hero_new_type_dict={"NNN":''}
i=1
os.chdir("D:/360Downloads/wangzhe_heros/")
for k,hero in enumerate(html_json):
    if k<88:
        continue  # 有些英雄未更新
    print("第",i,"位英雄是：", type(hero),type(html))
    print("第",i,"位英雄是：" , hero.get('cname'), hero['ename'])
    print(" title：" , hero['title'])
    print("皮肤有：" , hero.get('skin_name'))
    print("皮肤有：", hero.get('skin_name','|').split('|'))
    print("所属分类：",hero.get('hero_type'))
    print("所属分类2：", hero.get('hero_type2'))
    print("所属new分类：", hero.get('hero_new_type'))
    if hero.get('hero_type') not in hero_type_dict:
        hero_type_dict[hero.get('hero_type')] = hero.get('cname')
    else:
        hero_type_dict[hero.get('hero_type')] = hero_type_dict[hero.get('hero_type')] + ',' + hero.get('cname')
    if hero.get('hero_type2') not in hero_type2_dict:
        hero_type2_dict[hero.get('hero_type2')] = hero.get('cname')
    else:
        hero_type2_dict[hero.get('hero_type2')] = hero_type2_dict[hero.get('hero_type2')] + '|' + hero.get('cname')
    hero_new_type=hero.get('hero_new_type')
    print(hero_new_type)
    if not hero_new_type:
        print('NNN')
        hero_new_type_dict['NNN'] = hero_new_type_dict['NNN'] + '）（' + hero.get('cname')
    else:
        if hero_new_type not in hero_new_type_dict:
            hero_new_type_dict[hero_new_type] = hero.get('cname')
        else:
            hero_new_type_dict[hero_new_type] = hero_new_type_dict[hero_new_type] + '）（' + hero.get('cname')

#下载皮肤保存         game.gtimg.cn/images/yxzj/img201606/skin/hero-info/524/524-bigskin-1.jpg
#该皮肤信息未实时更新？ ,所以1-12 都尝试下载

    for u in range(12):
        skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(hero['ename']) + '/' + str(hero['ename']) + '-bigskin-' + str(u) + '.jpg'
        im = requests.get(skin_url)
        skin_name=''
        if u<=len(hero.get('skin_name','|').split('|')):
            skin_name=hero.get('skin_name','|').split('|')[u-1]
        if im.status_code == 200:
            filename=hero.get('cname') + "_" + skin_name + str(u)+'.jpg'
            #已存在，则不下载？ 直接覆盖
            if os.path.isfile(filename):
                pass
            else:
                open(filename, 'wb').write(im.content)
    i=i+1


hero_name = list(map(lambda x: x['cname'], html_json))  # 名字
print(hero_name)
hero_number = list(map(lambda x: x['ename'], html_json))  # 数字 即英雄编号
print(hero_number)


print("英雄分类：",hero_type_dict)
for key,value in hero_type_dict.items():
    print("英雄分类：",key)
    print("该分类英雄有：", value)
print("英雄分类2：",hero_type2_dict)
for key,value in hero_type2_dict.items():
    print("英雄分类2：",key)
    print("该分类2英雄有：", value)
print("英雄新分类：",hero_new_type_dict)
for key,value in hero_new_type_dict.items():
    print("英雄新分类：",key)
    print("该英雄新分类的英雄有：", value)
'''

if __name__ == "__main__":

    # 下载并保存
    ii = 0
    #	os.mkdir("D:/D/mylib/python/2/heros/"+hero_name[ii])
    #   os.chdir("D:/D/mylib/python/2/heros/"+hero_name[ii])
    os.mkdir("king_heros")
    os.chdir("king_heros")
    for v in hero_number:
        print(ii)

        #       print(os.chdir)
        #       print( hero_number)

        for u in range(12):
            onehero_links = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(v) + '/' + str(
                v) + '-bigskin-' + str(u) + '.jpg'
            print(onehero_links)
            im = requests.get(onehero_links)
            if im.status_code == 200:
                iv = re.split('-', onehero_links)
                open(hero_name[ii] + "_" + iv[-1], 'wb').write(im.content)
        ii = ii + 1
'''