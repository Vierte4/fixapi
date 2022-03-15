from datetime import datetime
from unittest import TestCase, main

from ctrader_fixapi_seller import FixApi
from users import demo1


class FixApiTest_execute_ConnectionAndLogon(TestCase):
    def setUp(self):
        self.fapi = FixApi(
            senderCompID=demo1.senderCompID,
            targetCompID=demo1.targetCompID,
            host=demo1.host,
            port=demo1.port,
            fixversion='FIX.4.4',
            time_in_ms=False)

    def test_connect_to_serv(self):
        self.assertIsNone(self.fapi.connect_to_serv())
        self.fapi.disconnect_from_serv()

    def test_execute_logon(self):
        self.fapi.connect_to_serv()

        resp = self.fapi.execute_logon(demo1.username, demo1.password)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        self.fapi.execute_logout()
        self.fapi.disconnect_from_serv()

    def test_execute_logout(self):
        self.fapi.connect_to_serv()

        self.fapi.execute_logon(demo1.username, demo1.password)
        resp = self.fapi.execute_logout()
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        self.fapi.disconnect_from_serv()

    def test_disconnect_from_serv(self):
        self.fapi.connect_to_serv()
        self.fapi.disconnect_from_serv()

        with self.assertRaises(Exception):
            self.fapi.sock.send('ok'.encode())


class FixApiTest_execute_orders_positive(TestCase):
    def setUp(self):
        self.fapi = FixApi(
            senderCompID=demo1.senderCompID,
            targetCompID=demo1.targetCompID,
            host=demo1.host,
            port=demo1.port,
            fixversion='FIX.4.4',
            time_in_ms=False)
        self.fapi.start_logging()
        self.fapi.connect_to_serv()
        self.fapi.execute_logon(demo1.username, demo1.password)

    def tearDown(self):
        self.fapi.execute_logout()
        self.fapi.disconnect_from_serv()

    def test_send_to_serv(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        message = f'8=FIX.4.4|9=140|35=D|49=demo.ctrader.{demo1.username}|' \
                  f'56=CSERVER|34=2|52={time}|11=876316397|55=1|' \
                  f'54=1|60={time}|40=3|38=1000|99=12313|'
        message += self.fapi.create_tail(message)

        resp = self.fapi.send_to_serv(message=message, message_type='Order')
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

    def test_execute_create_marketOrder(self):
        resp = self.fapi.execute_create_order_req(order_id=876316397,
                                                  symbol_id=1,
                                                  action='sell', qty=1000,
                                                  order_type='market')
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

    def test_execute_create_limitOrder(self):
        resp = self.fapi.execute_create_order_req(order_id=876316397,
                                                  symbol_id=1,
                                                  action='buy', qty=1000,
                                                  order_type='limit',
                                                  price=13123)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

    def test_execute_create_stopOrder(self):
        resp = self.fapi.execute_create_order_req(order_id=876316397,
                                                  symbol_id=1,
                                                  action='sell', qty=1000,
                                                  order_type='stop',
                                                  st_price=13123)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)


class FixApiTest_execute_neagtive(TestCase):

    def setUp(self):
        self.fapi = FixApi(
            senderCompID=demo1.senderCompID,
            targetCompID=demo1.targetCompID,
            host=demo1.host,
            port=demo1.port,
            fixversion='FIX.4.4',
            time_in_ms=False)
        self.fapi.start_logging()
        self.fapi.connect_to_serv()
        self.fapi.execute_logon(demo1.username, demo1.password)

    def tearDown(self):
        self.fapi.execute_logout()
        self.fapi.disconnect_from_serv()

    def test_send_to_serv(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        message = f'8=FIX.4.4|9=140|35=D|49=demo.ctrader.{demo1.username}|' \
                  f'56=CSERVER|34=2|52={time}|11=876316397|55=d|' \
                  f'54=1|60={time}|40=d|38=1000|99=12313|'
        message += self.fapi.create_tail(message)

        resp = self.fapi.send_to_serv(message=message, message_type='Order')
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

    def test_execute_create_marketOrder(self):
        resp = self.fapi.execute_create_order_req(order_id=876316397,
                                                  symbol_id=1,
                                                  action='sell', qty='d',
                                                  order_type='market')
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

    def test_execute_create_limitOrder(self):
        resp = self.fapi.execute_create_order_req(order_id=876316397,
                                                  symbol_id=1,
                                                  action='buy', qty='b',
                                                  order_type='limit',
                                                  price=13123)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

    def test_execute_create_stopOrder(self):
        resp = self.fapi.execute_create_order_req(order_id=876316397,
                                                  symbol_id=1,
                                                  action='sell', qty='d',
                                                  order_type='stop',
                                                  st_price=13123)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)


if __name__ == "__main__":
    main()
