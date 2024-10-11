use crate::enums::RType;
use crate::record_ref::RecordRef;
use crate::records::{BboMsg, Mbp1Msg, OhlcvMsg, Record, RecordHeader, TbboMsg, TradeMsg};
use serde::Serialize;

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum RecordEnum {
    Mbp1(Mbp1Msg),
    Ohlcv(OhlcvMsg),
    Trade(TradeMsg),
    Tbbo(TbboMsg),
    Bbo(BboMsg),
}

impl RecordEnum {
    pub fn from_ref(rec_ref: RecordRef) -> Option<Self> {
        match rec_ref.header().rtype() {
            RType::Mbp1 => rec_ref
                .get::<Mbp1Msg>()
                .map(|msg| RecordEnum::Mbp1(msg.clone())),
            RType::Ohlcv => rec_ref
                .get::<OhlcvMsg>()
                .map(|msg| RecordEnum::Ohlcv(msg.clone())),
            RType::Trade => rec_ref
                .get::<TradeMsg>()
                .map(|msg| RecordEnum::Trade(msg.clone())),
            RType::Tbbo => rec_ref
                .get::<TbboMsg>()
                .map(|msg| RecordEnum::Tbbo(msg.clone())),
            RType::Bbo => rec_ref
                .get::<BboMsg>()
                .map(|msg| RecordEnum::Bbo(msg.clone())),
        }
    }

    pub fn to_record_ref(&self) -> RecordRef {
        match self {
            RecordEnum::Mbp1(record) => record.into(),
            RecordEnum::Ohlcv(record) => record.into(),
            RecordEnum::Tbbo(record) => record.into(),
            RecordEnum::Bbo(record) => record.into(),
            RecordEnum::Trade(record) => record.into(),
        }
    }

    pub fn to_ref<'a>(&'a self) -> RecordEnumRef<'a> {
        match self {
            RecordEnum::Mbp1(msg) => RecordEnumRef::Mbp1(msg),
            RecordEnum::Ohlcv(msg) => RecordEnumRef::Ohlcv(msg),
            RecordEnum::Trade(msg) => RecordEnumRef::Trade(msg),
            RecordEnum::Tbbo(msg) => RecordEnumRef::Tbbo(msg),
            RecordEnum::Bbo(msg) => RecordEnumRef::Bbo(msg),
        }
    }
    pub fn msg(&self) -> &dyn Record {
        match self {
            RecordEnum::Mbp1(msg) => msg as &dyn Record,
            RecordEnum::Ohlcv(msg) => msg as &dyn Record,
            RecordEnum::Trade(msg) => msg as &dyn Record,
            RecordEnum::Tbbo(msg) => msg as &dyn Record,
            RecordEnum::Bbo(msg) => msg as &dyn Record,
        }
    }
}

impl PartialEq<dbn::RecordEnum> for RecordEnum {
    fn eq(&self, other: &dbn::RecordEnum) -> bool {
        match (self, other) {
            // Match and compare Mbp1 variants
            (RecordEnum::Mbp1(mbn_msg), dbn::RecordEnum::Mbp1(dbn_msg)) => mbn_msg.eq(dbn_msg),
            (RecordEnum::Tbbo(mbn_msg), dbn::RecordEnum::Mbp1(dbn_msg)) => mbn_msg.eq(dbn_msg),
            (RecordEnum::Bbo(mbn_msg), dbn::RecordEnum::Mbp1(dbn_msg)) => mbn_msg.eq(dbn_msg),
            (RecordEnum::Trade(mbn_msg), dbn::RecordEnum::Trade(dbn_msg)) => mbn_msg.eq(dbn_msg),
            (RecordEnum::Ohlcv(mbn_msg), dbn::RecordEnum::Ohlcv(dbn_msg)) => mbn_msg.eq(dbn_msg),
            _ => false,
        }
    }
}

