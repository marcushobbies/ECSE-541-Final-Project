from gem5.isas import ISA
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor

from m5.objects.ArmCPU import ArmO3CPU
from m5.objects.FuncUnitConfig import *

class ArmA9O3(ArmO3CPU):
    def __init__(self):
        super().__init__()
        self.fetchWidth = 8
        self.decodeWidth = 8
        self.renameWidth = 8
        self.dispatchWidth = 8
        self.issueWidth = 8
        self.wbWidth = 8
        self.commitWidth = 8

        self.numROBEntries = 256
        self.numPhysIntRegs = 512
        self.numPhysFloatRegs = 512

class ArmA9Core(BaseCPUCore):
    def __init__(self):
        core = ArmA9O3();
        super().__init__(core, ISA.ARM)

class ArmA9Processor(BaseCPUProcessor):
    def __init__(self):
        core_list = [ArmA9Core()]
        super().__init__(
            clk_freq="3GHz",
            cores = core_list
        )