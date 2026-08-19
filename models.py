from abc import ABC
from decimal import Decimal
from enum import Enum
from datetime import datetime
import uuid
import threading

class Transaction_type(Enum):
    DEPOSIT = "واریز"
    WITHDRAW = "برداشت"
    TRANSFER = "انتقال"

class Transaction_status(Enum):
    SUCCESS = "موفق"
    FAILED = "ناموفق"    

class Transaction:
    def __init__(self, amount, transaction_type, status, source_account=None, target_account=None, description=""):
        self.transaction_id = str(uuid.uuid4())[:8] 
        self.amount = Decimal(str(amount))
        self.transaction_type = transaction_type
        self.datetime = datetime.now()
        self.source_account = source_account
        self.target_account = target_account
        self.status = status
        self.description = description

class Customer:
    def __init__(self, name, national_id):
        self.name = name
        self.national_id = national_id
        self.accounts = []
        
    def add_account(self, account):
        self.accounts.append(account)

class Account(ABC):
    def __init__(self, account_number, owner, balance=Decimal("0.00")):
        self.account_number = account_number
        self.owner = owner
        self.__balance = Decimal(str(balance))
        self.transaction_history = []
        self.lock = threading.RLock()

    def get_balance(self):
        return self.__balance
    
    def deposit(self, amount):
        amt_decimal = Decimal(str(amount))
        if amt_decimal <= Decimal("0.00"):
            raise ValueError("مقدار واریزی باید بیشتر از صفر باشد.")
            
        with self.lock:
            self.__balance += amt_decimal
            new_transaction = Transaction(amt_decimal, Transaction_type.DEPOSIT, Transaction_status.SUCCESS, source_account=None, target_account=self.account_number, description="واریز موفق")
            self.transaction_history.append(new_transaction)

    def withdraw(self, amount):
        amt_decimal = Decimal(str(amount))
        if amt_decimal <= Decimal("0.00"):
            raise ValueError("مقدار برداشت باید بیشتر از صفر باشد.")
        
        with self.lock:
            if amt_decimal > self.__balance:
                failed_transaction = Transaction(amt_decimal, Transaction_type.WITHDRAW, Transaction_status.FAILED, source_account=self.account_number, target_account=None, description="تراکنش ناموفق به دلیل موجودی ناکافی")
                self.transaction_history.append(failed_transaction)
                raise ValueError("موجودی کافی نیست.")
            
            self.__balance -= amt_decimal
            new_transaction = Transaction(amt_decimal, Transaction_type.WITHDRAW, Transaction_status.SUCCESS, source_account=self.account_number, target_account=None, description="برداشت موفق")
            self.transaction_history.append(new_transaction)

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'lock' in state:
            del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        import threading
        self.lock = threading.RLock()

class SavingsAccount(Account):
    def __init__(self, account_number, owner, balance=Decimal("0.00"), interest_rate=Decimal("0.00")):
        super().__init__(account_number, owner, balance)
        self.interest_rate = Decimal(str(interest_rate))

    def calculate_interest(self):
        return self.get_balance() * self.interest_rate  

class CheckingAccount(Account):
    def __init__(self, account_number, owner, fee_rate=Decimal("0.01"), balance=Decimal("0.00")):
        super().__init__(account_number, owner, balance)
        self.fee_rate = Decimal(str(fee_rate))

    def withdraw(self, amount):
        amt_decimal = Decimal(str(amount))
        fee = amt_decimal * self.fee_rate
        total_amount = amt_decimal + fee
        
        if total_amount > self.get_balance():
            raise ValueError("موجودی کافی برای برداشت و کسر کارمزد نیست.")
            
        super().withdraw(total_amount)