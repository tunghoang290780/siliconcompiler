import os
import re
import shutil
import siliconcompiler
from siliconcompiler.tools.netgen import count_lvs

####################################################################
# Make Docs
####################################################################
def make_docs():
    '''
    Netgen is a tool for comparing netlists. By comparing a Verilog netlist with
    one extracted from a circuit layout, it can be used to perform LVS
    verification.

    Documentation: http://www.opencircuitdesign.com/netgen/

    Installation: https://github.com/RTimothyEdwards/netgen

    Sources: https://github.com/RTimothyEdwards/netgen

    '''

    chip = siliconcompiler.Chip()
    chip.target('skywater130')
    chip.set('arg','index','<index>')

    # check lvs
    chip.set('arg','step', 'lvs')
    setup_tool(chip)

    return chip

################################
# Setup Tool (pre executable)
################################

def setup_tool(chip):
    ''' Setup function for 'magic' tool
    '''

    tool = 'netgen'
    refdir = 'tools/'+tool
    step = chip.get('arg','step')
    index = chip.get('arg','index')

    # magic used for drc and lvs
    script = 'sc_lvs.tcl'

    chip.set('eda', tool, step, index, 'exe', tool)
    chip.set('eda', tool, step, index, 'vswitch', '-batch')
    chip.set('eda', tool, step, index, 'version', '1.5.192')
    chip.set('eda', tool, step, index, 'threads', 4)
    chip.set('eda', tool, step, index, 'refdir', refdir)
    chip.set('eda', tool, step, index, 'script', refdir + '/' + script)

    # set options
    options = []
    options.append('-batch')
    options.append('source')
    chip.set('eda', tool, step, index, 'option', options, clobber=False)

    design = chip.get('design')
    chip.add('eda', tool, step, index, 'input', f'{design}.spice')
    chip.add('eda', tool, step, index, 'input', f'{design}.vg')
    chip.add('eda', tool, step, index, 'output', f'{design}.lvs.out')

################################
# Version Check
################################

def parse_version(stdout):
    # First line: Netgen 1.5.190 compiled on Fri Jun 25 16:05:36 EDT 2021
    return stdout.split()[1]

################################
# Post_process (post executable)
################################

def post_process(chip):
    ''' Tool specific function to run after step execution

    Reads error count from output and fills in appropriate entry in metrics
    '''
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    design = chip.get('design')

    if step == 'lvs':
        # Export metrics
        lvs_failures = count_lvs.count_LVS_failures(f'outputs/{design}.lvs.json')

        # We don't count top-level pin mismatches as errors b/c we seem to get
        # false positives for disconnected pins. Report them as warnings
        # instead, the designer can then take a look at the full report for
        # details.
        pin_failures = lvs_failures[3]
        errors = lvs_failures[0] - pin_failures
        chip.set('metric', step, index, 'errors', 'real', errors)
        chip.set('metric', step, index, 'warnings', 'real', pin_failures)

    #TODO: return error code
    return 0

##################################################
if __name__ == "__main__":

    # File being executed
    prefix = os.path.splitext(os.path.basename(__file__))[0]
    output = prefix + '.json'

    # create a chip instance
    chip = siliconcompiler.Chip(loglevel="INFO")
    # load configuration
    chip.target('skywater130_asicflow')
    chip.set('arg','index','0')
    chip.set('arg','step','lvs')
    setup_tool(chip)
    # write out results
    chip.writecfg(output)
