from unittest import TestCase, main

from simple_fixapi import SimpleFixApi
from users import demo1


class SimpleFixApiTest_StartEndSession_positive(TestCase):
    def test_start_session(self):
        sapi = SimpleFixApi(demo1)
        resp = sapi.start_session()
        self.assertEqual(resp, 'Вход выполнен успешно')
        sapi.end_session()

    def test_end_session(self):
        sapi = SimpleFixApi(demo1)
        sapi.start_session()
        sapi.end_session()

        with self.assertRaises(Exception):
            sapi.fixApi.sock.send('ok'.encode())


class SimpleFixApiTest_StartEndSession_negative(TestCase):
    def test_start_session_negative_user(self):
        sapi = SimpleFixApi(demo1)
        sapi.user.password = 11111
        resp = sapi.start_session()

        sapi.end_session()

        self.assertEqual(resp, 'Неправильные логин и/или пароль')

    def test_start_session_negative_host(self):
        sapi = SimpleFixApi(demo1)
        sapi.fixApi.host = 111
        resp = sapi.start_session()
        sapi.end_session()
        self.assertEqual(resp, 'Сервер не отвечает')


class SimpleFixApiTest_SendOrder_positive(TestCase):
    def setUp(self):
        self.sapi = SimpleFixApi(demo1)
        self.sapi.start_session()

    def tearDown(self):
        self.sapi.end_session()

    def test_send_MarketOrder(self):
        resp = self.sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='buy',
            qty=1000,
            order_type='market')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

    def test_send_LimitOrder(self):
        resp = self.sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='sell',
            qty=1000,
            order_type='limit',
            price='1000000')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)

    def test_send_StopOrder(self):
        resp = self.sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='buy',
            qty=1000,
            order_type='stop',
            st_price=10000)

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNone(value_of_error)


class SimpleFixApiTest_negative(TestCase):
    def setUp(self):
        self.sapi = SimpleFixApi(demo1)
        self.sapi.start_session()

    def tearDown(self):
        self.sapi.end_session()

    def test_send_market_order_negative(self):
        resp = self.sapi.send_order(
            order_id=122,
            symbol_id='xxxx',
            action='sell',
            qty=1000,
            order_type='market')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

    def test_send_limit_order_negative(self):
        resp = self.sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='xxx',
            qty=1000,
            order_type='limit',
            price='1000000')

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)

    def test_send_stop_order_negative(self):
        resp = self.sapi.send_order(
            order_id=1,
            symbol_id='1',
            action='buy',
            qty=1000,
            order_type='aaaa',
            st_price=10000)

        self.assertTrue(type(resp) is dict)
        value_of_error = resp.get('58')
        self.assertIsNotNone(value_of_error)


if __name__ == '__main__':
    main()
