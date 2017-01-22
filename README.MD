# 12306 刷票脚本

## 注意事项

- 脚本采用python3开发，请使用python3运行该脚本
- 在刷到票后，采用slack发送通知消息，因此请先注册slack账号。在创建好slack账号后，创建一个名叫`ticket`的channel,并申请一个bot用于发消息。如希望采用其他的通知途径，请自行修改12306.py中的send_message实现。

## 使用方法

- 安装依赖库
    ```
pip3 install requests
pip3 install slackclient
    ```
- 复制`conf.py.sample`并修改文件名为`conf.py`，
- 根据注释修改刷票条件
- `python3 12306.py`启动脚本。
    - 注：你可以用supervisor来管理该脚本
