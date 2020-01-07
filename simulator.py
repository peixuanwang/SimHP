# -*- coding: utf-8 -*-
"""
Created on Thu Jul	5 13:32:05 2018

@author: Peixuan
"""


import random
import re
import sys
import getopt
import numpy as np
import time

class HPOBase(object):
	def __init__(self,_id):
		self._id=_id
		self.alt_ids=[]
		self.name=''
		self.parent=None
		self.level=-1 
		self.allParents=None 
		
class ObOs(object):
	def __init__(self,path):
		self.path=path
		self.map={}
		self.parseObO()
	def parseObO(self):
		f=open(self.path)
		lines=f.readlines()
		f.close()
		_hpoTxt=[]
		flag=False
		for line in lines:
			line=line.rstrip('\n').strip()
			if flag:
				_hpoTxt.append(line)
			if flag and line=='':
				self.parseHPO(_hpoTxt)
				_hpoTxt=[]
				flag=False
			if line.find('[Term]')==0:
				flag=True
				
	def parseHPO(self,_hpoText):
		_id=None
		_name=''
		#_namespace=''
		_is_as=[]
		_alt_ids=[]
		for _txt in _hpoText:
			if _txt.find('id:')==0:
				_id=_txt[_txt.find('HP'):_txt.find('HP')+10]
			elif _txt.find('name:')==0:
				_name=_txt[5:len(_txt)].rstrip().lstrip()
			elif _txt.find('alt_id:')==0:
				_alt_ids.append(_txt[_txt.find('HP'):_txt.find('HP')+10]) 
			elif _txt.find('is_a:')==0:
				_is_as.append(_txt[_txt.find('HP'):_txt.find('HP')+10]) 
		if _id:
			_hpo=None
			if _id in self.map:
				_hpo=self.map[_id]
			else:
				_hpo=HPOBase(_id)	
			_hpo.name=_name
			_hpo.parent=self.parseParent(_is_as)
			_hpo.alt_ids=_alt_ids
			self.map[_id]=_hpo
			if len(_alt_ids)>0:
				for _alt in _alt_ids:
					self.map[_alt]=_hpo 
	
						   
	def parseParent(self,is_as):
		__parent=[]
		for isa in is_as:
			if isa not in self.map:
				cHPO=HPOBase(isa)
				self.map[isa]=cHPO
			__parent.append(isa)
		return __parent
	
	def getLevel(self,_id):
		_min=100000
		_hpo=self.map[_id]
		if _hpo.level>0:
			pass
		elif len(_hpo.parent)==0:
			_hpo.level=1
		else:
			for g in _hpo.parent:
				lev=self.getLevel(g)
				if _min>lev:
					_min=lev
			_hpo.level=_min+1
		return _hpo.level
		
	def getAllParent(self,_id):
		_prs=[_id]
		_hpo=self.map[_id]
		if not _hpo.allParents is None:
			return _hpo.allParents
		if _hpo.parent is None or len(_hpo.parent)==0:
			_hpo.allParents=_prs
			return _hpo.allParents
		for g in _hpo.parent:
			ap=self.getAllParent(g)
			_prs.extend(ap)
		_hpo.allParents=list(set(_prs))
		return _hpo.allParents	 
	
