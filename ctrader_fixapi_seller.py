import logging
import socket
from datetime import datetime


class FixApi():
    def __init__(
            self,
            senderCompID,
            targetCompID,
            host,
            port,
            fixversion='FIX.4.4',
            time_in_ms=True):
        self.fixversion = fixversion
        self.senderCompID = senderCompID  # id клиента
        self.targetCompID = targetCompID  # id сервера
        self.len_position = len(f'8={self.fixversion}')
        self.msgSeqNum = 1  # int
        self.time_in_ms = time_in_ms  # время в мс, если True, иначе в секундах

        self.logger = logging.getLogger("CtraderSellerOrder")
        self.host = host
        self.port = port

    def start_logging(self):
        logging.basicConfig()
        self.logger.setLevel("INFO")

    def get_format_time(self):
        """Возвращет текущие дату и время"""
        if self.time_in_ms:
            return datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        else:
            return datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")

    def create_fix_api_format(self, kwargs: dict):
        """Получает словарь и формирует из него fix message следующего вида:
            ключ1=значение1|ключ2=значение2|...|ключN=значениеN
            Возвращает fix message"""
        message_items = kwargs.items()
        message_list = ['{}={}'.format(a[0], a[1]) for a in message_items]
        message = '|'.join(message_list)
        return message

    def create_tail(self, s: str):
        """Считает контрольную сумму сообщения и формирует из неё '
            хвост', который возвращает"""
        sum_ascii = 0
        s = s.replace("|", "\u0001")
        for c in s:
            sum_ascii += ord(c)
        control_sum = str(sum_ascii % 256)

        while len(control_sum) < 3:
            control_sum = '0' + control_sum
        tail = '10=' + control_sum + '|'

        return tail

    def create_header(self, message_type: str):
        """Создаёт и возвращает header"""
        time = self.get_format_time()
        header = {
            8: self.fixversion,
            35: message_type,
            49: self.senderCompID,
            56: self.targetCompID,
            34: self.msgSeqNum,
            52: time}
        return header

    def create_request(self, message: dict, message_type: str):
        """Формирует и возвращает готовый запрос"""
        message = self.create_fix_api_format(message)
        header = self.create_header(message_type)
        header = self.create_fix_api_format(header)
        msg = header + '|' + message
        len_msg = len(msg[self.len_position:])
        request = msg[:self.len_position] + f'|9={len_msg}' \
                  + msg[self.len_position:] + '|'
        request += self.create_tail(request)
        return request

    def parse_fix_message(self, message):
        """Превращает fix запрос в словарь, который возвращает"""
        message = message.split('\u0001')[:-1]
        message = {a[0]: a[1] for a in [b.split('=') for b in message]}
        return message

    def connect_to_serv(self):
        """Выполняет подключение к серверу и создание socket клиента"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        try:
            self.sock.connect((self.host, self.port))
        except:
            return 'Превышено времяя ожидания ответа от сервера'

    def disconnect_from_serv(self):
        self.sock.close()

    def send_to_serv(self, message, message_type):
        """Переводит message в биты, отправляет на сервер
            и возвращает ответ"""
        print(message)
        message = str(message).replace("|", "\u0001")
        message = message.encode()

        try:
            self.sock.send(message)
            response = self.sock.recv(65535).decode()

        except Exception as e:
            e = f'Exception: {e}'
            self.logger.info(e)
            return e
        formated_response = self.parse_fix_message(response)

        if not formated_response:
            self.logger.info("Ошибка! Сообщение не получено")
            return
        answer = formated_response.get('58')
        self.logger.info(f"{message_type}: {answer if answer else 'Success'}")

        self.msgSeqNum += 1

        return formated_response

    def create_logon_req(self, username, password):
        """Выполняет подключение к потоку"""

        request = self.create_request(
            message={57: 'TRADE', 98: 0, 108: 0, 141: 'Y', 553: username,
                     554: password},
            message_type='A',
        )

        return request

    def create_logout_req(self):
        """Выполняет отключение от потока"""

        request = self.create_request(
            message={57: 'TRADE'},
            message_type=5,
        )

        return request

    def create_order_req(
            self,
            order_id,  # id заявки
            symbol_id,  # id символа
            action,  # buy или sell
            qty,  # количество
            order_type='market',  # market, limit или stop
            price='Market',  # указывать только при order_type = limit
            st_price='None'  # указывать только при order_type = stop
    ):
        """Создаёт и возвращает сообщение для одиночного ордера по правилам
            fix api"""
        order_type = order_type.lower()
        action = action.lower()
        if action == 'buy':
            side = '1'
        elif action == 'sell':
            side = '2'
        else:
            side = 'ERROR'

        if order_type == 'market':
            order_type = 1
        elif order_type == 'limit':
            order_type = 2
        elif order_type == 'stop':
            order_type = 3
        else:
            order_type = 'ERROR'
        message = {
            11: order_id,
            55: symbol_id,
            54: side,
            60: self.get_format_time(),
            40: order_type,
            38: qty}

        if order_type == 2:
            message[44] = price

        if order_type == 3:
            message[99] = st_price

        request = self.create_request(
            message=message,
            message_type='D')

        self.logger.info(
            "Order: {} | Action: {} | Order type: {} |Symbol: {} |"
            " Quontity: {} | Price: {} | Stop Price: {}".format(
                order_id, action, order_type, symbol_id, qty, price, st_price))

        return (request)

    def execute_logon(self, username, password):
        '''Создаёт и отправляет запрос на logon. Возвращает ответ'''
        request = self.create_logon_req(username, password)
        response = self.send_to_serv(message=request, message_type='Logon')
        self.msgSeqNum = 2
        return response

    def execute_logout(self):
        '''Создаёт и отправляет запрос на logout. Возвращает ответ'''
        request = self.create_logout_req()
        response = self.send_to_serv(message=request, message_type='Logout')
        return response

    def execute_create_order_req(
            self,
            order_id,  # id заявки
            symbol_id,  # id символа
            action,  # buy или sell
            qty,  # количество
            order_type='market',  # market, limit или stop
            price='Market',  # указывать только при order_type = limit
            st_price='None'  # указывать только при order_type = stop
    ):
        '''Создаёт и отправляет ордер, сформированный по правилам fix api на
            сервер. Возвращает ответ'''
        request = self.create_order_req(
            order_id,  # id заявки
            symbol_id,  # id символа
            action,  # buy или sell
            qty,  # количество
            order_type,  # market, limit или stop
            price,  # указывать только при order_type = limit
            st_price)
        response = self.send_to_serv(
            message=request,
            message_type='Create Order')
        return response
