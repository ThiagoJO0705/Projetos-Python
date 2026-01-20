from enum import Enum

class ProfileInvestor(str, Enum):
    CONSERVATIVE = 'CONSERVADOR' 
    MODERATE = 'MODERADO'  
    BOLD = 'ARROJADO' 

class InvestmentType(str, Enum):
    STOCKS = 'AÇÕES'
    CRYPTO = 'CRIPTO'
    FUNDS = 'FUNDOS'
    FIXED_INCOME = 'RENDA_FIXA'