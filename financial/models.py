from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import app
from .config import settings


app.config['SQLALCHEMY_DATABASE_URI'] = settings.POSTGRE_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class FinancialData(db.Model):
    __tablename__ = 'financial_data'

    symbol = db.Column(db.String(10), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    open_price = db.Column(db.Numeric(10, 2), nullable=False)
    close_price = db.Column(db.Numeric(10, 2), nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)

    def __init__(self, symbol, date, open_price, close_price, volume):
        self.symbol = symbol
        self.date = date
        self.open_price = open_price
        self.close_price = close_price
        self.volume = volume

    def __repr__(self):
        return f"<FinancialData(symbol={self.symbol}, date={self.date}, open_price={self.open_price}, close_price={self.close_price}, volume={self.volume})>"
    