impl AsRef<[u8]> for RecordEnum {
    fn as_ref(&self) -> &[u8] {
        match self {
            RecordEnum::Mbp1(msg) => msg.as_ref(),
            RecordEnum::Ohlcv(msg) => msg.as_ref(),
            RecordEnum::Trade(msg) => msg.as_ref(),
            RecordEnum::Tbbo(msg) => msg.as_ref(),
            RecordEnum::Bbo(msg) => msg.as_ref(),
        }
    }
}

impl Record for RecordEnum {
    fn header(&self) -> &RecordHeader {
        match self {
            RecordEnum::Mbp1(msg) => &msg.hd,
            RecordEnum::Ohlcv(msg) => &msg.hd,
            RecordEnum::Trade(msg) => &msg.hd,
            RecordEnum::Tbbo(msg) => &msg.hd,
            RecordEnum::Bbo(msg) => &msg.hd,
        }
    }
}

#[cfg(feature = "python")]
impl IntoPy<Py<PyAny>> for RecordEnum {
    fn into_py(self, py: Python<'_>) -> Py<PyAny> {
        match self {
            RecordEnum::Mbp1(msg) => msg.into_py(py).into(),
            RecordEnum::Ohlcv(msg) => msg.into_py(py).into(),
            RecordEnum::Trade(msg) => msg.into_py(py).into(),
            RecordEnum::Tbbo(msg) => msg.into_py(py).into(),
            RecordEnum::Bbo(msg) => msg.into_py(py).into(),
        }
    }
}

