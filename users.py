from dataclasses import dataclass


@dataclass
class User:
    senderCompID: str
    targetCompID: str
    host: str
    port: int
    username: str
    password: str
    fixversion: str = 'FIX.4.4'

# Демосчёт для тестов
demo1 = User(
    senderCompID='demo.ctrader.3463849',
    targetCompID='CSERVER',
    host='h51.p.ctrader.com',
    port=5202,
    username='3463849',
    password='3463849')
