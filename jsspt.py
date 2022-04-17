from os.path import exists, isfile
class exceptions(Exception):
	tab_error = {}
	tab_error["FileErr"] = "File error"
class SplitJS(exceptions):
	def CheckUP(word:str, verbose:bool) -> str:
		array = [bob for bob in word.split(";")]
		if "for" not in array[0]:
			als = word.split(";", maxsplit=1)
			locate = []
			counter = 0
			for items in als:
				if "}" == items:
					locate.append(items)
				counter += 1
			if locate != [] or len(locate) != 0:
				count = word.split(";", maxsplit=1)[counter-1]
				als[counter-1] = count + "\x0A"
			als = "\x0A".join(bob for bob in als)
			if "{" in als:
				als = "\x0A" + word + "\x0A"
		else:
			als = word+"\x0A"
		return als
	def __init__(self, file:str, verbose=True, carriage_return=False):
		self.file = file
		self.verbose = verbose
		self.carriage_return = carriage_return
		self.exclude = None
		self.fname = ""
		if exists(self.file) == False or isfile(self.file) == False:
			raise exceptions(exceptions.tab_error["FileErr"])
		read = "".join(bob for bob in open(self.file, "r", encoding="utf-8", errors="ignore"))
		if self.verbose == True:
			print("[~] Read from file %d-bytes!"%(len(read)))
		caser = {True:"\r\x0A", False:"\x0A"}[self.carriage_return]
		new_template = ""
		chrs = 0
		for items_Objects in read:
			try:
				if items_Objects in ["}", "{"] and read[chrs+1] != ";":
					items_Objects = items_Objects + caser + "\x20"*3
			except:
				items_Objects = items_Objects + caser
			if len(new_template) != 0 and new_template[len(new_template)-1] not in ["{", "}"]:
				items_Objects = items_Objects
			#if len(new_template) != 0 and items_Objects == ";" and read[chrs-1] != "}":
				#items_Objects = items_Objects + caser
			new_template += items_Objects
			chrs += 1
		lines = []
		for items in new_template.split(caser):
			lines.append(SplitJS.CheckUP(items.strip(), self.verbose))
		if self.verbose == True:
			print("[~] Total lines %d!"%(len(lines)))
		self.new_template = "".join(bob for bob in lines)
		print("[~] Total lines re-written %d!"%(len(self.new_template)))
		if self.verbose == True:
			nlines = 0
			for items in self.new_template.split(caser):
				nlines +=1
			print("[~] Total breaks %d!"%(nlines))
	@property
	def save_file(self):
		vr = open(self.fname, "w", encoding="utf-8", errors="ignore")
		if self.verbose == True:
			print("[~] File saved as '%s'"%(self.fname) + ". . .\x0A[~] Total bytes written %d!"%(len(self.new_template)))
		vr.write(self.new_template)
		return True
	@save_file.setter
	def name(self, newval):
		self.fname = newval
vr = SplitJS(file="d:/new_file.js")
vr.name = "new_file2.js"
vr.save_file