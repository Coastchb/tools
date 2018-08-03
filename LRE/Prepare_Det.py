#!/usr/bin/env python
# Copyright 2016  Tsinghua University
#                 (Author: Yixiang Chen, Lantian Li, Dong Wang)
# Licence: Apache 2.0


import sys


# Load the result file in the following format
# <lang-id> ct-cn     id-id     ja-jf     ko-kr     ru-ru     vi-vn     zh-cn
# <utt-id>  <score1>  <score2>  <score3>  <score4>  <score5>  <score6>  <score7>

# The language identity is defined as: 
# 1: ct-cn, 2: id-id, 3: ja-jf, 4: ko-kr, 5: ru-ru, 6: vi-vn, 7: zh-cn


dictl = {'c':1, 'i':2, 'j':3, 'k':4, 'r':5, 'v':6, 'z':7}

# Load scoring file and label.scp.
def Loaddata(fin, labelscp):
	x = []
	for i in range(8):
		x.append(0)
	fin = open(fin, 'r')
	lines = fin.readlines()
	fin.close()

	labelscp = open(labelscp, 'r')
	linesw = labelscp.readlines()
	labelscp.close()

	labelscpdict = {}
	for line in linesw:
		part = line.split()
		labelscpdict[part[0].split('.')[0]] = part[1]
		
	label = []
	part = lines[0].split()
	for i in range(7):
		label.append(dictl[part[i][0]])

	data = []

	for line in lines[1:]:
		part = line.split()
		x[0] = labelscpdict[part[0].split('.')[0]]
		for i in range(7):
			x[label[i]] = part[i + 1]
		data.append(x)
		x = []
		for i in range(8):
			x.append(0)

	return data


# Generate target trials and nontarget trials.
# Prepare for plotting DET curves and computing EER / minDCF.
# data: matrix for result scores.
def fun(data, targetf, nontargetf):
	
	targetf = open(targetf, 'w')
	nontargetf = open(nontargetf, 'w')
	for part in data:
		lan = part[0].split('_')[0]
		for j in range(7):
			if j + 1 == dictl[lan[0]]:
				targetf.write(part[j + 1] + '\n')
			else:
				nontargetf.write(part[j + 1] + '\n')
	targetf.close()
	nontargetf.close()


if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print "usage %s <result file path> <label file path>" % (sys.argv[0])
        exit(0)
    
    data = Loaddata(sys.argv[1], sys.argv[2])
    fun(data,'DET/target.txt','DET/nontarget.txt')
