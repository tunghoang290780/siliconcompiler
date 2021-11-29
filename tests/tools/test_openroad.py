# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.
import os
import siliconcompiler
import pytest

@pytest.mark.eda
@pytest.mark.quick
def test_openroad(scroot):
    datadir = os.path.join(scroot, 'tests', 'data')

    # TODO: this filename used to be oh_fifo_sync_freepdk45.vg, but it was
    # changed to make the filename match with the design name in order for flow
    # file I/O checking to work right. We should think about how to eliminate
    # this restriction (or decide that we just want to accept it).
    netlist = os.path.join(datadir, 'oh_fifo_sync.vg')

    design = "oh_fifo_sync"

    chip = siliconcompiler.Chip()
    chip.set('design', design)
    chip.set('netlist', netlist)
    chip.set('mode', 'asic')
    chip.set('quiet', True)
    chip.set('asic', 'diearea', [(0,0), (100.13,100.8)])
    chip.set('asic', 'corearea', [(10.07,11.2), (90.25,91)])
    chip.set('arg','step', 'floorplan')
    chip.target("openroad_freepdk45")
    chip.run()

    # check that compilation succeeded
    assert chip.find_result('def', step='floorplan') is not None

#########################
if __name__ == "__main__":
    from tests.fixtures import scroot
    test_openroad(scroot())
