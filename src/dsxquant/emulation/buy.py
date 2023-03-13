from dsxquant import EventType
from dsxquant.emulation.base import BaseEmulation
from dsxquant import logger

class BuyEmulation(BaseEmulation):
    __title__ = "买入仿真"
    __desc__ = "描述"
    __type__ = EventType.BUY

    def execute(self):
        datas = self.data
        logger.info("仿真交易买入%s"%datas)