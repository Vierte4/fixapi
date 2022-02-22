from unittest import TestCase, main

from simple_fixapi import SimpleFixApi
from users import demo1


class SimpleFixApiTest_positive(TestCase):

    def test_start_session(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()

        resp = sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='buy',
            qty=1000,
            order_type='stop',
            st_price=12313)

        self.assertTrue(resp)
        sapi.end_session()

    def test_end_session(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()
        sapi.end_session()

        with self.assertRaises(Exception):
            sapi.fixApi.sock.send('ok'.encode())

    def test_send_market_order(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()

        resp = sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='buy',
            qty=1000,
            order_type='market')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        sapi.end_session()

    def test_send_limit_order(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()

        resp = sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='sell',
            qty=1000,
            order_type='limit',
            price='1000000')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        sapi.end_session()

    def test_send_stop_order(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()

        resp = sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='buy',
            qty=1000,
            order_type='stop',
            st_price=10000)

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

        sapi.end_session()


class SimpleFixApiTest_negative(TestCase):

    def test_send_market_order_negative(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()

        resp = sapi.send_order(
            order_id=122,
            symbol_id='xxxx',
            action='sell',
            qty=1000,
            order_type='market')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

        sapi.end_session()

    def test_send_limit_order_negative(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()

        resp = sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='xxx',
            qty=1000,
            order_type='limit',
            price='1000000')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

        sapi.end_session()

    def test_send_stop_order_negative(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()

        resp = sapi.send_order(
            order_id=1,
            symbol_id='1',
            action='buy',
            qty=1000,
            order_type='aaaa',
            st_price=10000)

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

        sapi.end_session()


if __name__ == '__main__':
    main()
