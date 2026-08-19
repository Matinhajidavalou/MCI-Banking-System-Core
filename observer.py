from abc import ABC, abstractmethod
import logging

class TransactionObserver(ABC):
    @abstractmethod
    def update(self, transaction):
        pass

class ConsoleObserver(TransactionObserver):
    def update(self, transaction):
        try:
            print(f"[اعلان سیستم] تراکنش {transaction.transaction_type.value} به مبلغ {transaction.amount} ثبت شد. (وضعیت: {transaction.status.value})")
        except Exception:
            pass

class FileLoggerObserver(TransactionObserver):
    def __init__(self, filename="transactions.log"):
        self.filename = filename
        logging.basicConfig(
            filename=self.filename,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            encoding='utf-8'
        )

    def update(self, transaction):
        try:
            log_msg = f"شناسه: {transaction.transaction_id} | نوع: {transaction.transaction_type.value} | مبلغ: {transaction.amount} | مبدأ: {transaction.source_account} | مقصد: {transaction.target_account} | وضعیت: {transaction.status.value}"
            logging.info(log_msg)
        except Exception:
            pass

class EventManager:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, transaction):
        for observer in self._observers:
            try:
                observer.update(transaction)
            except Exception:
                pass