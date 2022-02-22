from datetime import datetime
from unittest import TestCase, main

from ctrader_fixapi_seller import FixApi

fapi = FixApi(
    senderCompID='demo.ctrader.3454732',
    targetCompID='CSERVER',
    host='h28.p.ctrader.com',
    port=5202,
    fixversion='FIX.4.4',
    time_in_ms=False)


class FixApiTest_execute_positive(TestCase):

    def test_connect_to_serv(self):
        self.assertIsNone(fapi.connect_to_serv())
        fapi.disconnect_from_serv()

    def test_execute_logon(self):
        fapi.connect_to_serv()

        resp = fapi.execute_logon(3454732, 3454732)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        fapi.execute_logout()
        fapi.disconnect_from_serv()

    def test_send_to_serv(self):
        fapi.connect_to_serv()
        fapi.execute_logon(3454732, 3454732)

        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        message = '8=FIX.4.4|9=140|35=D|49=demo.ctrader.3454732|' \
                  f'56=CSERVER|34=2|52={time}|11=876316397|55=1|' \
                  f'54=1|60={time}|40=3|38=1000|99=12313|'
        message += fapi.create_tail(message)

        resp = fapi.send_to_serv(message=message, message_type='3454732')
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        fapi.execute_logout()
        fapi.disconnect_from_serv()

    def test_disconnect_from_serv(self):
        fapi.connect_to_serv()
        fapi.disconnect_from_serv()

        with self.assertRaises(Exception):
            fapi.sock.send('ok'.encode())

    def test_execute_create_order_market(self):
        fapi = FixApi(
            senderCompID='demo.ctrader.3454732',
            targetCompID='CSERVER',
            host='h28.p.ctrader.com',
            port=5202)
        fapi.start_logging()
        fapi.connect_to_serv()
        fapi.execute_logon(3454732, 3454732)

        resp = fapi.execute_create_order_req(order_id=876316397, symbol_id=1,
                                             action='sell', qty=1000,
                                             order_type='market')
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        fapi.execute_logout()
        fapi.disconnect_from_serv()

    def test_execute_create_order_limit(self):
        fapi = FixApi(
            senderCompID='demo.ctrader.3454732',
            targetCompID='CSERVER',
            host='h28.p.ctrader.com',
            port=5202)
        fapi.start_logging()
        fapi.connect_to_serv()
        fapi.execute_logon(3454732, 3454732)

        resp = fapi.execute_create_order_req(order_id=876316397, symbol_id=1,
                                             action='buy', qty=1000,
                                             order_type='limit', price=13123)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        fapi.execute_logout()
        fapi.disconnect_from_serv()

    def test_execute_create_order_stop(self):
        fapi = FixApi(
            senderCompID='demo.ctrader.3454732',
            targetCompID='CSERVER',
            host='h28.p.ctrader.com',
            port=5202)
        fapi.start_logging()
        fapi.connect_to_serv()
        fapi.execute_logon(3454732, 3454732)

        resp = fapi.execute_create_order_req(order_id=876316397, symbol_id=1,
                                             action='sell', qty=1000,
                                             order_type='stop', st_price=13123)
        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        fapi.execute_logout()
        fapi.disconnect_from_serv()

class FixApiTest_execute_neagtive(TestCase):

        def test_send_to_serv(self):
            fapi.connect_to_serv()
            fapi.execute_logon(3454732, 3454732)

            time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
            message = '8=FIX.4.4|9=140|35=D|49=demo.ctrader.3454732|' \
                      f'56=CSERVER|34=2|52={time}|11=876316397|55=d|' \
                      f'54=1|60={time}|40=d|38=1000|99=12313|'
            message += fapi.create_tail(message)

            resp = fapi.send_to_serv(message=message, message_type='3454732')
            self.assertTrue(type(resp) is dict)
            value_of_error = resp.get('58')
            self.assertIsNotNone(value_of_error)

            fapi.execute_logout()
            fapi.disconnect_from_serv()

        def test_execute_create_order_market(self):
            fapi = FixApi(
                senderCompID='demo.ctrader.3454732',
                targetCompID='CSERVER',
                host='h28.p.ctrader.com',
                port=5202)
            fapi.start_logging()
            fapi.connect_to_serv()
            fapi.execute_logon(3454732, 3454732)

            resp = fapi.execute_create_order_req(order_id=876316397,
                                                 symbol_id=1,
                                                 action='sell', qty='d',
                                                 order_type='market')
            self.assertTrue(type(resp) is dict)
            value_of_error = resp.get('58')
            self.assertIsNotNone(value_of_error)

            fapi.execute_logout()
            fapi.disconnect_from_serv()

        def test_execute_create_order_limit(self):
            fapi = FixApi(
                senderCompID='demo.ctrader.3454732',
                targetCompID='CSERVER',
                host='h28.p.ctrader.com',
                port=5202)
            fapi.start_logging()
            fapi.connect_to_serv()
            fapi.execute_logon(3454732, 3454732)

            resp = fapi.execute_create_order_req(order_id=876316397,
                                                 symbol_id=1,
                                                 action='buy', qty='b',
                                                 order_type='limit',
                                                 price=13123)
            self.assertTrue(type(resp) is dict)
            value_of_error = resp.get('58')
            self.assertIsNotNone(value_of_error)

            fapi.execute_logout()
            fapi.disconnect_from_serv()

        def test_execute_create_order_stop(self):
            fapi = FixApi(
                senderCompID='demo.ctrader.3454732',
                targetCompID='CSERVER',
                host='h28.p.ctrader.com',
                port=5202)
            fapi.start_logging()
            fapi.connect_to_serv()
            fapi.execute_logon(3454732, 3454732)

            resp = fapi.execute_create_order_req(order_id=876316397,
                                                 symbol_id=1,
                                                 action='sell', qty='d',
                                                 order_type='stop',
                                                 st_price=13123)
            self.assertTrue(type(resp) is dict)
            value_of_error = resp.get('58')
            self.assertIsNotNone(value_of_error)

            fapi.execute_logout()
            fapi.disconnect_from_serv()


if __name__ == "__main__":
    main()
