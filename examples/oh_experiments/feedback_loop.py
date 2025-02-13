# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.

import os
import re
import siliconcompiler

def main():
    # Setting up the experiment
    rootdir = (os.path.dirname(os.path.abspath(__file__)) +
               "/../../third_party/designs/oh/")

    design = 'oh_add'
    N = 8

    # Plugging design into SC
    chip = siliconcompiler.Chip(design)
    chip.add('input', 'verilog', rootdir+'/mathlib/hdl/'+design+'.v')
    chip.set('option', 'param', 'N', str(N))
    chip.set('option', 'relax', True)
    chip.set('option', 'quiet', True)
    chip.load_target('freepdk45_demo')

    # First run (import + run)
    steplist = ['import', 'syn']
    chip.set('option', 'steplist', steplist)
    chip.run()


    # Setting up the rest of the runs
    while True:

        # design experiment, width of adder
        N = N * 2
        chip.set('option', 'param', 'N', str(N), clobber=True)

        # Running syn only
        index = '0'
        step = 'syn'
        chip.set('option', 'steplist', ['syn'])

        # Setting a unique jobid
        oldid = chip.get('option', 'jobname')
        match = re.match(r'(.*)(\d+)$', oldid)
        newid = match.group(1) + str(int(match.group(2))+1)
        chip.set('option', 'jobname', newid)

        # Specifying that imports are copied from job0
        chip.set('option', 'jobinput', step, index, 'job0')

        # Make a run
        chip.run()

        # Query current run and last run
        new_area = chip.get('metric', step, index, 'cellarea')
        old_area = chip.get('metric', step, index, 'cellarea', job=oldid)

        # compare result
        print(N, new_area, old_area, newid, chip.get('option', 'jobname'))
        if (new_area/old_area) > 2.1:
            print("Stopping, area is exploding")
            break

if __name__ == '__main__':
    main()
