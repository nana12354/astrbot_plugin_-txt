# 导入 astrbot.api.all 模块中的所有对象
from astrbot.api.all import *
import os

# 使用 register 装饰器注册插件
@register("txt_search_plugin", "TXT 文件搜索插件", "搜索本地 D:/txt 目录下的 TXT 文件", "1.0.0")
class TxtSearchPlugin(Star):
    def __init__(self, context: Context):
        # 调用父类的构造方法进行初始化
        super().__init__(context)
        # 设置本地 TXT 文件的搜索目录
        self.txt_dir = 'D:/txt'

    # 使用 filter.command 装饰器注册指令
    @filter.command("search_txt")
    async def search_txt(self, event: AstrMessageEvent):
        # 获取消息发送者的名称
        sender_name = event.get_sender_name()
        print(f"消息由 {sender_name} 发送")

        # 获取消息内容（纯文本）
        message = event.get_plain_text()
        # 获取 AstrBotMessage 对象，查看消息适配器下发的消息具体内容
        bot_message = event.message_obj
        print(f"消息适配器下发的完整消息内容: {bot_message}")

        # 检查消息中是否包含书名号
        if '《' in message and '》' in message:
            # 提取书名
            start_index = message.index('《') + 1
            end_index = message.index('》')
            book_name = message[start_index:end_index]

            # 初始化一个空列表用于存储找到的 TXT 文件路径
            txt_files = []
            # 遍历指定目录及其子目录
            for root, dirs, files in os.walk(self.txt_dir):
                for file in files:
                    # 检查文件是否为 TXT 文件且包含书名
                    if file.endswith('.txt') and book_name in file:
                        txt_files.append(os.path.join(root, file))

            if txt_files:
                # 生成文件列表及编号
                file_list = []
                for i, file in enumerate(txt_files, start=1):
                    file_list.append(f"{i}. {os.path.basename(file)}")
                response = "找到以下 TXT 文件：\n" + "\n".join(file_list)
                # 发送包含文件列表的纯文本消息
                yield event.plain_result(response)
            else:
                # 若未找到相关文件，发送提示消息
                yield event.plain_result("未找到相关 TXT 文件。")
        else:
            # 若输入格式不正确，发送提示消息
            yield event.plain_result("请使用《书名》格式输入要搜索的书名。")

    # 使用 filter.command 装饰器注册指令
    @filter.command("send_txt")
    async def send_txt(self, event: AstrMessageEvent):
        # 获取消息发送者的名称
        sender_name = event.get_sender_name()
        print(f"消息由 {sender_name} 发送")

        # 获取消息内容（纯文本）
        message = event.get_plain_text()
        # 获取 AstrBotMessage 对象，查看消息适配器下发的消息具体内容
        bot_message = event.message_obj
        print(f"消息适配器下发的完整消息内容: {bot_message}")

        # 检查消息是否为有效的数字
        if message.isdigit():
            index = int(message) - 1
            # 初始化一个空列表用于存储所有 TXT 文件路径
            txt_files = []
            # 遍历指定目录及其子目录
            for root, dirs, files in os.walk(self.txt_dir):
                for file in files:
                    # 检查文件是否为 TXT 文件
                    if file.endswith('.txt'):
                        txt_files.append(os.path.join(root, file))
            if 0 <= index < len(txt_files):
                file_path = txt_files[index]
                try:
                    # 调用上下文的 send_file 方法发送文件（需根据实际情况实现）
                    await self.context.send_file(event, file_path)
                    # 发送文件已发送的提示消息
                    yield event.plain_result(f"已发送文件：{os.path.basename(file_path)}")
                except Exception as e:
                    # 若发送文件时出现错误，发送错误提示消息
                    yield event.plain_result(f"发送文件时出现错误：{str(e)}")
            else:
                # 若输入的编号无效，发送提示消息
                yield event.plain_result("无效的编号，请重新输入。")
        else:
            # 若输入不是有效的数字，发送提示消息
            yield event.plain_result("请输入有效的文件编号。")
