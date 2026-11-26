from gem5.isas import ISA
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.boards.arm_board import ArmBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes

from gem5.components.processors.simple_processor import SimpleProcessor

# for downloading the workload
from gem5.resources.resource import BinaryResource, WorkloadResource, obtain_resource

# to run the simulation
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent


"""
A simple gem5 configuration script that uses custom out-of-order CPUs, 
BigProcessor and LittleProcessor, defined in my_processors.py.

This script runs an x86 matrix multiply workload to its completion.
"""

from processors import ArmA9Processor


processor = ArmA9Processor()

cache = PrivateL1SharedL2CacheHierarchy(
    l1d_size = "32KiB",
    l1i_size = "32KiB",
    l2_size = "512KiB",
    l1d_assoc = 4,
    l1i_assoc = 4,
    l2_assoc = 8
)

memory = SingleChannelDDR4_2400(
    size = "3GiB"
)


board = SimpleBoard(
    clk_freq="800MHz",
    processor = processor,
    cache_hierarchy = cache,
    memory = memory
)

print("Setting workload...")

#board.set_workload(obtain_resource("arm-ubuntu-24.04-npb-sp-s", resource_version="2.0.0"))
board.set_se_binary_workload(obtain_resource(resource_id="arm-npb-cg-size-s"))

def exit_event_handler():
    print('first exit event: Kernel booted')
    yield False
    print('second exit event: In after boot')
    yield False
    print('third exit event: After run script')
    yield True

print("Setup simulator...")


simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler(),
    },
)

print("Running simulator...")

simulator.run()