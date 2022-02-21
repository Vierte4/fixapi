class User():
    def __init__(
		self, 
        senderCompID, 
        targetCompID, 
        host, 
        port,
        username,
        password,
        fixversion='FIX.4.4',
    ):
        self.senderCompID=senderCompID
        self.targetCompID=targetCompID
        self.host=host
        self.port=port
        self.fixversion=fixversion
        self.username=username
        self.password=password


demo1 = User(
	senderCompID='demo.ctrader.3454732',
    targetCompID='CSERVER',
    host='h28.p.ctrader.com',
    port=5202,
    username=3454732,
    password=3454732)

"""Имя хоста: h28.p.ctrader.com
(ваш текущий IP-адрес 80.86.83.5 может быть изменен без предупреждения)
Порт: 5212 (SSL), 5202 (обыкновенный текст).
Пароль: (пароль счета 3454732)
SenderCompID: demo.ctrader.3454732
TargetCompID: CSERVER
SenderSubID: TRADE"""