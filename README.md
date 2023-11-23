# UpdateWeather      [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/hellsakura/UpdateWeather/main.yml?color=%2346c018&logo=github&style=flat-square)](https://github.com/HellSakura/UpdateWeather/actions)
调用和风天气api，为瀚文75扩展模块生成天气图片

[![python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=ffffff)](https://www.python.org/)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/hellsakura/UpdateWeather?style=flat-square&logo=github)](https://github.com/HellSakura/UpdateWeather/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/hellsakura/UpdateWeather/total?color=brightgreen&style=flat-square&logo=github)](https://github.com/HellSakura/UpdateWeather/releases/latest)


## 效果预览
![图片预览](docs/output.png#pic_center)
<img src="./docs/Actual%20picture.png#pic_center" width = "128" height = "296"  />

## 使用说明

>⚠注意：扩展模块需要刷入 xingrz 的[扩展固件](https://github.com/xingrz/zmk-config_helloword_hw-75/tree/master/config/boards/arm/hw75_dynamic)，才能正常工作

* 参见[快速开始](https://github.com/HellSakura/UpdateWeather/wiki/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

## Todolist    ![咕咕咕](https://img.shields.io/badge/-%E5%92%95%E5%92%95%E5%92%95-blue?style=flat-square)
- [x] 详细的使用说明
- [ ] 支持局部刷新（在想了在想了）
- [ ] [更多](https://dev.qweather.com/docs/resource/icons/) 的中文天气矢量图 
- [ ] `location`直接填入城市名称即可
- [ ] 无需填写`loccation`，自动获取当前位置
- [ ] NEW UI
![Alt text](docs/todo.png)

## macOS上的使用说明

### 依赖安装
```bash
pip install -r requirements.txt
```

### HIDAPI安装
先从[hidapi](https://github.com/libusb/hidapi/tree/master)clone源码，然后编译安装
```bash
# precondition: create a <build dir> somewhere on the filesystem (preferably outside of the HIDAPI source)
# this is the place where all intermediate/build files are going to be located
cd <build dir>
# configure the build
cmake <HIDAPI source dir>
# build it!
cmake --build .
# install library; by default installs into /usr/local/
cmake --build . --target install
# NOTE: you need to run install command as root, to be able to install into /usr/local/
```

### 配置天气接口key和location
参照[快速开始](https://github.com/HellSakura/UpdateWeather/wiki/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

### 刷新天气
```bash
python UpdateWeather.py
```

### 设置masOS定时任务
```bash
# 创建定时任务
crontab -e
# 添加定时任务，每30分钟执行一次，记得这里改成自己的真实路径
*/30 * * * * cd /path/to/UpdateWeather && /path/to/python /path/to/UpdateWeather/UpdateWeather.py
```