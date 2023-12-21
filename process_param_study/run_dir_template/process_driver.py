"""Pre-process, execute and post-process a PROCESS run."""
import sys
import subprocess
from pathlib import Path

# from process.io.mfile import MFile
import json

# The first and second command line arguments to the script are the
# names of the Dakota parameters and results files
params = sys.argv[1]
results = sys.argv[2]

# Pre-processing
# Substitute parameters from Dakota into the template, writing ros.in
# Wants to be called via command line (requires own args)
input_template = "large_tokamak_IN.template"
input_file = "IN.DAT"  # result of processing template
# pyprepro lives in /opt/Dakota/bin, on PATH
subprocess.run(
    [
        "pyprepro",
        f"{input_template}",
        f"{input_file}",
        "--dakota-include",
        "params.in",
    ]
)

# Execution
# Run Process
subprocess.run(["process", "-i", "IN.DAT"])

# Post-processing
# Extract responses from MFILE
# mfile = MFile("MFILE.DAT")
# rmajor = mfile.data["rmajor"].get_scan(-1)

# Extract Process's responses from JSON
with open("responses.json", "r") as process_responses_file:
    responses = json.load(process_responses_file)

# Not sure if this is required (may prevent race conditions)
# mv results.tmp $results

# Write Dakota response file
with open(results, "w+") as dakota_responses_file:
    for key, value in responses.items():
        dakota_responses_file.write(f"{value}\t{key}\n")