def dis_hp(table,obo):
	ff = open(table,'r')
	hpo_disease = {}
	disease_hpo = {}
	dis_hp_freq = {}
	hp_level = {}
	hpall = []
	dis_name = {}
	hp_name = {}
	o = ObOs(obo)
	line = ff.readline()
	while True:
		line = ff.readline()
		if not line: break
		tmp = re.match('^OMIM',line)
		if tmp is not None:
			it = line.split('\t')
			dise = it[0].strip()+':'+str(re.findall(r"\d{6}",it[1].strip())[0])
			name = it[2].strip()
			if dise not in dis_name:
				dis_name[dise] = name
			freq = 1
			info = re.match('(\d+)/(\d+)',it[13])
			if info is not None:
				freq = float(info.group(1))/float(info.group(2))
			info = re.match('(\d+)\sof\s(\d+)',it[13])
			if info is not None:
				freq = float(info.group(1))/float(info.group(2))
			info = re.match('(\d+)%',it[13])
			if info is not None:
				freq = float(info.group(1))*0.01
			info = re.match('(\d+\.\d+)%',it[13])
			if info is not None:
				freq = float(info.group(1))*0.01	   
			info = re.match('(\d+)-(\d+)%',it[13])
			if info is not None:
				freq = (int(info.group(1))+int(info.group(2)))*0.01/2
			info = re.match('(\d+)%-(\d+)%',it[13])
			if info is not None:
				freq = (int(info.group(1))+int(info.group(2)))*0.01/2
			info = re.match('[Cc]ommon',it[13])
			if info is not None:
				freq = 0.5
			info = re.match('[Ff]requent',it[13])
			if info is not None:
				freq = 0.33
			info = re.match('[Hh]allmark',it[13])
			if info is not None:
				freq = 0.9
			info = re.match('[Oo]bligate',it[13])
			if info is not None:
				freq = 1
			info = re.match('[Oo]ccasional',it[13])
			if info is not None:
				freq = 0.1
			info = re.match('[Rr]are',it[13])
			if info is not None:
				freq = 0.05
			info = re.match('[Tt]ypical',it[13])
			if info is not None:
				freq = 0.5
			info = re.match('[Vv]ariable',it[13])
			if info is not None:
				freq = 1
			info = re.match('[Vv]ery\srare',it[13])
			if info is not None:
				freq = 0.01
			info = re.match('[Vv]ery\sfrequent',it[13])
			if info is not None:
				freq = 0.45
			hp = it[4].strip()
			dis_hp_freq[dise,hp] = freq
			if not hp in hpo_disease:
				hpo_disease[hp] = set()
			if not hp in hp_level:
				hp_level[hp] = o.getLevel(hp)
				hpall.append(hp)
			hpo_disease[hp].add(dise)
			if not dise in disease_hpo:
				disease_hpo[dise] = set()
			disease_hpo[dise].add(hp)
	ff.close()
	f = open(obo,'r').read()
	omim_obo = re.split("\[Term\]",f)
	omim_obo = omim_obo[1:]
	hp_name2 = {}
	for i in omim_obo:
		i = i.strip()
		lines = re.split("\n",i)
		id = ''
		for l in lines:
			m = re.match('id:\s(HP:\d{7})',l)
			if m is not None:
				id = m.group(1)
			m3 = re.match('^name:\s(.*)$',l)
			if m3 is not None:
				name = m3.group(1)
		if id not in hp_name2:
			hp_name[id] = name

	return disease_hpo,dis_hp_freq,hpall,dis_name,hp_name,o



def sim(_omim,obo,length,impre,noi,disease_hpo,dis_hp_freq,hpall,o,freq,freq_value):    
	fhp = []
	orghp = []
	prthp = []
	unrelatedhp = []
	subhp = []
	subhp_prt = []
	subhp_org = []
	subhp_noise = []
	prt = []
	nl = 0
	if freq:
		for hp in disease_hpo[_omim]:
			if not freq_value:		 
				freq_value = random.uniform(0,1)
			if (freq_value <= dis_hp_freq[_omim,hp]):
				fhp.append(hp)
	else:
		fhp = disease_hpo[_omim]
	orghp = list(set(fhp))
	m = re.match("^\[(\d+),(\d+)\]$",length)
	mm = re.match("^[0-9]+$",length)
	if not m is None:
		lower = int(m.group(1))
		upper = int(m.group(2))
		nl = np.random.randint(lower,upper)
	elif not mm is None:
		nl = int(length)
	else: 
		print ('-l <length> Error. Please input format like [4,20] or a none zreo integer number.')
		sys.exit()		  
	if nl == 0:
		print ('-l <length> Error. Please input format like [4,20] or a none zreo integer number.')
		sys.exit()
	
	nl_prt = int(round(nl*impre))
	nl_noise = int(round(nl*noi))
	nl_org = nl - nl_noise - nl_prt
		
	for hp in orghp:
		prt = list(set(o.getAllParent(hp)).difference(set(orghp)))
		if len(prt) > 0:
			prthp.extend(prt)
	prthp = list(set(prthp))
	relatedhp = orghp + prthp
	
	if len(orghp) < nl_org:
		if m is not None:
			print ('-l <length> Warning. The length is larger than the knowledge base. Replaced by random length.')
		if mm is not None:
			print ('-l <length> Warning. The length is larger than the knowledge base. Replaced by random length.')
		nl = np.random.randint(1,int(round(len(orghp)/(1 - noi - impre))))
		nl_prt = int(round(nl*impre))
		nl_org = int(round(nl*(1 - noi - impre)))
		nl_noi = nl - nl_prt - nl_org

	if nl_prt == 0:
		subhp_org = random.sample(orghp,nl_org)
		unrelatedhp = list(set(hpall).difference(set(relatedhp)))
	else:
		subhp_prt = random.sample(prthp,nl_prt)
		unrelatedhp = list(set(hpall).difference(set(relatedhp)))
		subhp_org = random.sample(orghp,nl_org)    
	if nl_noise == 0:
		subhp_noise = []
	else:
		subhp_noise = random.sample(unrelatedhp,nl_noise)	 
	subhp = subhp_org + subhp_prt + subhp_noise    
	return subhp


