from enum import Enum

class InvestorProfile(str, Enum):
    CONSERVATIVE = 'CONSERVADOR' 
    MODERATE = 'MODERADO'  
    BOLD = 'ARROJADO' 
    UNDEFINED = 'Indefinido'

class InvestmentType(str, Enum):
    STOCKS = 'AÇÕES'
    CRYPTO = 'CRIPTO'
    FUNDS = 'FUNDOS'
    FIXED_INCOME = 'RENDA_FIXA'