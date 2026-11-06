#!/bin/bash
#SBATCH --job-name=fb2_root
#SBATCH --partition=gpu
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:30:00
#SBATCH --gres=gpu:p100:1
# Batch 2, one cluster job per root (spec 2026-11-04; scripts/full_batch_2_driver.py installs and submits it). Every
# step of one root's windows on cluster nodes, from the whole root imgdir staged in $T/c019/data/<root>.imgdir:
# segmentation midline, ft2 net midline (GPU), tracking midline, 1000 px tracks, the w10-12 whole-pixel moved copy and
# its two tracks, then the checker for every window (check/<wid>.json). CPU steps 4 at a time. Each step skips an
# existing output; nothing is overwritten. The moved-copy frames are removed by the driver after the md5 check of the
# tracks on the storage host (Andrew, 2026-11-04).
# The driver passes, with --export: ROOT, T (cluster work folder), CODE (this repo at the synced commit), QB (tracker),
# ENV_ACTIVATE (tracker env), FT2_CODE and FT2_WEIGHTS (net midline); and --output/--error under $T/fb2/logs.
# Same steps as the job that ran batch 2; only the folder constants became these variables.
set -uo pipefail
D=$T/fb2/$ROOT
IMG=$T/c019/data/$ROOT.imgdir
source $ENV_ACTIVATE
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export D IMG CODE QB T
mkdir -p $D/seg $D/bm $D/midline $D/tracks $D/log $D/check $D/moved
echo "host=$(hostname) job=$SLURM_JOB_ID root=$ROOT start=$(date -Is)"
nvidia-smi --query-gpu=name --format=csv,noheader
seg() {   # wid from to
  f=$D/seg/$1_seg.npz; [ -f $f ] && return 0
  cd $CODE && PYTHONPATH=$QB:$CODE python scripts/remote/real_midline.py --imgdir $IMG --from-h $2 --to-h $3 --out $f > $D/log/$1_seg.log 2>&1
}
post() {  # wid from to
  m=$D/midline/$1_ft2_netmid.npz; t=$D/tracks/$1_ft2__st1__L1000.npz
  cd $CODE
  [ -f $m ] || PYTHONPATH=$QB:$CODE:$CODE/scripts/remote python scripts/remote/net_to_midline.py $QB $D/bm/$1_ft2_bm/*_htpmid.npz \
    $D/seg/$1_seg.npz $m > $D/log/$1_mid.log 2>&1 || return 1
  [ -f $t ] || PYTHONPATH=$QB:$CODE python scripts/remote/qb_track.py --imgdir $IMG --midline $m --out $t --movie real \
    --from-h $2 --to-h $3 --track-length 1000 --stride 1 > $D/log/$1_track.log 2>&1
}
moved_track() {  # wid from to which
  t=$D/tracks/$1_ft2_wp_$4__st1__L1000.npz; [ -f $t ] && return 0
  cd $CODE && PYTHONPATH=$QB:$CODE python scripts/remote/qb_track.py --imgdir $D/moved/$1_wp_$4.imgdir \
    --midline $D/moved/$1_ft2_wp_$4_midline.npz --out $t --movie real --from-h $2 --to-h $3 --track-length 1000 --stride 1 \
    > $D/log/$1_track_$4.log 2>&1
}
check() {  # wid from to
  o=$D/check/$1.json; [ -f $o ] && return 0
  cd $CODE
  r=$D/tracks/$1_ft2_wp_ref__st1__L1000.npz; m=$D/tracks/$1_ft2_wp_moved__st1__L1000.npz
  if [ -f $r ] && [ -f $m ]; then
    PYTHONPATH=$QB:$CODE python scripts/remote/check_window.py --window $1 --ref $r --moved $m --out $o > $D/log/$1_check.log 2>&1
  else
    PYTHONPATH=$QB:$CODE python scripts/remote/check_window.py --window $1 --track $D/tracks/$1_ft2__st1__L1000.npz --out $o \
      > $D/log/$1_check.log 2>&1
  fi
}
export -f seg post moved_track check
t0=$(date +%s)
xargs -P 4 -L 1 bash -c 'seg "$0" "$1" "$2" || echo "$0: seg failed"' < $D/windows.tsv
t1=$(date +%s); echo "seg: $(( t1 - t0 )) s"
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
while read -r wid a b; do
  [ -f $D/bm/$wid.done ] && continue
  [ -f $D/seg/${wid}_seg.npz ] || continue
  se=$(python -c "import sys,numpy as np; f=np.load(sys.argv[1])['frames']; print(int(f[0]), int(f[-1])+1)" $D/seg/${wid}_seg.npz)
  set -- $se
  PYTHONPATH=$FT2_CODE python $FT2_CODE/midline_ml/batch_midlines.py $IMG --out $D/bm/${wid}_ft2_bm --mode tile --lo 0.1 --hi 99.5 \
    --workers 3 --midline-weights $FT2_WEIGHTS --start $1 --end $2 < /dev/null > $D/log/${wid}_bm.log 2>&1 \
    && date -Is > $D/bm/$wid.done || echo "$wid: net midline failed"
done < $D/windows.tsv
t2=$(date +%s); echo "gpu: $(( t2 - t1 )) s"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
xargs -P 4 -L 1 bash -c 'post "$0" "$1" "$2" || echo "$0: post failed"' < $D/windows.tsv
t3=$(date +%s); echo "track: $(( t3 - t2 )) s"
mv_line=$(grep "^${ROOT}__w10-12 " $D/windows.tsv || true)
if [ -n "$mv_line" ] && [ -f $D/midline/${ROOT}__w10-12_ft2_netmid.npz ]; then
  w=${ROOT}__w10-12
  if [ ! -f $D/moved/${w}_wp_moved.imgdir.ok ]; then
    cd $CODE && PYTHONPATH=$QB:$CODE python scripts/remote/real_moved.py --imgdir $IMG --midline $D/midline/${w}_ft2_netmid.npz \
      --from-h 10 --to-h 12 --out-imgdir $D/moved/${w}_wp_moved.imgdir --out-midline $D/moved/${w}_ft2_wp_moved_midline.npz \
      --mode whole_pixel --out-ref-imgdir $D/moved/${w}_wp_ref.imgdir --out-ref-midline $D/moved/${w}_ft2_wp_ref_midline.npz \
      > $D/log/${w}_moved.log 2>&1 || echo "$w: moved copy failed"
  fi
  printf "%s 10 12 ref\n%s 10 12 moved\n" $w $w | xargs -P 2 -L 1 bash -c 'moved_track "$0" "$1" "$2" "$3" || echo "$0 $3: moved track failed"'
fi
t4=$(date +%s); echo "moved: $(( t4 - t3 )) s"
xargs -P 4 -L 1 bash -c 'check "$0" "$1" "$2" || echo "$0: check failed"' < $D/windows.tsv
t5=$(date +%s); echo "check: $(( t5 - t4 )) s"
n=$(ls $D/tracks/*__st1__L1000.npz 2>/dev/null | grep -vc "_wp_"); w=$(wc -l < $D/windows.tsv); c=$(ls $D/check/*.json 2>/dev/null | wc -l)
echo "end=$(date -Is) tracks $n of $w, checks $c"
[ "$n" = "$w" ] && date -Is > $D/root.done
exit 0
