"""Pre-process, execute and post-process a unc_rosen run."""
import sys
import subprocess
from pathlib import Path
import json
import unc_rosen
import numpy as np

# The first and second command line arguments to the script are the
# names of the Dakota parameters and responses files
params_filename = sys.argv[1]
responses_filename = sys.argv[2]

# Pre-processing
# Substitute parameters from Dakota's params_filename.in into the input file template,
# writing unc_rosen.json
# pyprepro pre-processing tool lives in /opt/Dakota/bin, on PATH
# Wants to be called via command line (requires own args)
input_template = "unc_rosen.template"
input_file = "unc_rosen_params.json"  # result of processing template
subprocess.run(
    [
        "pyprepro",
        f"{input_template}",
        f"{input_file}",
        "--dakota-include",
        f"{params_filename}",
    ]
)

# Extract input values for running unc_rosen
with open(input_file, "r") as unc_rosen_input_file:
    unc_rosen_inputs = json.load(unc_rosen_input_file)

x = np.array([unc_rosen_inputs["x"], unc_rosen_inputs["y"]])
e = np.array([unc_rosen_inputs["e1"], unc_rosen_inputs["e2"]])

# Run unc_rosen
obj_func, constrs = unc_rosen.main(x, e)

# Post-processing
# TODO Perhaps .tolist()?
# responses = {"obj_func": obj_func, "constrs": constrs}
# responses = {"obj_func": obj_func}
# for i, val in enumerate(constrs):
#     responses[f"con{i}"] = val

# Just write out con1 value for now
cons = np.sum(constrs)
responses = {"cons": cons}

# Write Dakota response file
# Dakota interprets "var" as a function value, "[var]" as a gradient
with open(responses_filename, "w+") as responses_file:
    for key, value in responses.items():
        responses_file.write(f"{value} {key}\n")
        # responses_file.write(f"{value}\n")
