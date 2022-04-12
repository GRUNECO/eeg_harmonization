import synapseclient 
import synapseutils
from synapseutils import walk
from pathlib import Path
import os
bids_root=r'Y:\datasets\CHBM'
bids_root = Path(bids_root)

syn = synapseclient.Synapse() 
syn.login('user','password') 

w = walk(syn, 'syn22324937')

for x in w:
    current_path = x[0][0]
    current_id = x[0][1]
    desired_path = os.path.join(bids_root,current_path)
    if 'eeg' in current_path:
        print(current_path)
        os.makedirs(desired_path,exist_ok=True)
        files = synapseutils.syncFromSynapse(syn, current_id,path=desired_path)
    else:
        continue
