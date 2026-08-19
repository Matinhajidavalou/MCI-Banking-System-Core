class BankException(Exception):
    pass

class InsufficientFundsException(BankException):
    pass

class InvalidAmountException(BankException):
    pass

class AccountNotFoundException(BankException):
    pass

class CustomerNotFoundException(BankException):
    pass

class TransferToSameAccountException(BankException):
    pass

class PersistenceException(BankException):
    pass