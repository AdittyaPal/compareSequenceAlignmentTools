from abc import ABC, abstractmethod
import subprocess

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

    def runCmd(self, cmd):
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            raise
