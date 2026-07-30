import tempfile
import pandas as pd

from pathlib import Path

from seqUtils import SeqUtils

class MMseqsUtils(SeqUtils):
    
    def __init__(self):
        super().__init__()
        self.executable = "mmseqs"

    def createDB(self, fastaPath, dbPath, dbFileName):
        """
            Wrapper to create databases for MMseqs2 search
        """
        if Path(dbPath).is_dir() == False:
            Path(dbPath).mkdir(parents = True, exist_ok = True)
        if not Path(f"{dbPath}/{dbFileName}.dbtype").exists():
            print("Preparing database...")
            db_cmd = [self.executable, "createdb", fastaPath, f"{dbPath}/{dbFileName}"]
            self.runCmd(db_cmd)
        return f"{dbPath}/{dbFileName}"

    def runSearch(self, queryDB, targetDB, outputFile, threads = 2, maxSeqs = 1000, **kwargs):
        """
            Wrapper for MMseqs2 search
        """
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            resultDB = tmpdir/"resultDB"
            sensitivity = kwargs.get("sensitivity", 7.5)
            
            searchCmd = [self.executable, "search", str(queryDB), str(targetDB), str(resultDB), str(tmpdir/"tmp"),
                            "-s", str(sensitivity), "--max-seqs", str(maxSeqs), "--threads", str(threads)]
            convertCmd = [self.executable, "convertalis", str(queryDB), str(targetDB), str(resultDB), str(outputFile),
                             "--format-output", ','.join(self.RESULT_COLUMNS) ]
            
            # Execute
            self.runCmd(searchCmd)            
            print(f"Search completed with sensitivity = {sensitivity}")
            self.runCmd(convertCmd)
            
            df = pd.read_csv(outputFile, sep = "\t", names = self.RESULT_COLUMNS)
        return df
