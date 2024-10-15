# To do list:
# 1. Set an icon.
# 2. Check update function.
# 3. Load json memory. Entry Fires's UID and default delay (15) if no contents in the input boxes.
# 4. Stop observing button.
# 5. Log output.
# 6. Error dialog window.


# Import the modules
import tkinter as tk
import requests
import os
import pathlib
import json
import webbrowser


# Functions
def check_network(url_1, url_2):
    try:
        response_1 = requests.get(url_1)
        response_2 = requests.get(url_2)
        if response_1.status_code != 200 and response_2.status_code != 200:
            print("警告：无法正常连接至服务器，请检查网络！")
            exit()
        else:
            pass
    except Exception as e:
        print("错误：网络连接失败！")
        print("ERROR: " + str(e))
        pass


def check_files():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = pathlib.Path(current_dir)
        if not path.joinpath("config.json").exists():
            with open(path.joinpath("config.json"), "w", encoding="utf-8") as create_config:
                create_config.write("""{
    "UID":"433570990",
    "Delay":"15",
    "Version":"0.2"
    }""")
        else:
            pass
        if not path.joinpath("output.txt").exists():
            with open(path.joinpath("output.txt"), "w", encoding="utf-8") as create_output:
                create_output.write("")
        else:
            pass
    except Exception as e:
        print("ERROR:" + str(e))
        exit()


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
        print("ERROR: " + str(e))
        exit()


def error_prompt():
    pass


# Calling at beginning
github_url = "https://github.com"
bilispace_url = "https://space.bilibili.com/"
check_network(github_url, bilispace_url)


# Main window UI
class BFO:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("BFO: 当前版本为测试版!")
        self.main_window.resizable(width=False, height=False)
        screenwidth = self.main_window.winfo_screenwidth()
        screenheight = self.main_window.winfo_screenheight()
        window_size = "%dx%d+%d+%d" % (460, 150, (screenwidth - 460) / 2, (screenheight - 150) / 2)
        self.main_window.geometry(window_size)

        self.update_check_text_title = tk.StringVar()
        self.update_check_text_title.set("Version 0.2")
        self.update_check_text = tk.Label(self.main_window, textvariable=self.update_check_text_title, anchor=tk.E)
        self.update_check_text.place(x=350, y=120, width=100, height=20)

        self.uid_text_title = tk.StringVar()
        self.uid_text_title.set("监视UID: ")
        self.uid_text = tk.Label(self.main_window, textvariable=self.uid_text_title, anchor=tk.W)
        self.uid_text.place(x=10, y=10, width=200, height=20)

        self.uid_input_default = tk.StringVar()
        self.uid_input_default.set("433570990")
        self.uid_input = tk.Entry(self.main_window, textvariable=self.uid_input_default, justify=tk.LEFT)
        self.uid_input.place(x=10, y=40, width=200, height=20)

        self.delay_text_title = tk.StringVar()
        self.delay_text_title.set("抓取频率(秒/次): ")
        self.delay_text = tk.Label(self.main_window, textvariable=self.delay_text_title, anchor=tk.W)
        self.delay_text.place(x=250, y=10, width=200, height=20)

        self.delay_input_default = tk.StringVar()
        self.delay_input_default.set("15")
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
            self.main_window, textvariable=self.update_button_title, command=self.check_update, state=tk.DISABLED)
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
                print("提示：抓取失败！")
            else:
                data = json.loads(response.text)["data"]
                follower = str(data["follower"])
                print("提示：当前粉丝数为"+follower)
                with open("output.txt", "w", encoding="utf-8") as write_output:
                    write_output.write(follower)
            self.main_window.after(int(load_delay) * 1000, self.start_observer)
        except Exception as e:
            print("ERROR: " + str(e))
            exit()

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
        local_version = "0.2"
        rest_api = 'https://api.github.com/repos/FiresJoeng/BFO/releases'

        try:
            response = requests.get(rest_api)
            if response.status_code != 200:
                print("警告：无法正常连接至服务器，请检查网络！")
                exit()
            else:
                release_version = json.loads(response.text)["tag_name"]
                if int(local_version) < int(release_version):  # New version available
                    release_url = f"https://github.com/FiresJoeng/BFO/releases/tag/{release_version}"
                    webbrowser.open(release_url)
                else:
                    pass
        except Exception as e:
            print("ERROR: " + str(e))
            exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = BFO(root)
    root.mainloop()
