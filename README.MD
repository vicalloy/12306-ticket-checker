# 12306 刷票脚本

## 注意事项

- 脚本采用python3开发，请使用python3运行该脚本
- 在刷到票后，采用 [Slack](https://slack.com/) 发送通知消息，因此请先创建Slack的Team。在创建好Team后，创建一个名叫`ticket`的channel,并申请一个Bot用于发消息。如希望采用其他的通知途径，请自行修改12306.py中的send_message实现。
    - 创建新Team https://slack.com/
    - 创建Bot参考文档 [Bot Users](https://api.slack.com/bot-users)

## 使用方法

- 安装依赖库
    ```
pip3 install requests
pip3 install slackclient
    ```
- 复制`conf.py.sample`并修改文件名为`conf.py`，
- 根据注释修改刷票条件
- `python3 12306.py`启动脚本，验证脚本是否可以正确执行。
    - 注：你可以用supervisor来管理该脚本
