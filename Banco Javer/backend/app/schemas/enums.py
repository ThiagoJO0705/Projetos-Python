from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    PIX = 'PIX'
    TED = 'TED'
    TEF = 'TEF'
    BANK_SLIP = 'BANK SLIP'

class TransactionDirection(str, Enum):
    CREDIT = 'CREDIT' 
    DEBIT = 'DEBIT'   
    