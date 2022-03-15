import re
from datetime import datetime
from unittest import TestCase, main

from ctrader_fixapi_seller import FixApi


class FixApiTest_default(TestCase):

    def setUp(self):
        self.fapi = FixApi(
            senderCompID='demo.ctrader.3454732',
            targetCompID='CSERVER',
            host='h28.p.ctrader.com',
            port=5202,
            fixversion='FIX.4.4',
            time_in_ms=False)

    def test_create_fix_api_format(self):
        dict = {
            8: 'FIX.4.4',
            35: 'message_type',
            49: 'senderCompID',
            56: 'targetCompID',
            34: 'msgSeqNum',
            52: 'time'}
        target_message = '8=FIX.4.4|35=message_type|' \
                         '49=senderCompID|56=targetCompID|34=msgSeqNum|52=time'

        self.assertTrue(self.fapi.create_fix_api_format(dict), target_message)

    def test_time_s(self):
        r = re.compile('\d{8}-\d{2}:\d{2}:\d{2}')

        self.assertTrue(re.match(r, self.fapi.get_format_time()))

    def test_time_ms(self):
        self.fapi.time_in_ms = True
        r = re.compile('\d{8}-\d{2}:\d{2}:\d{2}.\d{3}')

        self.assertTrue(re.match(r, self.fapi.get_format_time()))

    def test_create_tail(self):
        message = '8=FIX.4.4|9=126|35=A|49=theBroker.12345|56=CSERVER|34=1|' \
                  '52=20170117-08:03:04|57=TRADE|50=any_string|98=0|108=30|' \
                  '141=Y|553=12345|554=passw0rd!|'
        tail = '10=131|'

        self.assertEqual(self.fapi.create_tail(message), tail)

    def test_create_header(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        header = {
            8: 'FIX.4.4',
            35: 'message_type',
            49: 'demo.ctrader.3454732',
            56: 'CSERVER',
            34: 1,
            52: time}

        self.assertEqual(self.fapi.create_header('message_type'), header)

    def test_create_request(self):
        message = {57: 'TRADE', 98: 0, 108: 30, 141: 'Y', 553: 'username',
                   554: 'password'}
        message_type = 'A'
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        target_message = '8=FIX.4.4|9=119|35=A|49=demo.ctrader.3454732|' \
                         f'56=CSERVER|34=1|52={time}|57=TRADE|98=0|108=30|' \
                         '141=Y|553=username|554=password|'
        target_message += self.fapi.create_tail(target_message)

        self.assertEqual(
            self.fapi.create_request(message, message_type),
            target_message)

    def test_parse_fix_message(self):
        target_dict = {
            '8': 'FIX.4.4',
            '35': 'message_type',
            '49': 'senderCompID',
            '56': 'targetCompID',
            '34': 'msgSeqNum',
            '52': 'time'}
        message = '8=FIX.4.4|35=message_type|' \
                  '49=senderCompID|56=targetCompID|' \
                  '34=msgSeqNum|52=time|'.replace("|", "\u0001")

        self.assertEqual(self.fapi.parse_fix_message(message), target_dict)

    def test_create_logon_req(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        target_req = '8=FIX.4.4|9=118|35=A|49=demo.ctrader.3454732|56=CSERVER|' \
                     f'34=1|52={time}|57=TRADE|98=0|108=0|' \
                     '141=Y|553=username|554=password|'
        target_req += self.fapi.create_tail(target_req)

        self.assertEqual(
            self.fapi.create_logon_req('username', 'password'),
            target_req)

    def test_create_logout_req(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        target_req = '8=FIX.4.4|9=75|35=5|49=demo.ctrader.3454732|56=CSERVER|' \
                     f'34=1|52={time}|57=TRADE|'
        target_req += self.fapi.create_tail(target_req)

        self.assertEqual(
            self.fapi.create_logout_req(),
            target_req)

    def test_create_marketOrder_req(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        market_order = '8=FIX.4.4|9=129|35=D|49=demo.ctrader.3454732|' \
                       f'56=CSERVER|34=1|52={time}|11=order_id|' \
                       f'55=symbol_id|54=1|60={time}|40=1|38=qty|'
        market_order += self.fapi.create_tail(market_order)

        self.assertEqual(
            self.fapi.create_order_req(
                'order_id',
                'symbol_id',
                'buy',
                'qty',
                order_type='market',
            ),
            market_order)

    def test_create_limitOrder_req(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        limit_order = '8=FIX.4.4|9=136|35=D|49=demo.ctrader.3454732|' \
                      f'56=CSERVER|34=1|52={time}|11=order_id|' \
                      f'55=symbol_id|54=1|60={time}|40=2|38=qty|44=100|'
        limit_order += self.fapi.create_tail(limit_order)

        self.assertEqual(
            self.fapi.create_order_req(
                'order_id',
                'symbol_id',
                'buy',
                'qty',
                price=100,
                order_type='limit'
            ),
            limit_order)

    def test_create_stopOrder_req(self):
        time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        stop_order = '8=FIX.4.4|9=136|35=D|49=demo.ctrader.3454732|' \
                     f'56=CSERVER|34=1|52={time}|11=order_id|' \
                     f'55=symbol_id|54=1|60={time}|40=3|38=qty|99=100|'
        stop_order += self.fapi.create_tail(stop_order)

        self.assertEqual(
            self.fapi.create_order_req(
                'order_id',
                'symbol_id',
                'buy',
                'qty',
                st_price=100,
                order_type='stop',
            ),
            stop_order)


if __name__ == '__main__':
    main()
