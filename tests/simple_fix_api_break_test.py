from unittest import TestCase, main

from simple_fixapi import SimpleFixApi
from users import demo1


class SimpleFixApiTest_break(TestCase):

    def setUp(self):
        self.sapi = SimpleFixApi(demo1)
        print(self.sapi.user)
        self.sapi.start_session()
        self.answers = []

    def send_order_template(self, sapi):
        return sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='buy',
            qty=1000,
            order_type='stop',
            st_price=12313)

    def test_break_connect(self):

        for a in range(2):
            self.answers.append(self.send_order_template(self.sapi))

        print('break sock')
        self.sapi.fixApi.disconnect_from_serv()

        for a in range(2):
            self.answers.append(self.send_order_template(self.sapi))

        self.sapi.end_session()

        [print(answ) for answ in self.answers]

        for answ in self.answers:
            self.assertTrue(type(answ) is dict)
            value_of_error = answ.get('58')
            self.assertIsNone(value_of_error)

        self.assertTrue(len(self.answers) == 4)

    def test_break_sock_connect(self):

        for a in range(2):
            self.answers.append(self.send_order_template(self.sapi))

        print('break connection')
        self.sapi.fixApi.sock.close()
        self.sapi.fixApi.host = 1234

        for a in range(2):
            self.answers.append(self.send_order_template(self.sapi))

        print('connection restored')
        self.sapi.fixApi.host = demo1.host

        for a in range(2):
            self.answers.append(self.send_order_template(self.sapi))

        [print(answ) for answ in self.answers]

        self.sapi.end_session()

        for answ in self.answers[4:5]:
            self.assertTrue(type(answ) is dict)
            value_of_error = answ.get('58')
            self.assertIsNone(value_of_error)

        self.assertTrue(len(self.answers) == 6)


if __name__ == '__main__':
    main()
