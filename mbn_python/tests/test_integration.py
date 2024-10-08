import unittest
from mbn import (
    Side,
    Action,
    Schema,
    RType,
    SymbolMap,
    Metadata,
    BufferStore,
    BidAskPair,
    RecordMsg,
    OhlcvMsg,
    Mbp1Msg,
    TradeMsg,
    # TbboMsg,
    BboMsg,
)
from pandas import pandas


def handle_msg(msg: RecordMsg) -> int:
    return msg.ts_event


class IntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_side(self):
        # Direct instantiation
        bid = Side.BID
        self.assertEqual(bid, Side.BID)

        # from str
        ask = Side.from_str("A")
        self.assertEqual(ask, Side.ASK)

        # from int
        ask = Side.from_int(65)
        self.assertEqual(ask, Side.ASK)

        # Error
        with self.assertRaises(ValueError):
            Side.from_str("T")

        # with self.assertRaises(TypeError):
        #     Side.from_str(9)

    def test_action(self):
        # Direct instantiation
        modify = Action.MODIFY
        self.assertEqual(modify, Action.MODIFY)

        # from str
        add = Action.from_str("A")
        self.assertEqual(add, Action.ADD)

        # from int
        add = Action.from_int(65)
        self.assertEqual(add, Action.ADD)

        # Error
        with self.assertRaises(ValueError):
            Action.from_str("dj")

    def test_schema(self):
        # instantiation
        mbp_1 = Schema.MBP1
        self.assertEqual(mbp_1, Schema.MBP1)

        # from str
        ohlcv = Schema.from_str("ohlcv-1s")
        self.assertEqual(ohlcv, Schema.OHLCV1_S)

        # __str__
        schema = Schema.OHLCV1_S.__str__()
        self.assertEqual(schema, "ohlcv-1s")

        # Error
        with self.assertRaises(ValueError):
            Schema.from_str("ohlcv-12345s")

    def test_rtype(self):
        # from int
        rtype = RType.from_int(0x01)
        self.assertEqual(rtype, RType.MBP1)

        # from str
        rtype = RType.from_str("ohlcv")
        self.assertEqual(rtype, RType.OHLCV)

        # from schema
        rtype = RType.from_schema(Schema.from_str("ohlcv-1s"))
        self.assertEqual(rtype, RType.OHLCV)

        # Errors
        with self.assertRaises(ValueError):
            RType.from_int(0x09)

        with self.assertRaises(ValueError):
            RType.from_str("olghd")

    def test_metadata(self):
        symbol_map = SymbolMap({1: "AAPL", 2: "TSLA"})

        # Test
        metadata = Metadata(
            Schema.from_str("ohlcv-1s"),
            1234567654321,
            987654345676543456,
            symbol_map,
        )
        encoded = metadata.encode()
        decoded_metadata = metadata.decode(encoded)

        # Validate
        self.assertEqual(decoded_metadata.start, metadata.start)
        self.assertEqual(decoded_metadata.schema, metadata.schema)
        self.assertEqual(decoded_metadata.mappings, metadata.mappings)
        self.assertEqual(decoded_metadata.end, metadata.end)

    def test_symbol_map(self):
        # Test
        symbol_map = SymbolMap({1: "AAPL", 2: "TSLA"})

        # Validate
        ticker_1 = symbol_map.get_ticker(1)
        self.assertEqual(ticker_1, "AAPL")

        ticker_2 = symbol_map.get_ticker(2)
        self.assertEqual(ticker_2, "TSLA")

        mappings = symbol_map.map
        self.assertEqual(mappings, mappings)

    def test_bid_ask_properties(self):
        pair = BidAskPair(1, 2, 3, 4, 5, 6)

        # Validate
        self.assertEqual(pair.bid_px, 1)
        self.assertEqual(pair.ask_px, 2)
        self.assertEqual(pair.bid_sz, 3)
        self.assertEqual(pair.ask_sz, 4)
        self.assertEqual(pair.bid_ct, 5)
        self.assertEqual(pair.ask_ct, 6)
        self.assertEqual(pair.pretty_bid_px, 1 / 1e9)
        self.assertEqual(pair.pretty_ask_px, 2 / 1e9)

    def test_ohlcvmsg_properties(self):
        msg = OhlcvMsg(1, 123456765432, 1, 2, 3, 4, 100000)

        # Test
        self.assertEqual(msg.rtype, RType.OHLCV)
        self.assertEqual(msg.instrument_id, 1)
        self.assertEqual(msg.ts_event, 123456765432)
        self.assertEqual(msg.open, 1)
        self.assertEqual(msg.pretty_open, 1 / 1e9)
        self.assertEqual(msg.high, 2)
        self.assertEqual(msg.pretty_high, 2 / 1e9)
        self.assertEqual(msg.low, 3)
        self.assertEqual(msg.pretty_low, 3 / 1e9)
        self.assertEqual(msg.close, 4)
        self.assertEqual(msg.pretty_close, 4 / 1e9)
        self.assertEqual(msg.volume, 100000)
        self.assertEqual(msg.pretty_price, 4 / 1e9)
        # self.assert(msg, RecordMsg)

    def test_mbpmsg_properties(self):
        pair = BidAskPair(1, 2, 3, 4, 5, 6)
        msg = Mbp1Msg(
            1,
            123456765432,
            1,
            2,
            Action.ADD,
            Side.ASK,
            0,
            0,
            3,
            4,
            5,
            [pair],
        )

        # Test
        self.assertEqual(msg.rtype, RType.MBP1)
        self.assertEqual(msg.instrument_id, 1)
        self.assertEqual(msg.ts_event, 123456765432)
        self.assertEqual(msg.price, 1)
        self.assertEqual(msg.pretty_price, 1 / 1e9)
        self.assertEqual(msg.action, 65)
        self.assertEqual(msg.pretty_action, Action.ADD)
        self.assertEqual(msg.pretty_side, Side.ASK)
        self.assertEqual(msg.side, 65)
        self.assertEqual(msg.depth, 0)
        self.assertEqual(msg.ts_recv, 3)
        self.assertEqual(msg.ts_in_delta, 4)
        self.assertEqual(msg.sequence, 5)
        self.assertEqual(msg.levels[0].bid_px, pair.bid_px)
        self.assertEqual(msg.levels[0].ask_px, pair.ask_px)
        self.assertEqual(msg.levels[0].bid_sz, pair.bid_sz)
        self.assertEqual(msg.levels[0].ask_sz, pair.ask_sz)
        self.assertEqual(msg.levels[0].bid_ct, pair.bid_ct)
        self.assertEqual(msg.levels[0].ask_ct, pair.ask_ct)

    def test_trademsg_properties(self):
        msg = TradeMsg(
            1,
            123456765432,
            1,
            2,
            Action.TRADE,
            Side.ASK,
            0,
            0,
            3,
            4,
            5,
        )

        # Test
        self.assertEqual(msg.rtype, RType.TRADE)
        self.assertEqual(msg.instrument_id, 1)
        self.assertEqual(msg.ts_event, 123456765432)
        self.assertEqual(msg.price, 1)
        self.assertEqual(msg.pretty_price, 1 / 1e9)
        self.assertEqual(msg.action, 84)
        self.assertEqual(msg.pretty_action, Action.TRADE)
        self.assertEqual(msg.pretty_side, Side.ASK)
        self.assertEqual(msg.side, 65)
        self.assertEqual(msg.depth, 0)
        self.assertEqual(msg.ts_recv, 3)
        self.assertEqual(msg.ts_in_delta, 4)
        self.assertEqual(msg.sequence, 5)

    def test_bbomsg_properties(self):
        pair = BidAskPair(1, 2, 3, 4, 5, 6)
        msg = BboMsg(
            1,
            123456765432,
            1,
            2,
            Side.ASK,
            0,
            3,
            5,
            [pair],
        )

        # Test
        self.assertEqual(msg.rtype, RType.BBO)
        self.assertEqual(msg.instrument_id, 1)
        self.assertEqual(msg.ts_event, 123456765432)
        self.assertEqual(msg.price, 1)
        self.assertEqual(msg.pretty_price, 1 / 1e9)
        self.assertEqual(msg.pretty_side, Side.ASK)
        self.assertEqual(msg.side, 65)
        self.assertEqual(msg.ts_recv, 3)
        self.assertEqual(msg.sequence, 5)
        self.assertEqual(msg.levels[0].bid_px, pair.bid_px)
        self.assertEqual(msg.levels[0].ask_px, pair.ask_px)
        self.assertEqual(msg.levels[0].bid_sz, pair.bid_sz)
        self.assertEqual(msg.levels[0].ask_sz, pair.ask_sz)
        self.assertEqual(msg.levels[0].bid_ct, pair.bid_ct)
        self.assertEqual(msg.levels[0].ask_ct, pair.ask_ct)

    def test_msg_polymorphism(self):
        msg = OhlcvMsg(1, 123456765432, 1, 2, 3, 4, 100000)

        # Test
        ts_event = handle_msg(msg)
        self.assertEqual(ts_event, msg.ts_event)

    def test_buffer_store_file(self):
        # Binary
        bin = [
            2,
            141,
            38,
            251,
            113,
            31,
            1,
            0,
            0,
            248,
            189,
            152,
            190,
            28,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            65,
            65,
            80,
            76,
            2,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            84,
            83,
            76,
            65,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            14,
            2,
            0,
            0,
            1,
            0,
            0,
            0,
            212,
            241,
            180,
            96,
            0,
            0,
            0,
            0,
            100,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            200,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            50,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            150,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            232,
            3,
            0,
            0,
            0,
            0,
            0,
            0,
            14,
            2,
            0,
            0,
            2,
            0,
            0,
            0,
            213,
            241,
            180,
            96,
            0,
            0,
            0,
            0,
            110,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            210,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            55,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            155,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            76,
            4,
            0,
            0,
            0,
            0,
            0,
            0,
        ]

        # Write bin file
        buffer_obj = BufferStore(bytes(bin))
        buffer_obj.write_to_file("test.bin")

        # Test
        new_buffer = BufferStore.from_file("test.bin")
        metadata = new_buffer.metadata
        ohlcv_msgs = new_buffer.decode_to_array()

        # Validate
        self.assertEqual(metadata.schema, Schema.OHLCV1_S)
        self.assertEqual(metadata.start, 1234567898765)
        self.assertEqual(metadata.end, 123456765432)
        self.assertIsInstance(metadata.mappings, SymbolMap)
        self.assertIsInstance(ohlcv_msgs[0], OhlcvMsg)

    def test_buffer_store_with_metadata(self):
        bin = [
            1,
            141,
            38,
            251,
            113,
            31,
            1,
            0,
            0,
            248,
            189,
            152,
            190,
            28,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            65,
            65,
            80,
            76,
            2,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            84,
            83,
            76,
            65,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            20,
            1,
            0,
            0,
            1,
            0,
            0,
            0,
            212,
            241,
            180,
            96,
            0,
            0,
            0,
            0,
            232,
            3,
            0,
            0,
            0,
            0,
            0,
            0,
            10,
            0,
            0,
            0,
            1,
            1,
            0,
            0,
            13,
            49,
            15,
            134,
            72,
            112,
            0,
            0,
            57,
            48,
            0,
            0,
            64,
            226,
            1,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            3,
            0,
            0,
            0,
            20,
            1,
            0,
            0,
            1,
            0,
            0,
            0,
            212,
            241,
            180,
            96,
            0,
            0,
            0,
            0,
            232,
            3,
            0,
            0,
            0,
            0,
            0,
            0,
            10,
            0,
            0,
            0,
            1,
            1,
            0,
            0,
            13,
            49,
            15,
            134,
            72,
            112,
            0,
            0,
            57,
            48,
            0,
            0,
            64,
            226,
            1,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            3,
            0,
            0,
            0,
        ]

        # Test
        buffer_obj = BufferStore(bytes(bin))
        mbp_msgs = buffer_obj.decode_to_array()

        # Validate
        # Metadata
        self.assertEqual(buffer_obj.metadata.schema, Schema.MBP1)
        self.assertEqual(buffer_obj.metadata.start, 1234567898765)
        self.assertEqual(buffer_obj.metadata.end, 123456765432)
        self.assertIsInstance(buffer_obj.metadata.mappings, SymbolMap)

        # MSG
        self.assertEqual(mbp_msgs[0].hd.instrument_id, 1)
        self.assertEqual(mbp_msgs[0].hd.ts_event, 1622471124)
        self.assertIsInstance(mbp_msgs[0], Mbp1Msg)

    def test_decode_do_df(self):
        # Binary
        bin = [
            2,
            141,
            38,
            251,
            113,
            31,
            1,
            0,
            0,
            248,
            189,
            152,
            190,
            28,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            84,
            83,
            76,
            65,
            1,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            65,
            65,
            80,
            76,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            14,
            2,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            188,
            179,
            122,
            176,
            230,
            237,
            23,
            0,
            232,
            118,
            72,
            23,
            0,
            0,
            0,
            0,
            208,
            237,
            144,
            46,
            0,
            0,
            0,
            0,
            116,
            59,
            164,
            11,
            0,
            0,
            0,
            0,
            92,
            178,
            236,
            34,
            0,
            0,
            0,
            0,
            16,
            165,
            212,
            232,
            0,
            0,
            0,
            14,
            2,
            0,
            0,
            2,
            0,
            0,
            0,
            0,
            220,
            253,
            35,
            130,
            232,
            237,
            23,
            0,
            204,
            130,
            156,
            25,
            0,
            0,
            0,
            0,
            180,
            249,
            228,
            48,
            0,
            0,
            0,
            0,
            102,
            65,
            206,
            12,
            0,
            0,
            0,
            0,
            78,
            184,
            22,
            36,
            0,
            0,
            0,
            0,
            248,
            27,
            29,
            0,
            1,
            0,
            0,
        ]

        # Test
        buffer_obj = BufferStore(bytes(bin))
        df = buffer_obj.decode_to_df(pretty_ts=True, pretty_px=False)
        # Valdiate
        self.assertIsInstance(df, pandas.DataFrame)

    def test_decode_replay(self):
        # Binary
        bin = [
            2,
            141,
            38,
            251,
            113,
            31,
            1,
            0,
            0,
            248,
            189,
            152,
            190,
            28,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            65,
            65,
            80,
            76,
            2,
            0,
            0,
            0,
            4,
            0,
            0,
            0,
            84,
            83,
            76,
            65,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            14,
            2,
            0,
            0,
            1,
            0,
            0,
            0,
            212,
            241,
            180,
            96,
            0,
            0,
            0,
            0,
            100,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            200,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            50,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            150,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            232,
            3,
            0,
            0,
            0,
            0,
            0,
            0,
            14,
            2,
            0,
            0,
            2,
            0,
            0,
            0,
            213,
            241,
            180,
            96,
            0,
            0,
            0,
            0,
            110,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            210,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            55,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            155,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            76,
            4,
            0,
            0,
            0,
            0,
            0,
            0,
        ]

        # Test
        buffer_obj = BufferStore(bytes(bin))

        record = buffer_obj.replay()
        ts_event = 0
        while record is not None:
            self.assertTrue(record.ts_event > ts_event)
            record = buffer_obj.replay()


if __name__ == "__main__":
    unittest.main()
