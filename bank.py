import threading
import pickle
import datetime
import time
import random
from decimal import Decimal
from models import Customer, SavingsAccount, CheckingAccount
from exceptions import (PersistenceException, TransferToSameAccountException, 
                        AccountNotFoundException, InvalidAmountException)

class Bank:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.customers = {}
            self.accounts = {}
            self.bank_lock = threading.RLock()
            self.initialized = True

    def create_customer(self, name, national_id):
        if not national_id.isdigit() or len(national_id) != 10:
            raise ValueError("کد ملی باید دقیقاً ۱۰ رقم و فقط شامل اعداد باشد.")
            
        with self.bank_lock:
            if national_id in self.customers:
                raise ValueError("مشتری با این کد ملی از قبل وجود دارد.")
            customer = Customer(name, national_id)
            self.customers[national_id] = customer
            return customer

    def open_account(self, national_id, account_type, **kwargs):
        if not national_id.isdigit() or len(national_id) != 10:
            raise ValueError("کد ملی باید دقیقاً ۱۰ رقم باشد.")
            
        with self.bank_lock:
            if national_id not in self.customers:
                raise ValueError("مشتری با این کد ملی وجود ندارد.")
            
            customer = self.customers[national_id]
            
            while True:
                account_number = str(random.randint(10000000, 99999999))
                if account_number not in self.accounts:
                    break
            
            if account_type == "savings":
                interest_rate = kwargs.get("interest_rate", "0.20")
                account = SavingsAccount(account_number, customer, interest_rate=interest_rate)
            elif account_type == "checking":
                fee_rate = kwargs.get("fee_rate", "0.01")
                account = CheckingAccount(account_number, customer, fee_rate=fee_rate)
            else:
                raise ValueError("نوع حساب نامعتبر است.")
            
            self.accounts[account_number] = account
            customer.add_account(account)
            
            with open('transactions.log', 'a', encoding='utf-8') as f:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{now}] افتتاح حساب {account_type}: شماره {account_number} برای مشتری {national_id}\n")
                
            return account

    def transfer_funds(self, source_acc_number, dest_acc_number, amount):
        amount_dec = Decimal(str(amount))
        if amount_dec <= 0:
            raise InvalidAmountException("مبلغ انتقال باید معتبر و مثبت باشد.")
            
        if source_acc_number == dest_acc_number:
            raise TransferToSameAccountException("انتقال به همان حساب مجاز نیست.")
            
        source_account = self.accounts.get(source_acc_number)
        dest_account = self.accounts.get(dest_acc_number)
        
        if not source_account or not dest_account:
            raise AccountNotFoundException("حساب مبدأ یا مقصد یافت نشد.")

        if source_account.account_number < dest_account.account_number:
            first_lock = source_account.lock
            second_lock = dest_account.lock
        else:
            first_lock = dest_account.lock
            second_lock = source_account.lock

        with first_lock:
            with second_lock:
                source_account.withdraw(amount_dec)
                dest_account.deposit(amount_dec)
                
                with open('transactions.log', 'a', encoding='utf-8') as f:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{now}] انتقال وجه موفق: {amount_dec} تومان از {source_acc_number} به {dest_acc_number}\n")

    def start_interest_task(self):
        thread = threading.Thread(target=self._apply_interest_periodically, daemon=True)
        thread.start()

    def _apply_interest_periodically(self):
        while True:
            time.sleep(90)
            with self.bank_lock:
                for acc_num, account in self.accounts.items():
                    if isinstance(account, SavingsAccount):
                        interest = account.calculate_interest()
                        if interest > 0:
                            account.deposit(interest)
                            with open('transactions.log', 'a', encoding='utf-8') as f:
                                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                f.write(f"[{now}] واریز خودکار سود سیستمی: {interest} تومان به حساب {acc_num}\n")
                try:
                    self.save_data()
                except:
                    pass

    def save_data(self, filename="bank_data.pkl"):
        with self.bank_lock:
            try:
                with open(filename, 'wb') as file:
                    data_to_save = {
                        'customers': self.customers,
                        'accounts': self.accounts
                    }
                    pickle.dump(data_to_save, file)
            except Exception as e:
                raise PersistenceException(f"خطا در ذخیره داده‌ها: {e}")
            
    def load_data(self, filename="bank_data.pkl"):
        with self.bank_lock:
            try:
                with open(filename, 'rb') as file:
                    loaded_data = pickle.load(file)
                    self.customers = loaded_data.get('customers', {})
                    self.accounts = loaded_data.get('accounts', {})
            except FileNotFoundError:
                pass
            except Exception as e:
                raise PersistenceException(f"خطا در بارگذاری داده‌ها: {e}")