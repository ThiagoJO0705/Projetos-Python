from enum import Enum

class AssetType(str, Enum):
    STOCKS = 'AÇÕES'
    FII = 'FII'
    CRYPTO = 'CRIPTO'
    
class TransactionType(str, Enum):
    BUY = 'COMPRA' 
    SELL     = 'VENDA'   
    