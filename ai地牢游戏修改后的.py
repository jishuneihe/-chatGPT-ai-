import tkinter as tk
from tkinter import messagebox
from openai import OpenAI

# 创建主窗口
root = tk.Tk()
root.title("AI 地牢游戏")
# 设置主窗口背景色为黑色
root.configure(bg="#000000")

# 全局变量
api_key = ""
messages = []
client = None

# 定义文字颜色为白色，背景颜色为黑色
text_color = "#FFFFFF"
bg_color = "#000000"

# 输入 API 密钥
api_key_label = tk.Label(root, text="请输入 ChatGPT API 密钥:", fg=text_color, bg=bg_color)
api_key_label.pack(pady=5)
api_key_entry = tk.Entry(root, width=50, fg=text_color, bg=bg_color)
api_key_entry.pack(pady=5)

# 输入喜好
preference_label = tk.Label(root, text="请输入你的喜好:", fg=text_color, bg=bg_color)
preference_label.pack(pady=5)
preference_entry = tk.Entry(root, width=50, fg=text_color, bg=bg_color)
preference_entry.pack(pady=5)

# 聊天记录显示框
chat_history_text = tk.Text(root, height=20, width=80, fg=text_color, bg=bg_color)
chat_history_text.pack(pady=10)

# 输入框
input_entry = tk.Entry(root, width=50, fg=text_color, bg=bg_color)
input_entry.pack(pady=5)

# 初始化 API 客户端
def init_client():
    global api_key, client
    api_key = api_key_entry.get()
    if not api_key:
        messagebox.showwarning("警告", "请输入有效的 API 密钥！")
        return
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.chatanywhere.tech/v1"
        )
        preference = preference_entry.get()
        if not preference:
            messagebox.showwarning("警告", "请输入你的喜好！")
            return
        start_game(preference)
    except Exception as e:
        messagebox.showerror("错误", f"初始化客户端失败: {str(e)}")

# 开始游戏
def start_game(preference):
    global messages
    messages = [
        {"role": "system", "content": "你正在进行一个 AI 地牢游戏，根据用户的喜好生成一个故事，并和用户轮流对话推进剧情。"},
        {"role": "user", "content": f"我的喜好是 {preference}，请开始一个故事。"}
    ]
    get_ai_response()

# 获取 AI 回复
def get_ai_response():
    global messages
    try:
        stream = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            stream=True,
        )
        response = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        messages.append({"role": "assistant", "content": response})
        chat_history_text.insert(tk.END, f"AI: {response}\n")
    except Exception as e:
        messagebox.showerror("错误", f"获取 AI 回复失败: {str(e)}")

# 发送用户消息
def send_user_message():
    global messages
    user_message = input_entry.get()
    if not user_message:
        messagebox.showwarning("警告", "请输入你的消息！")
        return
    messages.append({"role": "user", "content": user_message})
    chat_history_text.insert(tk.END, f"你: {user_message}\n")
    input_entry.delete(0, tk.END)
    get_ai_response()

# 开始按钮
start_button = tk.Button(root, text="开始游戏", command=init_client, fg=text_color, bg=bg_color)
start_button.pack(pady=5)

# 发送按钮
send_button = tk.Button(root, text="发送", command=send_user_message, fg=text_color, bg=bg_color)
send_button.pack(pady=5)

root.mainloop()