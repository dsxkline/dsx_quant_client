import threading
from typing import List
from dsxquant.engins.event_bus import EventBus
from dsxquant.engins.event_model import EventModel
from dsxquant import EventType
from dsxquant.strategy.base import BaseStrategy    
from dsxquant.config.logconfig import logger
from dsxquant.engins.base import BaseEngin
from dsxquant.emulation.base import BaseEmulation
from dsxquant.emulation.buy import BuyEmulation
from dsxquant.emulation.cancel import CancelEmulation
from dsxquant.emulation.sell import SellEmulation

class EmulationEngin(BaseEngin):
    __name__ = "仿真交易引擎"
    __interface_execute = "execute"
    
    def __init__(self,event_types:List[EventType]=None):
        super().__init__(event_types)
        self.emulations:List[BaseEmulation] = []
        self.autoregister()
    
    def autoregister(self):
        self.register(BuyEmulation)
        self.register(SellEmulation)
        self.register(CancelEmulation)
   
    def register(self,emulation:BaseEmulation):
        """注册需要执行的仿真交易

        Args:
            emulation (BaseStrategy): _description_
        """
        self.emulations.append(emulation)
    
    def run(self):
        while(not self.exit):
            if self.event and self.event.target==self.__class__:
                for emulation in self.emulations:
                    if emulation.__type__==self.event.type:
                        if type(emulation)==type: emulation = emulation(self.event)
                        if hasattr(emulation,self.__interface_execute):
                            method = getattr(emulation,self.__interface_execute)
                            if callable(method):
                                event = method()
                                self.sendbus(event)
            # 处理后销毁
            self.destroy()
            self.next()
    
   