#[derive(Debug, Clone)]
pub enum RecordEnumRef<'a> {
    Mbp1(&'a Mbp1Msg),
    Ohlcv(&'a OhlcvMsg),
    Trade(&'a TradeMsg),
    Tbbo(&'a TbboMsg),
    Bbo(&'a BboMsg),
}

impl<'a> RecordEnumRef<'a> {
    pub fn from_ref(rec_ref: RecordRef<'a>) -> Option<Self> {
        match rec_ref.header().rtype() {
            RType::Mbp1 => rec_ref.get::<Mbp1Msg>().map(RecordEnumRef::Mbp1),
            RType::Ohlcv => rec_ref.get::<OhlcvMsg>().map(RecordEnumRef::Ohlcv),
            RType::Trade => rec_ref.get::<TradeMsg>().map(RecordEnumRef::Trade),
            RType::Tbbo => rec_ref.get::<TbboMsg>().map(RecordEnumRef::Tbbo),
            RType::Bbo => rec_ref.get::<BboMsg>().map(RecordEnumRef::Bbo),
        }
    }

    pub fn to_owned(&self) -> RecordEnum {
        match self {
            RecordEnumRef::Mbp1(msg) => RecordEnum::Mbp1((*msg).clone()),
            RecordEnumRef::Ohlcv(msg) => RecordEnum::Ohlcv((*msg).clone()),
            RecordEnumRef::Trade(msg) => RecordEnum::Trade((*msg).clone()),
            RecordEnumRef::Tbbo(msg) => RecordEnum::Tbbo((*msg).clone()),
            RecordEnumRef::Bbo(msg) => RecordEnum::Bbo((*msg).clone()),
        }
    }
}

impl<'a> Record for RecordEnumRef<'a> {
    fn header(&self) -> &RecordHeader {
        match self {
            RecordEnumRef::Mbp1(msg) => &msg.hd,
            RecordEnumRef::Ohlcv(msg) => &msg.hd,
            RecordEnumRef::Trade(msg) => &msg.hd,
            RecordEnumRef::Bbo(msg) => &msg.hd,
            RecordEnumRef::Tbbo(msg) => &msg.hd,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::records::BidAskPair;
    use dbn::FlagSet;

    #[test]
    fn test_encode_decode_record_enum() {
        let record_enum = RecordEnum::Mbp1(Mbp1Msg {
            hd: RecordHeader::new::<Mbp1Msg>(1, 1622471124),
            price: 1000,
            size: 10,
            action: 1,
            side: 1,
            depth: 0,
            flags: 0,
            ts_recv: 123456789098765,
            ts_in_delta: 12345,
            sequence: 123456,
            levels: [BidAskPair {
                bid_px: 1,
                ask_px: 2,
                bid_sz: 2,
                ask_sz: 2,
                bid_ct: 1,
                ask_ct: 3,
            }],
        });

        // Test
        let record_ref = record_enum.to_record_ref();
        let bytes = record_ref.as_ref();
        let new_ref = unsafe { RecordRef::new(bytes) };
        let ref_enum = RecordEnumRef::from_ref(new_ref).unwrap();
        let decoded = ref_enum.to_owned();

        // Validate
        assert_eq!(decoded, record_enum);
    }

    #[test]
    fn test_equality() -> anyhow::Result<()> {
        // DBN
        let header = dbn::RecordHeader::new::<dbn::Mbp1Msg>(1, 1231, 1231, 1622471124);
        let bid_ask = dbn::BidAskPair {
            bid_px: 10000000,
            ask_px: 200000,
            bid_sz: 3000000,
            ask_sz: 400000000,
            bid_ct: 50000000,
            ask_ct: 60000000,
        };

        let dbn_mbp = dbn::Mbp1Msg {
            hd: header,
            price: 12345676543,
            size: 1234543,
            action: 0,
            side: 0,
            flags: FlagSet::empty(),
            depth: 0,
            ts_recv: 1231,
            ts_in_delta: 123432,
            sequence: 23432,
            levels: [bid_ask],
        };
        let dbn_enum = dbn::RecordEnum::Mbp1(dbn_mbp);

        //MBN
        let mbn_enum = RecordEnum::Mbp1(Mbp1Msg {
            hd: RecordHeader::new::<Mbp1Msg>(1, 1622471124),
            price: 12345676543,
            size: 1234543,
            action: 0,
            side: 0,
            depth: 0,
            flags: 0,
            ts_recv: 1231,
            ts_in_delta: 123432,
            sequence: 23432,
            levels: [BidAskPair {
                bid_px: 10000000,
                ask_px: 200000,
                bid_sz: 3000000,
                ask_sz: 400000000,
                bid_ct: 50000000,
                ask_ct: 60000000,
            }],
        });

        assert!(mbn_enum == dbn_enum);

        Ok(())
    }

    #[test]
    fn test_inequality() -> anyhow::Result<()> {
        // DBN
        let header = dbn::RecordHeader::new::<dbn::Mbp1Msg>(1, 1231, 1231, 17777777777);
        let bid_ask = dbn::BidAskPair {
            bid_px: 10000000,
            ask_px: 200000,
            bid_sz: 3000000,
            ask_sz: 400000000,
            bid_ct: 50000000,
            ask_ct: 60000000,
        };

        let dbn_mbp = dbn::Mbp1Msg {
            hd: header,
            price: 12345676543,
            size: 1234543,
            action: 0,
            side: 0,
            flags: FlagSet::empty(),
            depth: 0,
            ts_recv: 1231,
            ts_in_delta: 123432,
            sequence: 23432,
            levels: [bid_ask],
        };
        let dbn_enum = dbn::RecordEnum::Mbp1(dbn_mbp);

        //MBN
        let mbn_enum = RecordEnum::Mbp1(Mbp1Msg {
            hd: RecordHeader::new::<Mbp1Msg>(1, 1622471124),
            price: 12345676543,
            size: 1234543,
            action: 0,
            side: 0,
            depth: 0,
            flags: 0,
            ts_recv: 1231,
            ts_in_delta: 123432,
            sequence: 23432,
            levels: [BidAskPair {
                bid_px: 10000000,
                ask_px: 200000,
                bid_sz: 3000000,
                ask_sz: 400000000,
                bid_ct: 50000000,
                ask_ct: 60000000,
            }],
        });

        assert!(mbn_enum != dbn_enum);

        Ok(())
    }
}