def omimlist(inputfile):
	omimlist = []
	f = open(inputfile,'r')
	lines = f.readlines()
	for line in lines:
		line = line.rstrip('\n').strip()
		if len(line) != 0:
			inline = re.match("^(OMIM:\d{6})$",line.upper())
			inline2 = re.match("^(\d{6})$",line)
			if (inline is None) and (inline2 is None):
				print(line + ":invalid input.")
				sys.exit()
			elif not inline is None:
				if not (inline.group(1)).upper() in omimlist:
					omimlist.append((inline.group(1)).upper())
			elif not inline2 is None:
				line2 = "OMIM:" + inline2.group(1)
				if not line2 in omimlist:
					omimlist.append(line2)
			
	f.close()
	return(omimlist)

def RandomOmim(disease_hpo,r,length):
	dis = []
	m = re.match("^\[(\d+),(\d+)\]$",length)
	mm = re.match("^[0-9]+$",length)
	if not m is None:
		upper = int(m.group(2))
		nl = upper
	elif not mm is None:
		nl = int(length)
	else: 
		print ('-l <length> Error. Please input format like [4,20] or a none zreo integer number.')
		sys.exit()		 
	for i in disease_hpo:
		if len(disease_hpo[i]) >= nl:
			dis.append(i)
	randomomim = random.sample(dis,r)
	return randomomim

def usage():
	print( '########################################################################')
	print( '#					  simulator on patient HPO data					   #')
	print( '########################################################################')
	print( '\nsimulator.py:')
	print( 'Generate your simulated patients phenotype data on your interested ')
	print( 'disease by your input OMIM numbers. You can also get random diseases ')
	print( 'data. The releases date of default obo file and phenotype annotation ')
	print( 'table is 2019-11-08. You can download the newest files from HPO website:')
	print( 'http://purl.obolibrary.org/obo/hp.obo')
	print( 'Make sure your disease has OMIM number in the file. \n')
	print( 'NOTE: You must set your outputfile by using -o. ' )
	print( '	  If you do not set -i input file, we will generate random diseases.' )
	print( '	  You can set the counts of random diseases by using -r.' )
	print( '\n')
	print( 'Mandatory parameter:\n')
	print( '	-o	 Output file.\n')
	print( 'Options:\n')
	print( '	-i	 One OMIM number or a inputfile(a list of OMIM numbers, separated')
	print( '		 by "\\n").')
	print( '	-b	 Hpo OBO file downloaded from HPO website. Default: hp.obo.')
	print( '	-t	 phenotype_annotation.tab file downloaded from HPO website.')
	print( '		 Default: phenotype_annotation.tab.')
	print( '	-r	 The numbers of random diseases. Default: 5.'  )
	print( '	-c	 Patient numbers per disease. Default: 20.') 
	print( '	-l	 The number range of patients HPs, Default: [4,20]. ')
	print( '		 You can also set a specific number such us 10.')
	print( '	-m	 Percent of query HP terms replaced by one of its ancestor, ')
	print( '		 greater than or equal to 0 and less than 1, Default: 0.2. ')
	print( '	-n	 Percent of unrelated terms randomly added to query HP terms,') 
	print( '		 greater than or equal to 0 and less than 1, Default: 0.15.\n')
	print( '	-v	 cuf-off frequency value to filter HP term and you need to set -f before use it.\n')
	print( 'Status:\n')
	print( '	-h	 Help.')
	print( '	-a	 Annotation on output file. Default: False.'  )
	print( '		 Set this parameter if you want to annotate.')
	print( '	-f	 Using frequency information. Default: False.')
	print( '		 Set -v parameter if you want to set a specific frequency value.')
	print( '		 no specific value means a random number between 0 and 1')

	

