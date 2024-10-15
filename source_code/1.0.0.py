# To do list:
# 1. Stop observing button.
# 2. Output Counter.


# Import the modules
import tkinter as tk
import requests
import os
import pathlib
import json
import webbrowser


# Defined at the beginning
local_version = "1.0.0"
github_url = "https://github.com"
bilispace_url = "https://space.bilibili.com/"
rest_api = "https://api.github.com/repos/FiresJoeng/BFO/releases"
icon = "BFO.ico"


# Functions
def error_prompt(error_detail, fix_method):
    error_prompt_window = tk.Toplevel()
    error_prompt_window.attributes("-toolwindow", 1)
    error_prompt_window.grab_set()
    error_prompt_window.title("警告：BFO发生了一个错误！")

    screenwidth = error_prompt_window.winfo_screenwidth()
    screenheight = error_prompt_window.winfo_screenheight()
    error_prompt_window_size = "+%d+%d" % (screenwidth / 2, screenheight / 2)
    error_prompt_window.geometry(error_prompt_window_size)
    error_prompt_window.resizable(width=False, height=False)

    error_text_title = tk.StringVar()
    error_text_title.set(f'''错误详情：{error_detail}
    \n解决方案：{fix_method}''')
    update_title = tk.Label(error_prompt_window, textvariable=error_text_title, anchor=tk.W)
    update_title.pack()


def check_network(url_1, url_2):
    try:
        response_1 = requests.get(url_1)
        response_2 = requests.get(url_2)
        if response_1.status_code != 200 and response_2.status_code != 200:
            error_prompt("无法正常连接至服务器！", "似乎没有网络，请连接网络后再试！")
        else:
            pass
    except Exception as e:
        error_prompt(e, "与服务器的连接不稳定，请检查网络连接情况！")


def check_files():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = pathlib.Path(current_dir)
        if not path.joinpath("config.json").exists():  # Config.json was not found
            with open(path.joinpath("config.json"), "w", encoding="utf-8") as create_config:
                create_config.write("""{
    "UID":"433570990",
    "Delay":"15"
    }""")
        else:
            pass
        if not path.joinpath("output.txt").exists():
            with open(path.joinpath("output.txt"), "w", encoding="utf-8") as create_output:
                create_output.write("")
        else:
            pass
    except Exception as e:
        error_prompt(e, "检查配置文件时出现问题，请给予本程序一定权限，并且不要破坏文件完整性！")


def save_files(input_uid, input_delay):
    try:
        check_files()
        with open("config.json", "r", encoding="utf-8") as read_config:
            config_content = json.load(read_config)
        config_content["UID"] = input_uid
        config_content["Delay"] = input_delay
        with open("config.json", "w", encoding="utf-8") as write_config:
            json.dump(config_content, write_config)
    except Exception as e:
        error_prompt(e, "写入配置文件时出现问题，请给予本程序一定权限，并且不要破坏文件完整性！")


# Calling at beginning
check_network(github_url, bilispace_url)
print("提示：请勿关闭此窗口，此窗口为程序核心，且此窗口会输出部分信息！")


