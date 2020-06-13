import json
import xml.dom.minidom
import sys
import os


def json2xml(json_file):
    if json_file[-5:] != '.json':
        raise KeyError
    xml_file = json_file[0:-4] + 'xml'
    with open(json_file, 'r', encoding='utf-8') as f0, open(xml_file, 'w', encoding='utf-8') as f1:
        json_txt = f0.read()
        json_dict = json.loads(json_txt)
        start_time = json_dict['info']['start_time']
        danmaku_list = json_dict['full_comments']

        doc = xml.dom.minidom.Document()
        root = doc.createElement('i')
        doc.appendChild(root)
        for danmaku in danmaku_list:
            if not danmaku.get('text'):  # 跳过礼物
                continue
            d = doc.createElement('d')
            uid_crc32b = hex(binascii.crc32(str(danmaku['user_id']).encode()))[2:]
            p = f'{(danmaku["time"]-start_time)/1000},1,25,16777215,' \
                f'{danmaku["time"]//1000},0,{uid_crc32b},{danmaku["i"]}'
            d.setAttribute('p', p)
            d.appendChild(doc.createTextNode(danmaku['text']))
            root.appendChild(d)
        doc.writexml(f1)


if __name__ == '__main__':
    print('正在转换文件：', sys.argv[1], '\n')
    try:
        json2xml(sys.argv[1])
    except Exception:
        print('转换失败\n')
    else:
        print('转换成功\n')

    os.system('pause')
