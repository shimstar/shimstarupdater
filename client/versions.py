import xml.dom.minidom
import os, sys


class updaterVersion:
	instance=None
	def __init__(self):
		self.versions={'titi':'toto'}
		self.versions.clear()
		self.higherVersion=0.0
		self.loadXml()
		updaterVersion.instance=self

		
	@staticmethod
	def getInstance():
		if updaterVersion.instance==None:
			updaterVersion()
		return updaterVersion.instance
	
	def loadXml(self):
		dom = xml.dom.minidom.parse(os.getcwd() + "\\versions.xml")
		#~ dom = xml.dom.minidom.parse("c:\\temp\\versions.xml")
		versions=dom.getElementsByTagName('version')
		for v in versions:
			version=float(v.getElementsByTagName('id')[0].firstChild.data)
			filesXml=v.getElementsByTagName('file')
			filesArray=[]
			for f in filesXml:
				#~ filesArray.append(f.getElementsByTagName('name')[0].firstChild.data)
				filesArray.append(f.firstChild.data)
			self.versions[version]=filesArray
			if version>self.higherVersion:
				self.higherVersion=version

	def getHigherVersion(self):
		return self.higherVersion

	def getFiles(self,version):
		filesToTransfert=[]
		for v in self.versions.iterkeys():
			
			if v>version:
				for f in self.versions[v]:
					if filesToTransfert.count(f)==0:
						filesToTransfert.append(f)
		return filesToTransfert			
		#~ print filesToTransfert
				
			
	
	