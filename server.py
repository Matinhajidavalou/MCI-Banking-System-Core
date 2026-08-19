import socket
import threading
import json
from bank import Bank

def handle_client(conn, addr, bank):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            try:
                bank.load_data()
            except:
                pass
            
            request = json.loads(data.decode('utf-8'))
            action = request.get('action')
            acc_num = request.get('account')
            
            account = bank.accounts.get(acc_num)
            if not account:
                conn.send(json.dumps({"status": "error", "message": "حساب یافت نشد"}).encode('utf-8'))
                continue

            if action == 'balance':
                conn.send(json.dumps({"status": "success", "balance": float(account.get_balance())}).encode('utf-8'))
            
            elif action == 'deposit':
                amount = float(request.get('amount'))
                account.deposit(amount)
                bank.save_data()
                conn.send(json.dumps({"status": "success"}).encode('utf-8'))
                
            elif action == 'withdraw':
                amount = float(request.get('amount'))
                try:
                    account.withdraw(amount)
                    bank.save_data()
                    conn.send(json.dumps({"status": "success"}).encode('utf-8'))
                except Exception as e:
                    conn.send(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                    
        except:
            break
            
    conn.close()

def start_server():
    bank = Bank()
    bank.load_data()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5050))
    server.listen()
    
    print("  روی پورت 5050 روشن شد...")
    print("منتظر اتصال کلاینت‌ها (ATM)...\n")
    
    while True:
        conn, addr = server.accept()
        print(f"[+] اتصال جدید از: {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr, bank))
        thread.start()

if __name__ == "__main__":
    start_server()