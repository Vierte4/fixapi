from ctrader_fixapi_seller import FixApi
from users import User, demo1


class SimpleFixApi():
    def __init__(self, user: User):
        self.user = user

        self.fixApi = FixApi(
            senderCompID=user.senderCompID,
            targetCompID=user.targetCompID,
            host=user.host,
            port=user.port)

    def start_session(self):
        '''Запускает логгинг, создаёт соединение с сервером и логинится'''
        self.fixApi.start_logging()
        self.fixApi.connect_to_serv()
        self.fixApi.execute_logon(self.user.username, self.user.password)

    def end_session(self):
        '''Разлогинивается и отключает соединение с сервером'''
        self.fixApi.execute_logout()
        self.fixApi.disconnect_from_serv()

    def send_order(
            self,
            order_id,  # id заявки
            symbol_id,  # id символа
            action,  # buy или sell
            qty,  # количество
            order_type='market',  # market, limit или stop
            price='Market',  # указывать только при order_type = limit
            st_price='None'  # указывать только при order_type = stop
    ):
        '''Формирует и отправляет ордер на сервер. Возвращает ответ. Если ответ
            не был получен, пытается заново подключиться к серву и залогиниться'''
        response = self.fixApi.execute_create_order_req(
            order_id,  # id заявки
            symbol_id,  # id символа
            action,  # buy или sell
            qty,  # количество
            order_type,  # market, limit или stop
            price,  # указывать только при order_type = limit
            st_price  # указывать только при order_type = stop
        )

        if type(response) is dict:
            return response
        else:
            self.fixApi.connect_to_serv()
            self.fixApi.execute_logon(self.user.username, self.user.password)
            return self.fixApi.execute_create_order_req(
                order_id,  # id заявки
                symbol_id,  # id символа
                action,  # buy или sell
                qty,  # количество
                order_type,  # market, limit или stop
                price,  # указывать только при order_type = limit
                st_price  # указывать только при order_type = stop
            )


if __name__ == "__main__":
    sapi = SimpleFixApi(demo1)
    sapi.start_session()

    print(sapi.send_order(
        order_id=122,
        symbol_id=1,
        action='buy',
        qty=1000,
        order_type='stop',
        st_price=12313))

    print(sapi.send_order(
        order_id=123,
        symbol_id=1,
        action='buy',
        qty=1000,
        order_type='stop',
        st_price=12313))

    print(sapi.send_order(
        order_id=124,
        symbol_id=1,
        action='buy',
        qty=1000,
        order_type='stop',
        st_price=12313))

    print(sapi.send_order(
        order_id=125,
        symbol_id=1,
        action='buy',
        qty=1000,
        order_type='stop',
        st_price=12313))

    print(sapi.send_order(
        order_id=126,
        symbol_id=1,
        action='buy',
        qty=1000,
        order_type='stop',
        st_price=12313))

    print(sapi.send_order(
        order_id=127,
        symbol_id=1,
        action='buy',
        qty=1000,
        order_type='stop',
        st_price=12313))

    sapi.end_session()
