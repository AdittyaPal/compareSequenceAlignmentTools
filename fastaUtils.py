from Bio import SeqIO
from pathlib import Path
import numpy as np
import requests
from io import StringIO
import gzip
import time

def downloadDataBase(sourceURL, outputFile):
    """
        Download the complete database from the passed URL using direct FTP
    """
    
    print(f"Downloading the database from:")
    print(f"  {sourceURL}")
    print("  This may take several minutes...")
    
    try:
        # Stream download with progress indicator
        response = requests.get(sourceURL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        # Download and decompress on the fly
        with open(outputFile + '.gz', 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    progress = (downloaded / total_size) * 100
                    print(f"\rProgress: {progress:.1f}%", end='', flush=True)
        
        print(f"\nDownload complete. Decompressing...")
        
        # Decompress
        with gzip.open(outputFile + '.gz', 'rb') as f_in:
            with open(outputFile, 'wb') as f_out:
                f_out.write(f_in.read())
        
        print(f"  The database was downloaded successfully!")
        print(f"  File: {outputFile}")
        
        # Clean up compressed file
        import os
        os.remove(outputFile + '.gz')
        
        return outputFile
        
    except Exception as e:
        print(f"Error downloading the database: {e}")
        return None

def analyzeFastaFile(fastaPath):
    """
    Analyze a FASTA file and return comprehensive statistics
    
    Parameters:
        fastaPath: str path to FASTA file
    
    Returns:
        dict: stats dictionary
    """
    
    # read all sequences
    sequences = list(SeqIO.parse(fastaPath, "fasta"))
    
    if len(sequences) == 0:
        print(f"Warning: No sequences found in {fastaPath}")
        return None

    lengths = []
    # extract lengths
    for seq in sequences:
        lengths.append(len(seq.seq))
    
    # generate statistics
    stats = {
        "filename": Path(fastaPath).name,
        "num_sequences": len(sequences),
        "avg_length": np.mean(lengths),
        "std_length": np.std(lengths),
        "min_length": np.min(lengths),
        "max_length": np.max(lengths),
        "total_length": np.sum(lengths),
        "lengths": lengths,  # For detailed analysis
    }
    
    # adding quartiles
    stats["quartiles"] = {
        "25%": np.percentile(lengths, 25),
        "50% (median)": np.percentile(lengths, 50),
        "75%": np.percentile(lengths, 75)
    }
    
    return stats

def printFastaStats(stats):
    """
        Pretty print FASTA statistics
    """
    
    if stats is None:
        return
    
    print(f"\n{'='*60}")
    print(f"Analysis for: {stats['filename']}")
    print(f"{'='*60}")
    print(f"Number of sequences:   {stats['num_sequences']:,}")
    print(f"Total length (bp/aa):  {stats['total_length']:,}")
    print(f"\nLength statistics:")
    print(f"  Average length:      {stats['avg_length']:.2f}")
    print(f"  Standard deviation:  {stats['std_length']:.2f}")
    print(f"  Minimum length:      {stats['min_length']}")
    print(f"  Maximum length:      {stats['max_length']}")
    print(f"\nQuartiles:")
    for q, val in stats['quartiles'].items():
        print(f"  {q}: {val:.2f}")



