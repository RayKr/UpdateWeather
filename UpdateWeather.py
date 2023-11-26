import configparser
import os
import requests
import datetime
import binascii
import re
import hid
import tkinter as tk
from psutil import *
from PIL import Image
from tkinter import messagebox

#读取config.ini文件

config = configparser.ConfigParser()
config_file = os.path.join(os.getcwd(), 'config.ini')
config.read(config_file)

if not config.has_option('DEFAULT', 'key'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'key'")
    exit()

if not config.has_option('DEFAULT', 'location'):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "配置文件中缺少必要参数 'location'")
    exit()

key = config.get('DEFAULT', 'key')
if not key:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "未填写 'key' 参数")
    exit()

location = config.get('DEFAULT', 'location')
if not location:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "未填写 'location' 参数")
    exit()


# 使用和风天气api
params = {
    'key': key,
    'location': location,
    'language': 'zh',
    'unit': 'm'
}

session = requests.Session()

url = 'https://devapi.qweather.com/v7/weather/3d'
url_today = 'https://devapi.qweather.com/v7/weather/now'

try:
    with session.get(url, params=params) as r, session.get(url_today, params=params) as t:
        r.raise_for_status()
        t.raise_for_status()

        try:
            data = r.json()['daily']
        except KeyError:
            raise ValueError(r.text)
        
        data_today = t.json()['now']

        today = data[0]['fxDate']
        
        tempmin = data[0]['tempMin']
        tempmax = data[0]['tempMax']

        textDay = data[0]['textDay']
        textNight = data[0]['textNight']

        tempnow = data_today['temp']

        iconDay = data[0]['iconDay']
        iconNight = data[0]['iconNight']

        print('获取当前天气'+today)


except requests.exceptions.RequestException as e:
    error_message = str(e)
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "请检查网络连接")
    exit()

except (KeyError, ValueError) as e:
    error_message = str(e)
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('错误', "请检查key或location输入是否正确\n" + error_message)
    exit()


# 定义数字图片和线条图片的路径
image_path = "./img/"
line_path = "./img/line.png"
cpu_path = "./img/cpu.png"
bai_path = "./img/%.png"
men_path = "./img/men.png"
gb_path = "./img/g.png"
chinese_path = "./img/"
nowtemp_path = "./img/nowtemp.png"
wave_path = "./img/wave.png"

# 定义要解析的日期字符串和中文字符串
date_str = today
iconDay_str = iconDay
iconNight_str  = iconNight
textDay_str = textDay
textNight_str = textNight

# 获取当前是星期几
year, month, day = map(int, date_str.split('-'))
date = datetime.date(year, month, day)
weekday = date.strftime("%A")
# 根据星期切换图片
weekday2 = date.strftime("%A")+"2"

# 将日期字符串解析成数字列表和线条数量
digits = [int(d) if d.isdigit() else "-" for d in date_str]
num_lines = date_str.count("-")

# 将CPU数据解析成数字列表和线条数量
cpu = str(cpu_percent(interval=2))
cpu_xinxi = [int(d) if d.isdigit() else "." for d in cpu]

# 计算cpu字符串的长度
cpu_str_len = len(cpu)
# print("CPU使用率：",cpu_str_len)
# print("CPU使用率：",cpu)
# print("CPU使用率：",cpu_xinxi)

# 读取内存信息
mem = virtual_memory()
mem_total = str(round((float(mem.total) / 1024 / 1024 / 1024),0))
mem_percent = str(int(mem.percent))
#print("内存总量: ",mem_total,"内存使用率：", mem_percent, "%")

# 计算内存信息字符串的长度
mem_total_str_len = len(mem_total)
mem_percent_str_len = len(mem_percent)
#print("内存长度：",mem_total_str_len,mem_percent_str_len)

# 将内存总量数据解析成数字列表和线条数量
mem_total_xinxi = [int(d) if d.isdigit() else "." for d in mem_total]
# 将内存使用率数据解析成数字列表和线条数量
mem_percent_xinxi = [int(d) if d.isdigit() else "." for d in mem_percent]


#print("内存长度：",mem_total_xinxi,mem_percent_xinxi)

# 将温度值转换为带有符号的字符串
tempmin_digits = [d for d in tempmin if d.isdigit() or d == "-"]
tempmin_int = int("".join(tempmin_digits))
tempmin_str = "{:d}".format(tempmin_int)

tempmax_digits = [d for d in tempmax if d.isdigit() or d == "-"]
tempmax_int = int("".join(tempmax_digits))
tempmax_str = "{:d}".format(tempmax_int)

tempnow_digits = [d for d in tempnow if d.isdigit() or d == "-"]
tempnow_int = int("".join(tempnow_digits))
tempnow_str = "{:d}".format(tempnow_int)

# 计算温度值字符串的长度
tempmin_str_len = len(tempmin_str)
tempmax_str_len = len(tempmax_str)
tempnow_str_len = len(tempnow_str)

# 计算温度值字符串在新图片上的水平偏移量
if tempmin_str_len == 3:
    tempmin_offset_x =(64 - (12 * 3 + 8)) // 2
