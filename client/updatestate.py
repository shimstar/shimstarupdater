C_STATE_INIT_FIRSTUPDATE=-2
C_STATE_FIRSTUPDATE=-1
C_STATE_INIT=0
C_STATE_CONNECTED=1
C_STATE_TOUPDATE=2
C_STATE_WAITING_UPDATE=3
C_STATE_ENDUPDATE=4
C_STATE_NOTCONNECTED=5
C_STATE_FILEVERSION_RECEIVED=6
C_STATE_WAITING_CLICK=7

class updateState:
	instance=None
	def __init__(self):
		self.state=0
		updateState.instance=self
		
	@staticmethod
	def getInstance():
		if updateState.instance==None:
			updateState()
			
		return updateState.instance
		
	def getState(self):
		return self.state
		
	def setState(self,state):
		self.state=state
		
	
	