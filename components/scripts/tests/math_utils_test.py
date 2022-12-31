import pytest

from math_utils import (feq_pt, feq_line,
						parallel_lines, perp_offset)

def checkPerpOffset(line, d, r0, r1):
	r = perp_offset(line, d)
	assert feq_pt(r[0], r0)
	assert feq_pt(r[1], r1)

def test_perp_offset():
	checkPerpOffset([[0,0], [0,10]], 5, [-5,0], [5,0])
	checkPerpOffset([[0,0], [10,10]], 5, [-3.535534,3.535534], [3.535534,-3.535534])

def checkParallelLines(line, d, line0, line1):
	r = parallel_lines(line, d)
	assert feq_line(r[0], line0)
	assert feq_line(r[1], line1)

def test_parallel_lines():
	checkParallelLines([[0,0], [0,10]], 5, [[-5,0],[-5,10]], [[5,0],[5,10]])
	checkParallelLines([[0,0], [10,10]], 5, [[-3.535534,3.535534], [6.4644661,13.535534]], [[3.535534,-3.535534],[13.535534,6.4644661]])
