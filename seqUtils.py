from abc import ABC, abstractmethod

class SeqUtils(ABC):
    
    def __init__(self):
        self.RESULT_COLUMNS = ["query", "target", "pident", "alnlen", "mismatch",
                                "gapopen", "qstart", "qend", "tstart", "tend",
                                "evalue", "bits", "qlen", "tlen", "qcov", "tcov"]
    
    #methods must be overridden in derived classes
    @abstractmethod
    def createDB(self, fastaPath, dbPath, dbFileName):
        pass
    
    @abstractmethod
    def runSearch(self, queryDB, targetDB, outputFile):
        pass
