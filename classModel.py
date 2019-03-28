import cv2

class clsModel:
    def __init__(self):
        self._model = None
    
    def loadModel(self, pathModel):
        model = cv2.face.LBPHFaceRecognizer_create()
        model.read(pathModel)        
    
    def set_Model(self, value):
        self.model=value
    
    def get_Model(self):
        return(self.model)
    
    def del_Model(self):
        del self