#/bin/bash
fe_dir="$(dirname $(dirname $(realpath $0)) )/frontend"
cd $fe_dir
../../scripts/internal/rollback-vercel.sh