def main(argv):
	inputfile = ''
	outputfile = ''
	length = '[4,20]'
	imprecision = '0.2'
	noise = '0.15'
	impre = 0.2
	noi = 0.15
	obo = 'hp.obo'
	table = 'phenotype_annotation.tab'
	case = '20'
	r = ''
	anno = False
	freq = False
	freq_value = False
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hafv:o:b:t:c:i:l:m:n:r:")
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == "-i":
			inputfile = arg
		elif opt == "-o":
			outputfile = arg
		elif opt == "-l":
			length = arg
		elif opt == "-m":
			imprecision = arg
			m = re.match("^0\.[0-9]+$",imprecision)
			if not m is None:
				impre = float(imprecision)
			elif imprecision == '0':
				impre = 0
			else:
				print ("-m: invalid input.") 
				sys.exit()
		elif opt == "-n":
			noise = arg
			m = re.match("^0\.[0-9]+$",noise)
			if not m is None:
				noi = float(noise)
			elif noise == "0":
				noi = 0
			else:
				print ("-n: invalid input.")
				sys.exit()
		elif opt == "-b":
			obo = arg
		elif opt == "-t":
			table = arg
		elif opt == "-c":
			case = arg
		elif opt == "-r":
			r = arg
		elif opt == "-v":
			freq_value = arg
		elif opt == "-a":
			anno = True
		elif opt == "-f":
			freq = True
		elif opt == "-h":
			usage()			   
			sys.exit(2)
	
	print ('Initializing...')
	if	outputfile == '':
		print('Initialize error. Please specify your output file by using -o !')
		sys.exit()	  
	
	if noi+impre >= 1:
		print('Initialize error. The percentage of (noise + imprecision) should less than 1!')
		sys.exit()
	
	if inputfile != '':
		if r != '':
			print ("Initialize error. You can not specify input file and generate random diseases at the same time!")
			sys.exit()
		else:
			disease_hpo,dis_hp_freq,hpall,dis_name,hp_name,o = dis_hp(table,obo)
			if not (re.match("^\d{6}$",inputfile)) is None:
				omimlists = ["OMIM:"+inputfile]
			elif not (re.match("^OMIM:\d{6}$",inputfile,re.IGNORECASE)) is None:
				omimlists = [inputfile.upper()]
			else:
				omimlists = omimlist(inputfile)
		#impre = float(imprecision)
		#noi = float(noise)
	elif  inputfile == '':
		if r == '':
			r = '5'
		disease_hpo,dis_hp_freq,hpall,dis_name,hp_name,o = dis_hp(table,obo)
		omimlists = RandomOmim(disease_hpo,int(r),length)
		#impre = float(imprecision)
		#noi = float(noise)
	
	f = open(outputfile,'w')
	if outputfile[-4:] == '.csv':
		sep = ","
	else:
		sep = "\t"
	if freq_value:
		f.write("#The parameters: -l<length>:" + length + "\t-m<imprecision>:" + imprecision + "\t-n<noise>:" + noise + "\t-c<case>:" + case + "\t-f<frequency>" + "\t-v<filter-value>:" + freq_value  +"\n")
	else:
		if freq:
			f.write("#The parameters: -l<length>:" + length + "\t-m<imprecision>:" + imprecision + "\t-n<noise>:" + noise + "\t-c<case>:" + case + "\t-f<frequency>" + "\n")
		else:
			f.write("#The parameters: -l<length>:" + length + "\t-m<imprecision>:" + imprecision + "\t-n<noise>:" + noise +  "\t-c<case>:" + case + "\n")
	for omimid in omimlists:
		f.write("\n\n" + omimid + sep + dis_name[omimid] + "\n\n" )
		for a in range(int(case)):
			patienthp = sim(omimid,obo,length,impre,noi,disease_hpo,dis_hp_freq,hpall,o,freq,float(freq_value))
			if not anno:
				s = sep.join(patienthp)
				f.write("patient" + str(a+1) + sep + s + "\n" )
			else:
				hhp = []
				for hpi in patienthp:
					hhp.append(hpi + '|' + hp_name[hpi])
				s = sep.join(hhp)
				f.write("patient" + str(a+1) + sep + s + "\n" )
	f.close()


class ShowProcess():
	i = 0 
	max_steps = 0 
	max_arrow = 50 

	def __init__(self, max_steps):
		self.max_steps = max_steps
		self.i = 0
	def show_process(self, i=None):
		if i is not None:
			self.i = i
		else:
			self.i += 1
		num_arrow = int(self.i * self.max_arrow / self.max_steps) 
		num_line = self.max_arrow - num_arrow 
		percent = self.i * 100.0 / self.max_steps
		process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
					  + '%.2f' % percent + '%' + '\r' 
		sys.stdout.write(process_bar) 
		sys.stdout.flush()

	def close(self, words='done'):
		print ('')
		print (words)
		self.i = 0

if __name__=='__main__':
	main(sys.argv[1:])
	max_steps = 100
	process_bar = ShowProcess(max_steps)
	for i in range(max_steps):
		process_bar.show_process()
		time.sleep(0.05)
	process_bar.close()			  

