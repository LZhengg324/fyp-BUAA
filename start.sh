#!/bin/bash

host=${host:-"0.0.0.0"}
port=${port:-"8080"}
secret=${secret:-"trame123"}

/opt/paraview/bin/mpiexec -np 16 /opt/paraview/bin/pvserver &

sleep 2  # 等待 pvserver 启动

/opt/paraview/bin/pvpython /deploy/app.py \
  --host "${host}" \
  --port "${port}" \
  --authKey "${secret}" \
  --server
