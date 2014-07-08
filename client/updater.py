from pandac.PandaModules import loadPrcFileData 
loadPrcFileData('', 'win-size %i %i' % (1200, 720))
loadPrcFileData("model-cache-dir",".\cache")
loadPrcFileData("model-cache-textures", "1" )
#~ loadPrcFileData("", "window-type none")
import xml.dom.minidom
import os, sys
from array import array
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from panda3d.rocket import *
from pandac.PandaModules import Filename
import time
from updatestate import *
from versions import *

#~ urlUpdater="http://shimrod.free.fr/shimstar/updater"
urlUpdater="http://localhost/updater"

class shimStarUpaterClient(DirectObject):
	instance=None
	def __init__(self):
		#~ self.network=network()
		shimStarUpaterClient.instance=self
		self.version=-1
		self.targetedVersion=-1
		self.iterFile=0
		self.user=""
		self.pwd=""
		self.ip=""
		self.updatingVersion=-1
		self.files=[]
		self.sssStream=None
		self.updatedFiles=[]
		self.http=None
		self.firtUpdate=True
		self.directory=os.getcwd()
		self.currentDir=os.getcwd()
		s="/" + self.currentDir[0:1].lower() + self.currentDir[2:]
		s=s.replace("\\","/")
		self.convCurrentDir=s
		self.loadVersion()
		self.loadVersionFile()
		LoadFontFace(self.convCurrentDir + "/assets/brassiere.ttf")
		r = RocketRegion.make('pandaRocket', base.win)
		r.setActive(1)
		self.context = r.getContext()
		ih = RocketInputHandler()
		base.mouseWatcher.attachNewNode(ih)
		r.setInputHandler(ih)
		
		self.back=self.context.LoadDocument('windows/background.rml')
		self.error=self.context.LoadDocument('windows/error.rml')
		self.back.Show()
		self.doc = self.context.LoadDocument('windows/update.rml')
		#~ self.accept("CLOSEF4",self.quit)
		#~ self.doc.Show()
		self.winPath= self.context.LoadDocument('windows/file.rml')
		self.convDirectory=""
		self.createTree(self.directory)
		self.readUpdateFile()
		if self.firtUpdate==True:
			updateState.getInstance().setState(C_STATE_INIT_FIRSTUPDATE)
		
		taskMgr.add(self.dispatch,"dispatch Main",-40)  
	
	@staticmethod
	def getInstance():
		if shimStarUpaterClient.instance==None:
			shimStarUpaterClient()
		return shimStarUpaterClient.instance
	
	def loadVersionFile(self):
		self.http = HTTPClient()
		self.channel = self.http.makeChannel(True)
		self.channel.beginGetDocument(DocumentSpec(urlUpdater+ '/files.xml'))
		ff=Filename(str(self.convCurrentDir) + "/versions.xml")
		#~ ff=Filename("/c/Users/ogilp/AppData/Local/Panda3D/start" + "/versions.xml")
		#~ ff=Filename(self.currentDir + "/versions.xml")
		self.channel.downloadToFile(ff)
		while self.channel.run():
				pass
	
		if not self.channel.isDownloadComplete():
			print "Error downloading file." + self.channel.getStatusString() + str(self.channel.getStatusCode())
			sys.exit()
		elif self.channel.isDownloadComplete():
			print "versions xml downloaded"
			
		self.files=updaterVersion.getInstance().getFiles(float(self.version))
		self.http=None
			
	def loadInstallFile(self):
		if self.http==None:
			self.http = HTTPClient()
			self.channel = self.http.makeChannel(True)
			self.channel.beginGetDocument(DocumentSpec(urlUpdater + '/install/install.xml'))
			ff=Filename(self.convCurrentDir + "/install.xml")
			self.channel.downloadToFile(ff)
		while self.channel.run():
				pass
	
		if not self.channel.isDownloadComplete():
			print "Error downloading file." + self.channel.getStatusString() + str(self.channel.getStatusCode())
			sys.exit()
		elif self.channel.isDownloadComplete():
			print "Install xml downloaded"
			
	def loadLocalRessources(self):
		dom = xml.dom.minidom.parse(os.getcwd() + "\\install.xml")
		files=dom.getElementsByTagName('file')
		filesInstall=[]
		for f in files:
			name=f.getElementsByTagName('name')[0].firstChild.data
			filesInstall.append(name)
			
		for f in filesInstall:
			self.http = HTTPClient()
			self.channel = self.http.makeChannel(True)
			self.channel.beginGetDocument(DocumentSpec(urlUpdater + '/install/' + f))
			ff=Filename(self.convCurrentDir + "/" + f)
			self.createTree(self.currentDir+"\\"+f.replace("/","\\"))
			self.channel.downloadToFile(ff)
			while self.channel.run():
					pass
		
			if not self.channel.isDownloadComplete():
				print "Error downloading file." + self.channel.getStatusString() + str(self.channel.getStatusCode())
				sys.exit()
			elif self.channel.isDownloadComplete():
				print f + " downloaded"
	
	def onChoosePath(self):
		self.createTree(self.winPath.GetElementById('path').value)
		print "onChoosePath: " + str(os.path.isdir(self.winPath.GetElementById('path').value))
		if os.path.isdir(self.winPath.GetElementById('path').value)==False:
			self.error.Show()
		else:
			self.directory=self.winPath.GetElementById('path').value
			self.winPath.Hide()
			self.doc.Show()
			updateState.getInstance().setState(C_STATE_INIT)
			
		
	def readUpdateFile(self):
		if os.path.isfile("./update.txt")!=False:
			fileHandle = open ( "./update.txt", 'r' ) 
			tabLines=fileHandle.readlines()
			for t in tabLines:
				tabLine=t.split("=")
				if tabLine[0]=="version":
					self.updatingVersion=float(tabLine[1])
				elif tabLine[0]=="file":
					self.updatedFiles.append(tabLine[1].replace("\n",""))
			fileHandle.close()
		
	def createTree(self,directory):
		if len(directory)>0:
			indexDot=directory.find(".")
			if indexDot==-1:
				indexSlash=directory.find("\\")
				if indexSlash!=-1:
					if os.path.isdir(directory)==False:
						tabDirectory=directory.split("\\")
						s=""
						for i in range(len(tabDirectory)-1):
							if s=="":
								s+=tabDirectory[i]
							else:
								s+="\\" + tabDirectory[i]
						f=self.createTree(s)
						if f==True:
							if os.path.isdir(directory)==False:
								os.mkdir(directory)
							return True
					else:
						return True
			else:
				tabDirectory=directory.split("\\")
				s=""
				for i in range(len(tabDirectory)-1):
					if s=="":
						s+=tabDirectory[i]
					else:
						s+="\\" + tabDirectory[i]
				f=self.createTree(s)
		return True
		
	def loadVersion(self):
		if os.path.isfile("config.xml")!=False:
			dom = xml.dom.minidom.parse("./config.xml")
			print dom.toxml()
			versions=dom.getElementsByTagName('version')
			for v in versions:
				self.version=float(v.firstChild.data)
			direc=dom.getElementsByTagName('directory')
			for d in direc:
				self.directory=d.firstChild.data
				
			usr=dom.getElementsByTagName('user')
			for u in usr:
				if u.firstChild!=None:
					self.user=str(u.firstChild.data)
				
			pwd=dom.getElementsByTagName('password')
			for p in pwd:
				if p.firstChild!=None:
					self.pwd=str(p.firstChild.data)
			
			ipp=dom.getElementsByTagName('ipd')
			for ip in ipp:
				if ip.firstChild!=None:
					self.ip=str(ip.firstChild.data)
			
			self.firtUpdate=False
			
		s="/" + self.directory[0:1].lower() + self.directory[2:]
		s=s.replace("\\","/")
		self.convDirectory=s
		
	def dispatch(self,task):
		if updateState.getInstance().getState()==C_STATE_INIT_FIRSTUPDATE:
			self.winPath.Show()
			updateState.getInstance().setState(C_STATE_FIRSTUPDATE)
		elif updateState.getInstance().getState()==C_STATE_INIT:
			#~ self.loadVersion()
			self.doc.Show()
			version=self.doc.GetElementById("actualversion")
			version.inner_rml=str(self.version)
			directory=self.doc.GetElementById("path")
			print directory.GetAttribute("disabled")
			#~ directory.SetDisabled(False)
			directory.inner_rml=str(self.directory)
			#~ directory.SetDisabled(True)
			status=self.doc.GetElementById("status")
			status.inner_rml="<span style='color:#00ff00;'>Online</span>"
			updateState.getInstance().setState(C_STATE_TOUPDATE)
		elif updateState.getInstance().getState()==C_STATE_NOTCONNECTED:
			status=self.doc.GetElementById("status")
			status.inner_rml="<span style='color:#ff0000;'>Offline</span>"
		elif updateState.getInstance().getState()==C_STATE_TOUPDATE:
			self.targetedVersion=updaterVersion.getInstance().getHigherVersion()
			if self.updatingVersion==-1:
				fileHandle = open ( "./update.txt", 'w' ) 
				fileHandle.write("version="+str(self.targetedVersion) + "\n")
				fileHandle.close()
			nbfichier=self.doc.GetElementById("nbfichier")
			nbfichier.inner_rml=str("0 / " + str(len(self.files)))
			version=self.doc.GetElementById("targetversion")
			version.inner_rml=str(self.targetedVersion)
			if self.targetedVersion==self.version:
				update=self.doc.GetElementById("update")
				update.inner_rml="<span style='color:#ff0000;'>Mettre a jour</span>"
				connect=self.doc.GetElementById("connect")
				connect.inner_rml="<span style='color:#00ff00;'>Jouer</span>"
				updateState.getInstance().setState(C_STATE_WAITING_PLAY)
				#~ updateState.getInstance().setState(C_STATE_CACHING)
			else:
				update=self.doc.GetElementById("update")
				update.inner_rml="<span style='color:#00ff00;'>Mettre a jour</span>"
				connect=self.doc.GetElementById("connect")
				connect.inner_rml="<span style='color:#ff0000;'>Jouer</span>"
				updateState.getInstance().setState(C_STATE_WAITING_CLICK)
			self.iterFile=0
		elif updateState.getInstance().getState()==C_STATE_WAITING_UPDATE:
			self.directory=self.doc.GetElementById("path").inner_rml
			if self.directory[len(self.directory)-1]!="\\":
				self.directory+="\\"
			s="/" + self.directory[0:1].lower() + self.directory[2:]
			s=s.replace("\\","/")
			self.convDirectory=s
			self.createTree(self.directory.replace("\\","\\\\")+"\\")
			if os.path.isdir(self.directory)==False:
				updateState.getInstance().setState(C_STATE_TOUPDATE)
				self.error.Show()
			else:
				#~ sssStream=None
				if self.iterFile>=len(self.files):
					updateState.getInstance().setState(C_STATE_ENDUPDATE)
				else:
					findInUpdatedFiles=False
					for f in self.updatedFiles:
						f=f.replace("\n","")
						if f==self.files[self.iterFile]:
							findInUpdatedFiles=True
							self.iterFile+=1
					if findInUpdatedFiles==False:
						if self.http==None:
							self.http = HTTPClient()
							self.channel = self.http.makeChannel(True)
							self.channel.setPersistentConnection(False)
							#~ print "downlaoding : " + urlUpdater + "/" + self.files[self.iterFile].replace("\\","/")
							self.channel.getDocument(DocumentSpec(urlUpdater + "/" + self.files[self.iterFile].replace("\\","/")))
							ff=Filename(self.convDirectory + "/" + self.files[self.iterFile].replace("\\","/"))
							self.createTree(self.directory+self.files[self.iterFile])
							self.channel.downloadToFile(ff)
						else:
							if self.channel.run():
								pass
							else:
								if not self.channel.isDownloadComplete():
									print "Error downloading file." + self.channel.getStatusString() + str(self.channel.getStatusCode())
									return task.done
								elif self.channel.isDownloadComplete():
									fileHandle = open ( "./update.txt", 'a+' ) 
									fileHandle.write("file="+str(self.files[self.iterFile])+ "\n")
									fileHandle.close()
									self.iterFile+=1
									nbfichier=self.doc.GetElementById("nbfichier")
									nbfichier.inner_rml=str( str(self.iterFile) + " / " + str(len(self.files)))
									self.http=None
							
		elif updateState.getInstance().getState()==C_STATE_ENDUPDATE:
			self.loadVersion()
			docXml = xml.dom.minidom.Document()
			confXml=docXml.createElement("config")
			versionXml=docXml.createElement("version")
			dirXml=docXml.createElement("directory")
			userXml=docXml.createElement("user")
			passwordXml=docXml.createElement("password")
			ipXml=docXml.createElement("ip")
			userXml.appendChild(docXml.createTextNode(str(self.user)))
			passwordXml.appendChild(docXml.createTextNode(str(self.pwd)))
			versionXml.appendChild(docXml.createTextNode(str(self.targetedVersion)))
			dirXml.appendChild(docXml.createTextNode(str(self.directory)))
			ipXml.appendChild(docXml.createTextNode(str(self.ip)))
			confXml.appendChild(passwordXml)
			confXml.appendChild(userXml)
			confXml.appendChild(versionXml)
			confXml.appendChild(ipXml)
			confXml.appendChild(dirXml)
			docXml.appendChild(confXml)
			fileHandle = open ( "./config.xml", 'w' ) 
			fileHandle.write(docXml.toxml())
			fileHandle.close()
			fileHandle = open ( "./update.txt", 'w' ) 
			fileHandle.close()
			update=self.doc.GetElementById("update")
			update.inner_rml="<span style='color:#ff0000;'>Mettre a jour</span>"
			#~ connect=self.doc.GetElementById("connect")
			#~ connect.inner_rml="<span style='color:#00ff00;'>Jouer</span>"
			updateState.getInstance().setState(C_STATE_CACHING)
		elif updateState.getInstance().getState()==C_STATE_CACHING:
			cache=self.doc.GetElementById("cache")
			cache.inner_rml="<span style='color:#00ff00;'>Mise en cache</span>"
			patth=self.winPath.GetElementById('path').value + "models"
			convPatth=self.winPath.GetElementById('path').value.replace("\\","/")
			convPatth="/" + convPatth[0:1] + convPatth[2:]
			convPatth+="models"
			self.caching(patth,convPatth)
			cache=self.doc.GetElementById("cache")
			cache.inner_rml="<span style='color:#0000ff;'>Mise en cache</span>"
			connect=self.doc.GetElementById("connect")
			connect.inner_rml="<span style='color:#00ff00;'>Jouer</span>"
			updateState.getInstance().setState(C_STATE_WAITING_PLAY)
			return task.done
		
		return task.cont
	
	def caching(self,dir,convPatth):
		for files in os.listdir(dir):
			if files.count(".egg")>0 or files.count(".bam")>0:
				#~ print convPatth + "/" + str(files)
				loader.loadModel(convPatth + "/" + str(files))
			elif os.path.isdir(dir + "\\"+ files):
				self.caching(dir+"\\" +files,convPatth + "/" + files)