# Main window UI
class BFO:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Bilibili Followers Observer")
        self.main_window.resizable(width=False, height=False)
        screenwidth = self.main_window.winfo_screenwidth()
        screenheight = self.main_window.winfo_screenheight()
        main_window_size = "%dx%d+%d+%d" % (460, 150, (screenwidth - 460) / 2, (screenheight - 150) / 2)
        self.main_window.geometry(main_window_size)

        self.update_check_text_title = tk.StringVar()
        self.update_check_text_title.set(f"Version {local_version}")
        self.update_check_text = tk.Label(self.main_window, textvariable=self.update_check_text_title, anchor=tk.E)
        self.update_check_text.place(x=350, y=120, width=100, height=20)

        self.uid_text_title = tk.StringVar()
        self.uid_text_title.set("监视UID: ")
        self.uid_text = tk.Label(self.main_window, textvariable=self.uid_text_title, anchor=tk.W)
        self.uid_text.place(x=10, y=10, width=200, height=20)

        self.delay_text_title = tk.StringVar()
        self.delay_text_title.set("抓取频率(单位: 秒/次): ")
        self.delay_text = tk.Label(self.main_window, textvariable=self.delay_text_title, anchor=tk.W)
        self.delay_text.place(x=250, y=10, width=200, height=20)

        try:
            check_files()
            with open("config.json", "r", encoding="utf-8") as read_config:
                config_content = json.load(read_config)
                default_uid = config_content.get("UID", "警告：无法正常读取配置文件！")
                default_delay = config_content.get("Delay", "请删除该程序目录下的”config.json“")
        except Exception as e:
            error_prompt(e, "读取配置文件时出现问题，请给予本程序一定权限，并且不要破坏文件完整性！")

        self.uid_input_default = tk.StringVar()
        self.uid_input_default.set(default_uid)
        self.uid_input = tk.Entry(self.main_window, textvariable=self.uid_input_default, justify=tk.LEFT)
        self.uid_input.place(x=10, y=40, width=200, height=20)

        self.delay_input_default = tk.StringVar()
        self.delay_input_default.set(default_delay)
        self.delay_input = tk.Entry(self.main_window, textvariable=self.delay_input_default, justify=tk.LEFT)
        self.delay_input.place(x=250, y=40, width=200, height=20)

        self.confirm_button_title = tk.StringVar()
        self.confirm_button_title.set("开始抓取")
        self.confirm_button = tk.Button(
            self.main_window, textvariable=self.confirm_button_title, command=self.start_observer)
        self.confirm_button.place(x=10, y=80, width=130, height=30)

        self.help_button_title = tk.StringVar()
        self.help_button_title.set("使用帮助")
        self.help_button = tk.Button(self.main_window, textvariable=self.help_button_title, command=self.get_help)
        self.help_button.place(x=165, y=80, width=130, height=30)

        self.update_button_title = tk.StringVar()
        self.update_button_title.set("检查更新")
        self.update_button = tk.Button(
            self.main_window, textvariable=self.update_button_title, command=self.check_update)
        self.update_button.place(x=320, y=80, width=130, height=30)

    def start_observer(self):
        self.confirm_button.config(state=tk.DISABLED)
        self.uid_input.config(state=tk.DISABLED)
        self.delay_input.config(state=tk.DISABLED)
        save_files(self.uid_input.get(), self.delay_input.get())
        with open("config.json", "r", encoding="utf-8") as read_config:
            config_content = json.load(read_config)
        load_uid = config_content["UID"]
        load_delay = config_content["Delay"]
        bilibili_api = str(f"https://api.bilibili.com/x/relation/stat?vmid={load_uid}&jsonp=jsonp")

        try:
            response = requests.get(bilibili_api)
            if response.status_code != 200:
                print("[警告] 本次抓取失败......")
            else:
                data = json.loads(response.text)["data"]
                follower = str(data["follower"])
                print("[输出] 当前粉丝数为："+follower)
                with open("output.txt", "w", encoding="utf-8") as write_output:
                    write_output.write(follower)
            self.main_window.after(int(load_delay) * 1000, self.start_observer)
        except Exception as e:
            error_prompt(e, "请检查输入框内的内容是否为纯数字，然后再试一次！")

    def get_help(self):
        help_window = tk.Toplevel(self.main_window)
        help_window.attributes("-toolwindow", 1)
        help_window.grab_set()
        help_window.title("使用帮助")
        help_window.resizable(width=False, height=False)
        help_window.geometry("+%d+%d" % (self.main_window.winfo_x() + 100, self.main_window.winfo_y() + 50))

        help_text_title = tk.StringVar()
        help_text_title.set('''OBS文本源导入本程序目录下“output.txt”即可使用。
        \n更多详细信息请前往：github.com/FiresJoeng/BFO
        \n©2023 Fires Joeng''')
        help_title = tk.Label(help_window, textvariable=help_text_title, anchor=tk.W)
        help_title.pack()

    def check_update(self):
        try:
            response = requests.get(rest_api)
            if response.status_code != 200:
                error_prompt(f"来自GitHub的响应异常！状态码：{str(response.status_code)}", "与服务器的连接不稳定，请检查网络连接情况！")
            else:
                release_version = json.loads(response.text)[0]["tag_name"]
                if local_version < release_version:  # New version available
                    release_url = f"https://github.com/FiresJoeng/BFO/releases/tag/{release_version}"
                    update_window = tk.Toplevel(self.main_window)
                    update_window.attributes("-toolwindow", 1)
                    update_window.grab_set()
                    update_window.title("新的更新可用！")
                    update_window.resizable(width=False, height=False)
                    update_window.geometry("+%d+%d" % (
                        self.main_window.winfo_x() + 100, self.main_window.winfo_y() + 50))

                    update_text_title = tk.StringVar()
                    update_text_title.set(f'''当前版本：{local_version}
                            \n最新版本：{release_version}
                            \n是否跳转至GitHub查看更新？''')
                    update_title = tk.Label(update_window, textvariable=update_text_title, anchor=tk.W)
                    update_title.pack()

                    get_update_button = tk.Button(
                        update_window, text="  更新  ",
                        command=lambda: webbrowser.open(release_url))
                    get_update_button.pack(side=tk.LEFT, padx=10)

                    ignore_update_button = tk.Button(
                        update_window, text="  忽略  ",
                        command=update_window.destroy)
                    ignore_update_button.pack(side=tk.RIGHT, padx=10)

                else:
                    update_window = tk.Toplevel(self.main_window)
                    update_window.attributes("-toolwindow", 1)
                    update_window.grab_set()
                    update_window.title("暂无新的更新！")
                    update_window.resizable(width=False, height=False)
                    update_window.geometry("+%d+%d" % (
                        self.main_window.winfo_x() + 100, self.main_window.winfo_y() + 50))

                    update_text_title = tk.StringVar()
                    update_text_title.set(f'''当前版本：v{local_version}
                            \n最新版本：v{release_version}
                            \n您已是最新版本！''')
                    update_title = tk.Label(update_window, textvariable=update_text_title, anchor=tk.W)
                    update_title.pack()

                    ignore_update_button = tk.Button(
                        update_window, text="  关闭  ",
                        command=update_window.destroy)
                    ignore_update_button.pack(side=tk.BOTTOM, padx=10)
        except Exception as e:
            error_prompt(e, "似乎没有网络，请连接网络后再试！")


if __name__ == "__main__":
    root = tk.Tk()
    app = BFO(root)
    try:
        root.iconbitmap(icon)
    except tk.TclError as icon_not_found:
        error_prompt("缺少文件："+str(icon), "建议前往GitHub完整下载本程序！")
    root.mainloop()
