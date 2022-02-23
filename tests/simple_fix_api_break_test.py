from unittest import TestCase, main

from simple_fixapi import SimpleFixApi
from users import demo1


class SimpleFixApiTest_break(TestCase):
    def send_order_shablon(self, sapi):
        return sapi.send_order(
            order_id=122,
            symbol_id=1,
            action='buy',
            qty=1000,
            order_type='stop',
            st_price=12313)

    def test_break_connect(self):

        sapi = SimpleFixApi(demo1)
        sapi.start_session()
        answers = []

        for a in range(2):
            answers.append(self.send_order_shablon(sapi))

        print('break sock')
        sapi.fixApi.disconnect_from_serv()

        for a in range(2):
            answers.append(self.send_order_shablon(sapi))

        sapi.end_session()

        [print(answ) for answ in answers]

        for answ in answers:
            self.assertTrue(type(answ) is dict)
            value_of_error = answ.get('58')
            self.assertIsNone(value_of_error)

        self.assertTrue(len(answers) == 4)

    def test_break_sock_connect(self):

        sapi = SimpleFixApi(demo1)
        sapi.start_session()
        answers = []

        for a in range(2):
            answers.append(self.send_order_shablon(sapi))

        print('break connection')
        sapi.fixApi.sock.close()
        sapi.fixApi.host = 1234

        for a in range(2):
            answers.append(self.send_order_shablon(sapi))

        print('connection restored')
        sapi.fixApi.host = demo1.host

        for a in range(2):
            answers.append(self.send_order_shablon(sapi))

        [print(answ) for answ in answers]

        sapi.end_session()

        for answ in answers[4:5]:
            self.assertTrue(type(answ) is dict)
            value_of_error = answ.get('58')
            self.assertIsNone(value_of_error)

        self.assertTrue(len(answers) == 6)


if __name__ == '__main__':
    main()
