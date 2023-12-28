import random
import sys

random.seed(21)

# Standard symbols A-M
symBase = "abcdefghijklm"

# Restricted set of symbols.
syms = "abcdefghmrwyz"

# Random ordering of the restricted set of symbols.
symRandom = ''.join(random.sample(syms,len(syms)))

#print(symRandom)

# Create map from standard symbol to the randomized order of restricted symbols.
symMap = {}
for i in range(0, len(symBase)):
	symMap[symBase[i]] = symRandom[i]

# Standard arrangement of 13 dobble cards using standard symbols.
dobble13 = [
	['a', 'b', 'c', 'd',                                                  ],
	['a',                 'e', 'f', 'g',                                  ],
	['a',                                 'h', 'i', 'j',                  ],
	['a',                                                 'k', 'l', 'm',  ],

	[     'b',            'e',            'h',            'k',            ],
	[     'b',                 'f',            'i',            'l',       ],
	[     'b',                      'g',            'j',            'm',  ],

	[          'c',       'e',                 'i',                 'm',  ],
	[          'c',            'f',                 'j',   'k',           ],
	[          'c',                 'g',  'h',                  'l',      ],

	[               'd',  'e',                      'j',        'l',      ],
	[               'd',       'f',       'h',                       'm', ],
	[               'd',            'g',       'i',        'k',           ],
]

# Calc dobble set with randomized, restricted symbols.
d13set = []
for d in dobble13:
	sym = [symMap[x] for x in d]
	sym.sort(reverse=True)
	d13set.append(sym)

#print(d13set)

# The possible way we can select 2 of the 4 symbols.
# We want to make sure we don't use one pattern too often.
patterns = ["0011", "0101", "0110", "1001", "1010", "1100"]

def valid(selectPats, d13):
	# Counts for each symbol
	sums = {}
	for s in list(syms):
		sums[s] = 0

	# Track the patterns used for each symbol.
	symPats = {}
	for s in list(syms):
		symPats[s] = set()
	
	for i in range(len(selectPats)):
		select = list(selectPats[i])
		for iSelect in range(len(select)):
			if select[iSelect] == '1':
				sums[d13[i][iSelect]] += 1
				symPats[d13[i][iSelect]].add(selectPats[i])
	
	# If any symbol occurs more than 2 times, then this is invalid.
	for s in list(syms):
		if sums[s] > 2:
			return False

	# If we have patterns for each card, then check the pattern distribution.
	if len(selectPats) == 13:
		# If a symbol only uses a pattern once, then invalid.
		for s in list(syms):
			if len(symPats[s]) == 1:
				return False
	
		pSums = {}
		for p in patterns:
			pSums[p] = 0
		for p in selectPats:
			pSums[p] += 1
		# Make sure each pattern is used at least twice.
		for p in patterns:
			if pSums[p] < 2:
				return False

	return True

def print_selection(selectPats, d13):
	# Counts for each symbol
	sums = {}
	for s in list(syms):
		sums[s] = 0

	# Track the patterns used for each symbol.
	symPats = {}
	for s in list(syms):
		symPats[s] = set()

	for i in range(len(selectPats)):
		select = list(selectPats[i])
		p = []
		for iSelect in range(len(select)):
			if select[iSelect] == '1':
				sums[d13[i][iSelect]] += 1
				p.append(d13[i][iSelect])
				symPats[d13[i][iSelect]].add(selectPats[i])
			else:
				p.append('_')
		print(d13[i], "->", p)

	# Each symbol must appear exactly twice.
	for s in list(syms):
		if sums[s] != 2:
			print("Invalid!")
	#print(sums)

	# Print patterns used for each symbol.
	for s in list(syms):
		print(s, symPats[s])
	
	# Count how many times each pattern occurs.
	pSums = {}
	for p in patterns:
		pSums[p] = 0
	for p in selectPats:
		pSums[p] += 1
	print(pSums)

def find_patterns():
	for i in patterns:
		for ii in patterns:
			p = [i, ii]
			if not valid(p, d13set):
				continue
			for iii in patterns:
				p = [i, ii, iii]
				if not valid(p, d13set):
					continue
				for iv in patterns:
					p = [i, ii, iii, iv]
					if not valid(p, d13set):
						continue
					for v in patterns:
						p = [i, ii, iii, iv, v]
						if not valid(p, d13set):
							continue
						for vi in patterns:
							p = [i, ii, iii, iv, v, vi]
							if not valid(p, d13set):
								continue
							for vii in patterns:
								p = [i, ii, iii, iv, v, vi, vii]
								if not valid(p, d13set):
									continue
								for viii in patterns:
									p = [i, ii, iii, iv, v, vi, vii, viii]
									if not valid(p, d13set):
										continue
									for ix in patterns:
										p = [i, ii, iii, iv, v, vi, vii, viii, ix]
										if not valid(p, d13set):
											continue
										for x in patterns:
											p = [i, ii, iii, iv, v, vi, vii, viii, ix, x]
											if not valid(p, d13set):
												continue
											for xi in patterns:
												p = [i, ii, iii, iv, v, vi, vii, viii, ix, x, xi]
												if not valid(p, d13set):
													continue
												for xii in patterns:
													p = [i, ii, iii, iv, v, vi, vii, viii, ix, x, xi, xii]
													if not valid(p, d13set):
														continue
													for xiii in patterns:
														p = [i, ii, iii, iv, v, vi, vii, viii, ix, x, xi, xii, xiii]
														if valid(p, d13set):
															print_selection(p, d13set)

find_patterns()
