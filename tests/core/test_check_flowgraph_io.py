import siliconcompiler

def test_check_flowgraph():
    chip = siliconcompiler.Chip()

    chip.set('design', 'foo')
    chip.add('source', 'foo.v')

    chip.node('import', 'surelog')
    chip.node('syn', 'yosys')
    chip.edge('import', 'syn')

    for step in chip.getkeys('flowgraph'):
        for index in chip.getkeys('flowgraph', step):
            stepstr = step + index
            # Setting up tool is optional
            tool = chip.get('flowgraph', step, index, 'tool')
            if tool not in chip.builtin:
                chip.set('arg','step', step)
                chip.set('arg','index', index)
                func = chip.find_function(tool, 'tool', 'setup_tool')
                func(chip)
                # Need to clear index, otherwise we will skip
                # setting up other indices. Clear step for good
                # measure.
                chip.set('arg','step', None)
                chip.set('arg','index', None)

    assert chip._check_flowgraph_io()
