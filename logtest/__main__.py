#!/usr/bin/python3

from app import *


def main():

    root = Tk()
    app = App()
    app.init_widgets(root)
    root.mainloop()

    # root.title("日志分析")
    # root.geometry("1000x500")
    #
    # select_file_button = Button(root,text="选择日志文件")
    # select_file_button["command"] = lambda:selected_logfile(select_file_button)
    # select_file_button.pack()
    # info_label = Label(root, text="日志解析完成后，会在该应用同级目录生成结果文件：logText.txt")
    # info_label.pack()
    #
    # quit_Button = Button(root, text="退出程序",
    #                       command=lambda :exit(root))
    # quit_Button.pack()
    # root.mainloop()


if __name__ == '__main__':
    main()




