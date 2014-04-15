import xml.dom.minidom
import os, sys


def appendFiles(directory,root,docXml,filesXml):
	for files in os.listdir(directory):
		if os.path.isfile(directory+ "\\" + files):
			fileXml=docXml.createElement("file")
			if root!="":
				fileXml.appendChild(docXml.createTextNode(root + "\\" + files))
			else:
				fileXml.appendChild(docXml.createTextNode(files))
			filesXml.appendChild(fileXml)
		else:
			if root!="":
				appendFiles(directory+"\\"+files,root+"\\"+files,docXml,filesXml)
			else:
				appendFiles(directory+"\\"+files,files,docXml,filesXml)
			
			
docXml = xml.dom.minidom.Document()

versionsXml=docXml.createElement("versions")
versionXml=docXml.createElement("version")
idXml=docXml.createElement("id")
idXml.appendChild(docXml.createTextNode("0.3"))
filesXml=docXml.createElement("files")

appendFiles("C:\\pascal\\shimstar\\v3\\shimstarupdater\\ressources","",docXml,filesXml)

versionXml.appendChild(idXml)
versionXml.appendChild(filesXml)
versionsXml.appendChild(versionXml)
docXml.appendChild(versionsXml)
#~ dirXml=docXml.createElement("directory")
#~ userXml=docXml.createElement("user")
#~ passwordXml=docXml.createElement("password")
#~ versionXml.appendChild(docXml.createTextNode(str(self.version)))
#~ dirXml.appendChild(docXml.createTextNode(str(self.ressourceDirectory)))
#~ userXml.appendChild(docXml.createTextNode(str(self.user)))
#~ passwordXml.appendChild(docXml.createTextNode(str(self.pwd)))
#~ confXml.appendChild(passwordXml)
#~ confXml.appendChild(userXml)
#~ confXml.appendChild(versionXml)
#~ confXml.appendChild(dirXml)
#~ docXml.appendChild(confXml)
fileHandle = open (  "files.xml", 'w' ) 
fileHandle.write(docXml.toxml())
fileHandle.close()
