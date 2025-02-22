#!/usr/bin/env python

import sys
from pyparsing import (Word, Group, SkipTo, StringEnd,
                       Suppress, ZeroOrMore,
                       alphas, nums, alphanums, printables,
                       oneOf)

s = Suppress

identifier = Word(printables)('id') 

definition = Word(alphas)('type') + Word(nums)('size') + \
             identifier + Word(printables)('name')

signal = Group(s('$var') + definition + s('$end'))('signal')

content = SkipTo('$end')('content') + s('$end')
section = Group(s('$') + Word(alphas)('name') + content)('section')

unit      = s('1') + oneOf('s ms ns us ps fs')
timescale = (s('$timescale') + unit + s('$end'))('timescale')

scope   = Group(s('$scope module') + Word(printables)('module') + s('$end'))('scope')
upscope = Group(s('$upscope') + s(content))('upscope')

enddefinitions = s('$enddefinitions' + content)

time = s('#') + Word(nums)('time')

std_logic        = oneOf('U X 0 1 Z W L H-')('std_logic')
std_logic_vector = Word('b', 'UX01ZWLH-')('std_logic_vector')

value = Group((std_logic | std_logic_vector ) + identifier)('value')
step  = Group(time + ZeroOrMore(value))('step')

headers = signal | timescale | scope | upscope
changes = enddefinitions + ZeroOrMore(step) + StringEnd()

vcd = ZeroOrMore(headers | changes | section)('vcd')
