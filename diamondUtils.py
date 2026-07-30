import pandas as pd

from pathlib import Path

from seqUtils import SeqUtils

class DiamondUtils(SeqUtils):
    
    def __init__(self):
        super().__init__()
        self.executable = "diamond"

    def createDB(self, fastaPath, dbPath, dbFileName):
        """
            Wrapper to create databases for Diamond search
        """
        if Path(dbPath).is_dir() == False:
            Path(dbPath).mkdir(parents = True, exist_ok = True)
        if not Path(f"{dbPath}/{dbFileName}.dmnd").exists():
            print("Preparing database...")
            db_cmd = [self.executable, "makedb", "--in", fastaPath, "--db", f"{dbPath}/{dbFileName}"]
            self.runCmd(db_cmd)
        return f"{dbPath}/{dbFileName}"

    def runSearch(self, queryDB, targetDB, outputFile, threads = 2, maxSeqs = 1000, **kwargs):
        """
            Wrapper for Diamond search
        """

        mode = kwargs.get("mode", "sensitive")
        evalue = kwargs.get("evalue", 1e-3)
        
        blastp_cmd = [
            self.executable, "blastp", "--query", queryDB, "--db", str(targetDB), "--out", str(outputFile),
            "--outfmt", "6",  "--threads", str(threads), f"--{mode}", 
            "--max-target-seqs", str(maxSeqs), "--evalue", str(evalue)
        ]
            
        # execute
        self.runCmd(blastp_cmd)
        print(f"Search completed in the mode: {mode}")

        df = pd.read_csv(outputFile, sep = "\t")
        df.rename(columns = {"bitscore": "bits",
                            "qseqid": "query",
                            "sseqid": "target",
                            "length": "alnlen",
                            "sstart": "tstart",
                            "send": "tend",
                            "slen": "tlen"
                        }, inplace=True)
                    
        return df