elif tempmin_str_len == 2:
    tempmin_offset_x = (64 - (12 * 2 + 8)) // 2
else:
    tempmin_offset_x = (64 - (12 * 1 + 8)) // 2

if tempmax_str_len == 3:
    tempmax_offset_x = 64 + (64 - (12 * 3 + 8)) // 2
elif tempmax_str_len == 2:
    tempmax_offset_x = 64 + (64 - (12 * 2 + 8)) // 2
else:
    tempmax_offset_x = 64 + (64 - (12 * 1 + 8)) // 2

if tempnow_str_len == 3:
    tempnow_offset_x = (190 - (12 * 3 + 8)) // 2
elif tempnow_str_len == 2:
    tempnow_offset_x = (190 - (12 * 2 + 8)) // 2
else:
    tempnow_offset_x = (190 - (12 * 1 + 8)) // 2

# 创建一张128x296的新图片
new_image = Image.new("RGB", (128, 296), color=(255, 255, 255))

# 将数字图片和线条图片拼接到新图片上
x_offset = (128 - 120) // 2
y_offset = (32 - 14) // 2
for digit in digits:
    if digit == "-":
        # 加载线条图片
        line_image = Image.open(line_path)

        # 将线条图片粘贴到新图片上
        new_image.paste(line_image, (x_offset, y_offset))

        # 更新线条图片在新图片中的水平偏移量
        x_offset += line_image.width
    else:
        # 加载数字图片
        digit_image = Image.open(image_path + str(digit) + ".png")

        # 将数字图片粘贴到新图片上
        new_image.paste(digit_image, (x_offset, y_offset))

        # 更新数字图片在新图片中的水平偏移量
        x_offset += digit_image.width

# 将星期粘贴到新图片上
weekday_image = Image.open(chinese_path + str(weekday) + ".png")
new_image.paste(weekday_image, (0, 32))

# 将cpu的数字图片和线条图片拼接到新图片上
x_offset2 = (128 - 80) // 2
y_offset2 = 55
for cpu_xinxis in cpu_xinxi:
    if cpu_xinxis == "-":

        # 加载线条图片
        line_image = Image.open(line_path)

        # 将线条图片粘贴到新图片上
        new_image.paste(line_image, (x_offset2, y_offset2))

        # 更新线条图片在新图片中的水平偏移量
        x_offset2 += line_image.width
    else:
        # 加载cpu图片
        cpu_image = Image.open(cpu_path)
        new_image.paste(cpu_image, (6, 55))
    
        # 加载数字图片
        cpu_image2 = Image.open(image_path + str(cpu_xinxis) + ".png")

        # 将数字图片粘贴到新图片上
        new_image.paste(cpu_image2, (x_offset2, y_offset2))

        # 更新数字图片在新图片中的水平偏移量
        x_offset2 += cpu_image2.width

# 加载%图片     s
bai_image = Image.open(bai_path)
new_image.paste(bai_image, (x_offset2+1, y_offset2))


# 将内存的数字图片和线条图片拼接到新图片上
x_offset3 = (128 - 80) // 2
y_offset3 = 76
for mem_total_xinxis in mem_total_xinxi:
    if mem_total_xinxis == "-":

        # 加载线条图片
        line_image = Image.open(line_path)

        # 将线条图片粘贴到新图片上
        new_image.paste(line_image, (x_offset3, y_offset3))

        # 更新线条图片在新图片中的水平偏移量
        x_offset3 += line_image.width
    else:
        # 加载cpu图片
        men_image = Image.open(men_path)
        new_image.paste(men_image, (6, 76))
    
        # 加载数字图片
        cpu_image3 = Image.open(image_path + str(mem_total_xinxis) + ".png")

        # 将数字图片粘贴到新图片上
        new_image.paste(cpu_image3, (x_offset3, y_offset3))

        # 更新数字图片在新图片中的水平偏移量
        x_offset3 += cpu_image3.width

# 加载%图片     
mem_total_image = Image.open(gb_path)
new_image.paste(mem_total_image, (x_offset3+1, y_offset3))

# 将内存使用率数字图片和线条图片拼接到新图片上
x_offset3=x_offset3+25
for mem_percent_xinxis in mem_percent_xinxi:
    if mem_percent_xinxis == "-":

        # 加载线条图片
        line_image = Image.open(line_path)

        # 将线条图片粘贴到新图片上
        new_image.paste(line_image, (x_offset3, y_offset3))

        # 更新线条图片在新图片中的水平偏移量
        x_offset3 += line_image.width
    else:
    
        # 加载数字图片
        cpu_image4 = Image.open(image_path + str(mem_percent_xinxis) + ".png")

        # 将数字图片粘贴到新图片上
        new_image.paste(cpu_image4, (x_offset3, y_offset3))

        # 更新数字图片在新图片中的水平偏移量
        x_offset3 += cpu_image4.width

# 加载%图片     
mem_total_image = Image.open(bai_path)
new_image.paste(mem_total_image, (x_offset3+1, y_offset3))



