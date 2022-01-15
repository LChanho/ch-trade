import requests
import json

def realtimeRank(size):
    custom_header = {
        'referer' : 'https://miningcalc.kr/trade/volume/upbit/',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    }

    url = 'https://api.upbit.com/v1/ticker?markets=KRW-BTC,KRW-ETH,KRW-NEO,KRW-MTL,KRW-LTC,KRW-XRP,KRW-ETC,KRW-OMG,KRW-SNT,KRW-WAVES,KRW-XEM,KRW-QTUM,KRW-LSK,KRW-STEEM,KRW-XLM,KRW-ARDR,KRW-ARK,KRW-STORJ,KRW-GRS,KRW-REP,KRW-ADA,KRW-SBD,KRW-POWR,KRW-BTG,KRW-ICX,KRW-EOS,KRW-TRX,KRW-SC,KRW-ONT,KRW-ZIL,KRW-POLY,KRW-ZRX,KRW-LOOM,KRW-BCH,KRW-BAT,KRW-IOST,KRW-RFR,KRW-CVC,KRW-IQ,KRW-IOTA,KRW-MFT,KRW-ONG,KRW-GAS,KRW-UPP,KRW-ELF,KRW-KNC,KRW-BSV,KRW-THETA,KRW-QKC,KRW-BTT,KRW-MOC,KRW-ENJ,KRW-TFUEL,KRW-MANA,KRW-ANKR,KRW-AERGO,KRW-ATOM,KRW-TT,KRW-CRE,KRW-MBL,KRW-WAXP,KRW-HBAR,KRW-MED,KRW-MLK,KRW-STPT,KRW-ORBS,KRW-VET,KRW-CHZ,KRW-STMX,KRW-DKA,KRW-HIVE,KRW-KAVA,KRW-AHT,KRW-LINK,KRW-XTZ,KRW-BORA,KRW-JST,KRW-CRO,KRW-TON,KRW-SXP,KRW-HUNT,KRW-PLA,KRW-DOT,KRW-SRM,KRW-MVL,KRW-STRAX,KRW-AQT,KRW-GLM,KRW-SSX,KRW-META,KRW-FCT2,KRW-CBK,KRW-SAND,KRW-HUM,KRW-DOGE,KRW-STRK,KRW-PUNDIX,KRW-FLOW,KRW-DAWN,KRW-AXS,KRW-STX,KRW-XEC,KRW-SOL,KRW-MATIC,KRW-NU,KRW-AAVE,KRW-1INCH,KRW-ALGO,KRW-NEAR,KRW-WEMIX'

    req = requests.get(url, headers=custom_header)

    tickers = {}

    if req.status_code == requests.codes.ok:
        #print('접속 성공')
        stock_data = json.loads(req.text)
        for i in range(len(stock_data)):
            tickers[stock_data[i]['market']] = stock_data[i]['acc_trade_price_24h']

        tickers = sorted(tickers.items(), key = lambda item: item[1], reverse=True)

        a = []
        for i in range(size):
            i = tickers[i]
            a.append(i[0])
        return a