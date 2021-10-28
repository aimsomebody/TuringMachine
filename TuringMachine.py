import sys
import json
from abc import ABC, abstractmethod
from time import sleep

class rules():
	def __init__(self):
		self.rules = []
		self.ruleCount = 0

	def addRule(self, rl):
		self.rules.append({"state": int(rl[0]), "read": rl[1], 
					"write": rl[2], "move": rl[3], "nextState": int(rl[4])})
		self.addRuleCount()
		return

	def addRuleCount(self):
		self.ruleCount = self.ruleCount + 1
		return

	def getRuleCount(self):
		return self.ruleCount

	def getRule(self,row):
		return self.rules[row]

	def getState(self, row):
		return self.rules[row]["state"] 

	def getRead(self, row):
		return self.rules[row]["read"] 

	def getWrite(self, row):
		return self.rules[row]["write"] 

	def getMove(self, row):
		return self.rules[row]["move"] 

	def getNextState(self, row):
		return self.rules[row]["nextState"] 


class tape():
	def __init__(self):
		self.tape = {}
		self.headPosition = 0 

	def setTape(self, tp):
		self.tape = list(tp)
		return

	def setHeadPosition(self, hp):
		self.headPosition = int(hp)
		return 

	def moveLeft(self):
		self.headPosition = self.headPosition - 1
		return

	def moveRight(self):
		self.headPosition = self.headPosition + 1
		return

	def updateTape(self, value):
		self.tape[self.getCurrentPosition()] = value

	def getCurrentN(self):
		return self.tape[self.getCurrentPosition()]

	def getCurrentPosition(self):
		return int(self.headPosition)

	def getTape(self):
		return "".join(map(str,  [str(nt) for nt in self.tape]))		


class params():
	def __init__(self):
		self.rules = rules()
		self.tape = tape()
	def rulesParam(self):
		return self.rules

	def tapeParam(self):
		return self.tape

class parser(ABC):
	def __init__(self,params):
		self.params = params

	@abstractmethod
	def parse(self,lines):
		pass

class txtParser(parser):
	def parse(self,filename):
		with open(filename) as f:
			lines = f.readlines()
		self.params.tapeParam().setHeadPosition(lines[0].split()[0])
		self.params.tapeParam().setTape(lines[1].split()[0])
		for i in range(2,len(lines)):
			n = lines[i].split()
			self.params.rulesParam().addRule(n)
		return


class jsonParser(parser):
	def parse(self,filename):
		with open(filename) as jsonFile:
			data = json.load(jsonFile)
		self.params.tapeParam().setHeadPosition(data["head-start-position"].split()[0])
		self.params.tapeParam().setTape(data["tape"].split()[0])
		rl = []
		for i in data["rules"]:
			for x in i:
				rl.append(i[x])
			self.params.rulesParam().addRule(rl)
			rl = []
		return

class tmProcessor():
	def __init__(self,params):
		self.rules = params.rulesParam()
		self.tape = params.tapeParam()
		self.state = 0

	def readTapeNRules(self):
		while(1):
			for i in range(self.rules.getRuleCount()):
				if self.rules.getState(i) == self.state and self.rules.getRead(i) == self.tape.getCurrentN():
					self.tape.updateTape(self.rules.getWrite(i))
					if self.rules.getMove(i) == "L":
						self.tape.moveLeft()
					else:
						self.tape.moveRight()						
					self.state = int(self.rules.getNextState(i))
					# sleep(0.05)
					print(self.tape.getTape())



if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("tm.py (json or txt file)")
		exit()

	filename = sys.argv[1]
	rulesAndTape = params()
	try:
		m = globals()[filename.split(".")[-1]+"Parser"](rulesAndTape)
		func = getattr(m,"parse")
		func(filename)
		tmProcessor(rulesAndTape).readTapeNRules()
	except KeyError:
		print("Error: 	Class with this name is not defined!")
		exit()

	# print(txtParser.__mro__)


