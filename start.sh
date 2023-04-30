#!/bin/bash

tmux new-session -d -s sky
tmux send-keys -t sky "python himmelcam.py" Enter
# Attach to session named "sky"
tmux attach -t sky


