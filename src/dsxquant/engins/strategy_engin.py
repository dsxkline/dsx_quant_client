from typing import List
from dsxquant.strategy.base import BaseStrategy    
from dsxquant.config.logconfig import logger
from dsxquant.engins.base import BaseEngin
from dsxquant import EventType

class StrategyEngin(BaseEngin):
    __name__ = "策略引擎"
    __interface_execute = "execute"
    __interface_load = "load"

    def __init__(self,event_types=None):
        super().__init__(event_types)
        self.strategies:List[BaseStrategy] = []
   
    def register(self,strategy:BaseStrategy):
        """注册需要执行的策略

        Args:
            strategy (BaseStrategy): _description_
        """
        self.strategies.append(strategy)

    def run(self):
        real = False
        while(not self.exit):
            if self.strategies:
                if self.event and self.event.target==self.__class__:
                    i = 0
                    for strategy in list(self.strategies):
                        if type(strategy)==type: 
                            strategy = strategy(self.event)
                            self.strategies[i] = strategy
                        if strategy.__type__==self.event.type:
                            if self.event.source==strategy:
                                # load
                                if hasattr(strategy,self.__interface_load):
                                    load = getattr(strategy,self.__interface_load)
                                    if callable(load):
                                        load(self.event)
                                if hasattr(strategy,"real"):
                                    real = getattr(strategy,"real")
                                # execute
                                if hasattr(strategy,self.__interface_execute):
                                    execute = getattr(strategy,self.__interface_execute)
                                    if callable(execute):
                                        event = execute()
                                        self.sendbus(event)
                        if self.event.type==EventType.THEEND and self.event.target==self.__class__:
                            # 最后一个策略运行完毕
                            if self.event.source==self.strategies[-1]:
                                # from dsxquant import EmulationEngin,TradeEngin
                                # 结束回测,通知交易组建
                                self.event.target=None
                                self.sendbus(self.event)
                                break
                        i += 1
                # 处理后销毁
                self.destroy()
                self.next()
    
   