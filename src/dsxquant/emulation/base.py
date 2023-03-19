from dsxquant import EventType
from dsxquant.engins.event_model import EventModel
from dsxquant.orders.orders import Orders

class BaseEmulation:
    # 定义自己处理的类型
    __type__:EventType = EventType.NONE
    __title__ = "仿真交易名称"
    __desc__ = "描述"

    def __init__(self,event:EventModel) -> None:
        self.event:EventModel = event
        # 最好有包装类
        self.data = self.event.data
        # 订单管理
        self.orders:Orders = Orders(self.event.source,self.event.source.symbol)
        pass

    def execute(self):
        pass