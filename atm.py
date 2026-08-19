import socket
import json
import time

def run_atm():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5050))
    except:
        print("خطا: ارتباط با سرور مرکزی برقرار نشد.")
        return

    while True:
        print("\n" + "="*50)
        print(" سیستم خودپرداز متصل به سرور مرکزی ")
        print("="*50)

        account_num = input("لطفاً شماره حساب ۸ رقمی خود را وارد کنید (یا 'q' برای خاموش کردن): ").strip()
        
        if account_num.lower() == 'q':
            print("\nدستگاه خودپرداز خاموش میشود...")
            client.close()
            break

        while True:
            print("\n" + "-"*15 + " منوی عملیات " + "-"*15)
            print("۱. مشاهده موجودی")
            print("۲. واریز وجه")
            print("۳. برداشت وجه")
            print("۴. خروج")
            
            choice = input("\nانتخاب شما: ").strip()
            
            if choice == '1':
                req = {"action": "balance", "account": account_num}
                client.send(json.dumps(req).encode('utf-8'))
                resp = json.loads(client.recv(1024).decode('utf-8'))
                if resp.get("status") == "success":
                    print(f"\nموجودی فعلی شما: {resp.get('balance')} تومان")
                else:
                    print(f"\nخطا: {resp.get('message')}")
                    
            elif choice == '2':
                amount = input("مبلغ واریز (تومان): ").strip()
                req = {"action": "deposit", "account": account_num, "amount": amount}
                client.send(json.dumps(req).encode('utf-8'))
                resp = json.loads(client.recv(1024).decode('utf-8'))
                if resp.get("status") == "success":
                    print("\nواریز با موفقیت انجام شد.")
                else:
                    print(f"\nخطا: {resp.get('message')}")
                    
            elif choice == '3':
                amount = input("مبلغ برداشت (تومان): ").strip()
                req = {"action": "withdraw", "account": account_num, "amount": amount}
                client.send(json.dumps(req).encode('utf-8'))
                resp = json.loads(client.recv(1024).decode('utf-8'))
                if resp.get("status") == "success":
                    print("\nبرداشت با موفقیت انجام شد.")
                else:
                    print(f"\nخطا: {resp.get('message')}")
                    
            elif choice == '4':
                print("\nکارت خود را بردارید.")
                time.sleep(2)
                break

if __name__ == "__main__":
    run_atm()