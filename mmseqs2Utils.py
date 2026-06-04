import subprocess
import tempfile
import os
from pathlib import Path

def createMmseqsDataBase(fastaPath, path, filename):
    """
        Wrapper to create databases for MMseqs2 search
    """
    if Path(path).is_dir() == False:
        Path(path).mkdir(parents = True, exist_ok = True)
    if not Path(f"{path}/{filename}.dbtype").exists():
        print("Preparing database...")
        subprocess.run(["mmseqs", "createdb", fastaPath, f"{path}/{filename}"], check=True)
    return f"{path}/{filename}"

def runMmseqsSearch(queryPath, targetPath, outputFile, sensitivity = 7, threads = 2, maxSeqs = 1000):
    """
        Wrapper for MMseqs2 search
    """
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        resultDB = tmpdir/"resultDB"
        
        cmds = [
                    ["mmseqs", "search", str(queryPath), str(targetPath), str(resultDB), str(tmpdir/"tmp"),
                        "-s", str(sensitivity), "--max-seqs", str(maxSeqs), "--threads", str(threads)],
                    ["mmseqs", "convertalis", str(queryPath), str(targetPath), str(resultDB), str(outputFile),
                         "--format-output", "query,target,pident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,qlen,tlen,qcov,tcov"]
            ]
        # Execute
        for cmd in cmds:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if "search" in cmd:
                print(f"Search completed with sensitivity = {sensitivity}")
        
    return outputFile
