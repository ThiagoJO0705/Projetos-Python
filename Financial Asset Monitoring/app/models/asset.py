from sqlalchemy import Column, Integer, String, Enum
from app.schemas.enums import AssetType
from app.dbconfig import Base

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(Enum(AssetType), nullable=False)

    def __init__(self, ticker, name, type):
        self.ticker = ticker
        self.name = name
        self.type = type