# 将天气图标粘贴到新图片上
weather_image = Image.open(image_path + iconDay + ".jpg")
new_image.paste(weather_image, (6, 96))
weather_image = Image.open(image_path + iconNight + ".jpg")
new_image.paste(weather_image, (70, 96))

# 将温度值字符串中的每个字符分别加载对应的图片，并粘贴到新图片上
tempmin_y_offset = 180
for min, ch in enumerate(tempmin_str):
    if ch == "-":
        # 加载减号图片
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempmin_offset_x, tempmin_y_offset))
    else:
        # 加载对应数字图片
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempmin_offset_x + min * 12, tempmin_y_offset))

tempmax_y_offset = 180
for max, ch in enumerate(tempmax_str):
    if ch == "-":
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempmax_offset_x, tempmax_y_offset))
    else:
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempmax_offset_x + max * 12, tempmax_y_offset))

tempnow_y_offset = 209
for now, ch in enumerate(tempnow_str):
    if ch == "-":
        minus_image = Image.open(image_path + "minus.png")
        new_image.paste(minus_image, (tempnow_offset_x, tempnow_y_offset))
    else:
        digit_image = Image.open(image_path + ch + ".png")
        new_image.paste(digit_image, (tempnow_offset_x + now * 12, tempnow_y_offset))


# 将中文图片粘贴到新图片上
weather_image = Image.open(image_path + textDay + ".png")
new_image.paste(weather_image, (0, 150))
weather_image = Image.open(image_path + textNight + ".png")
new_image.paste(weather_image, (72, 150))

# 将温度单位图片粘贴到新图片上
temp_unit_image = Image.open(image_path + "temp_unit.png")
new_image.paste(temp_unit_image, (tempmin_offset_x + min * 12 + 12, tempmin_y_offset))
new_image.paste(temp_unit_image, (tempmax_offset_x + max * 12 + 12, tempmax_y_offset))
new_image.paste(temp_unit_image, (tempnow_offset_x + now * 12 + 12, tempnow_y_offset))

# 将其他图片粘贴到新图片上
nowtemp_image = Image.open(nowtemp_path)
new_image.paste(nowtemp_image, (3, 205))
wave_image = Image.open(wave_path)
new_image.paste(wave_image, (58, 148))
new_image.paste(wave_image, (58, 175))

# 将星期变更的7张照片粘贴到新图片上
weekday_image = Image.open(chinese_path + str(weekday2) + ".png")
new_image.paste(weekday_image, (0, 227))

# 保存新图片
new_image.save("output.png")
print('创建图片')

# 刷新墨水屏
if __name__ == '__main__':
    img = Image.open('./output.png')

    black_img = img.convert("L")  # 转化为黑白图片#进行灰度处理
    bdata_list = list(black_img.getdata())

    threshold = 128
    bvalue_list = [0 if i < threshold else 1 for i in bdata_list]
    # 将8位一组放在一起
    ob_list = []
    s = "0b"
    for i in range(1, len(bvalue_list) + 1):
        s += str(bvalue_list[i - 1])
        if i % 8 == 0:
            ob_list.append(s)
            s = "0b"
    # 转换为16进制字符串 格式定位两位
    ox_list = ['%02x' % int(i, 2) for i in ob_list]
    j = 0
    firstPackage = '013e8d2508072a8825080b1080251a8025'
    nextPackage = '013e'
    lastPackage = '0128'
    hexStr = ''
    hexStr += firstPackage
    for i in range(0, 47):
        hexStr += ox_list[j]
        j += 1
    packCount = int((len(ox_list) - 47) / 62)
    for i in range(0, packCount):
        hexStr += nextPackage
        for k in range(0, 62):
            if j >= len(ox_list):
                hexStr += '00'
            else:
                hexStr += ox_list[j]
            j += 1
    hexStr += lastPackage
    for k in range(0, 62):
        if j >= len(ox_list):
            hexStr += '00'
        else:
            hexStr += ox_list[j]
        j += 1
    st2 = re.findall(r'.{128}', hexStr)
    st2.append(hexStr[int(int(len(hexStr) / 128) * 128):])
    h = hid.enumerate(vid=0x1d50, pid=0x615e)
    # 用usage_page选择设备
    path = None 
    for device_info in h:
        if device_info['usage_page'] == 65300:
            path = device_info['path']
            break
    if path:
        d = hid.Device(path=path)
    #   d = hid.Device(path=h[2]['path'])
    d.write(binascii.unhexlify(
        '01050408011200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
    pack = d.read(1000).decode("utf8", "ignore")
    print("CPU使用率：",cpu_percent(interval=2))
    print("内存总量: ",mem_total,"内存使用率：", mem_percent, "%")
    print('Zephyr 版本:' + pack[9:16])
    print('ZMK 版本:' + pack[18:25])
    print('固件版本:' + pack[27:34])
    for i in st2:
        if i == '':
            continue
        d.write(binascii.unhexlify(i))
    print('图片刷新完成')
