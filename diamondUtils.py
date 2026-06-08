import subprocess
import os
from pathlib import Path

def createDiamondDataBase(fastaPath, path, filename, threads = 2):
    """
        Wrapper to create databases for Diamond search
    """
    if Path(path).is_dir() == False:
        Path(path).mkdir(parents = True, exist_ok = True)
    if not Path(f"{path}/{filename}.dbtype").exists():
        print("Preparing database...")
        subprocess.run(["diamond", "makedb", "--in", fastaPath, "--db", f"{path}/{filename}", "--threads", str(threads)], check=True)
    return f"{path}/{filename}"

def runDiamondSearch(queryPath, targetPath, outputFile, sensitivity = "sensitive", threads = 2, maxSeqs = 1000, evalue = 1e-3):
    """
        Wrapper for Diamond search
    """
    
    blastp_cmd = [
        "diamond", "blastp", "--query", queryPath, "--db", str(targetPath), "--out", str(outputFile),
        "--outfmt", "6",  "--threads", str(threads), f"--{sensitivity}", 
        "--max-target-seqs", str(maxSeqs), "--evalue", str(evalue)
    ]
        
    # execute
    result = subprocess.run(blastp_cmd, capture_output=True, text=True, check=True)
    if "search" in " ".join(blastp_cmd):
        print(f"Search completed with sensitivity: {sensitivity}")
                
    return outputFile
