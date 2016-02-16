import arcpy
import pythonaddins


class ApplySymbology(object):
    """Implementation for LiDAR1_Plugin_addin.applysymbology (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("C:/LiDAR1_Plugin_1.4/LiDAR1_Toolbox.tbx", "ApplySymbology")

class ButtonGenerateIndices(object):
    """Implementation for LiDAR1_Plugin_addin.buttonIndices (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("C:/LiDAR1_Plugin_1.4/LiDAR1_Toolbox.tbx", "GenerateIndicesBatch")

class LoadIndices(object):
    """Implementation for LiDAR1_Plugin_addin.loadindices (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
         pythonaddins.GPToolDialog("C:/LiDAR1_Plugin_1.4/LiDAR1_Toolbox.tbx", "LoadIndices")

class CalculateRMSE(object):
    """Implementation for LiDAR1_Plugin_addin.buttonRMSE (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("C:/LiDAR1_Plugin_1.4/LiDAR1_Toolbox.tbx", "CalculateRMSE")

class CalibrateDTM(object):
    """Implementation for LiDAR1_Plugin_addin.buttonCalibrateDTM (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("C:/LiDAR1_Plugin_1.4/LiDAR1_Toolbox.tbx", "CalibrateDTM")

class CenterLines(object):
    """Implementation for LiDAR1_Plugin_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("C:/LiDAR1_Plugin_1.4/LiDAR1_Toolbox.tbx", "GenerateMidline")


class SplitShpmask(object):
    """Implementation for LiDAR1_Plugin_addin.splitshpmask (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("C:/LiDAR1_Plugin_1.4/LiDAR1_Toolbox.tbx", "SplitShpmask")