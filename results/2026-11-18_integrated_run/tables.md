# c027 integrated run: tables

Windows: 1189. Records: 1189. Real windows have no ground truth; 'accepted after repair' means the checker passes after a kept remedy.

### Outcome per method

| method | accepted | accepted after repair | declined by rule | declined by check | declined by agent | declined by tree | step_limit | paused | total |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: |
| integrated | 1034 | 2 | 58 | 0 | 85 | 0 | 6 | 4 | 1189 |
| remedy tree (+ rule and pass as integrated) | 1034 | 12 | 58 | 0 | 0 | 78 | 0 | 7 | 1189 |
| fixed script | 1034 | 0 | 58 | 93 | 0 | 0 | 0 | 4 | 1189 |

### Integrated run per condition

| condition | accepted | accepted after repair | declined by rule | declined by agent | step_limit | paused | total |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| - | 0 | 0 | 0 | 0 | 0 | 2 | 2 |
| control | 368 | 0 | 19 | 28 | 2 | 0 | 417 |
| control then control | 42 | 0 | 5 | 6 | 0 | 0 | 53 |
| mannitol | 291 | 1 | 23 | 27 | 2 | 1 | 345 |
| mannitol then control | 272 | 1 | 7 | 17 | 2 | 1 | 300 |
| mannitol then mannitol | 61 | 0 | 4 | 7 | 0 | 0 | 72 |

### Integrated run per experiment (date)

| experiment | accepted | accepted after repair | declined by rule | declined by agent | step_limit | paused | total |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| 0708 | 184 | 0 | 6 | 22 | 3 | 1 | 216 |
| 0711 | 173 | 0 | 17 | 11 | 0 | 0 | 201 |
| 0714 | 206 | 1 | 16 | 13 | 1 | 0 | 237 |
| 0721 | 222 | 1 | 6 | 21 | 1 | 1 | 252 |
| 0727 | 249 | 0 | 13 | 18 | 1 | 2 | 283 |

### Diagnostician vs remedy tree

- Windows with both final: 90. Same outcome: 74. Same final kept settings: 69

| window | diagnostician | its remedies (closure before -> after, kept) | tree | its remedies |
| :-- | :-- | :-- | :-- | :-- |
| 0708_c11__w0-2 | decline | none | decline | st1_regv2p1125b223 56.20 -> 56.20 rolled back; st1_r22 56.20 -> 47.85 rolled back; st1_r30 56.20 -> 40.71; st1_r30_mslight4 40.71 -> 35.28 rolled back |
| 0708_c4__w0-2 | step_limit | st1_r22 103.55 -> 103.07 rolled back; st1_mask 103.55 -> nan rolled back; st1_mslight4 103.55 -> 57.69 | decline | st1_regv2p470b410 103.55 -> 335.59 rolled back; st1_r16 103.55 -> 102.35 rolled back; st1_r22 103.55 -> 103.07 rolled back; st1_mslight4 103.55 -> 57.69 |
| 0708_m11__w0-2 | step_limit | st1_mslight4 49.13 -> 53.63 rolled back; st1_crop 49.13 -> 49.13 rolled back | decline | st1_regv2p920b195 49.13 -> 49.13 rolled back; st1_r15 49.13 -> 50.45 rolled back; st1_r20 49.13 -> 50.53 rolled back; st1_mslight4 49.13 -> 53.63 rolled back |
| 0708_m8__w0-2 | step_limit | st1_mslight4 19.57 -> 22.10 rolled back; st1_crop 19.57 -> 19.57 rolled back | decline | st1_regv2p1030b78 19.57 -> 19.57 rolled back; st1_r20 19.57 -> 21.75 rolled back; st1_r26 19.57 -> 22.36 rolled back; st1_mslight4 19.57 -> 22.10 rolled back |
| 0708_m8__w6-8 | decline | st1_mslight4 39.18 -> 39.83 rolled back | decline | st1_regv2p1080b155 39.18 -> 151.48 rolled back; st1_r21 39.18 -> 36.82 rolled back; st1_r28 39.18 -> 29.22; st1_r28_mslight4 29.22 -> 28.48 rolled back |
| 0708_m8__w18-20 | decline | st1_regv2p1010b170 42.96 -> 48.30 rolled back | decline | st1_regv2p1010b170 42.96 -> 48.30 rolled back; st1_r20 42.96 -> 30.24; st1_r26 30.24 -> 24.52 rolled back; st1_r20_mslight4 30.24 -> 29.75 rolled back |
| 0708_m9__w0-2 | decline | st1_regv2p1055b152 38.34 -> 137.40 rolled back | decline | st1_regv2p1055b152 38.34 -> 137.40 rolled back; st1_r18 38.34 -> 32.77 rolled back; st1_r24 38.34 -> 25.00; st1_r24_mslight4 25.00 -> 25.97 rolled back |
| 0711_m3__w14-16 | decline | none | accept | st1_regv2p1030b100 25.18 -> 49.10 rolled back; st1_r20 25.18 -> 24.40 rolled back; st1_r26 25.18 -> 23.75 rolled back; st1_mslight4 25.18 -> 13.75 |
| 0714_c4__w0-2 | step_limit | st1_regv2p1285b238 59.96 -> 60.02 rolled back; st1_crop 59.96 -> 59.96 rolled back; st1_mslight4 59.96 -> 66.84 rolled back | decline | st1_regv2p1285b238 59.96 -> 60.02 rolled back; st1_r8 59.96 -> 57.90 rolled back; st1_r10 59.96 -> 56.49 rolled back; st1_mslight4 59.96 -> 66.84 rolled back |
| 0714_c5__w0-2 | decline | st1_regv2p970b344 86.90 -> 108.95 rolled back | decline | st1_regv2p970b344 86.90 -> 108.95 rolled back; st1_r21 86.90 -> 85.76 rolled back; st1_r28 86.90 -> 83.57 rolled back; st1_mslight4 86.90 -> 31.18 |
| 0714_c5__w6-8 | decline | none | decline | st1_regv2p1020b200 50.37 -> 50.37 rolled back; st1_r24 50.37 -> 50.05 rolled back; st1_r32 50.37 -> 49.46 rolled back; st1_mslight4 50.37 -> 22.00 |
| 0714_c6__w0-2 | decline | none | accept | st1_regv2p1190b82 20.63 -> 20.63 rolled back; st1_r21 20.63 -> 6.35 |
| 0714_c9__w2-4 | decline | none | decline | st1_regv2p1095b220 55.45 -> 55.45 rolled back; st1_r24 55.45 -> 50.18 rolled back; st1_r32 55.45 -> 35.70; st1_r32_mslight4 35.70 -> 25.96 |
| 0714_c9__w12-14 | decline | none | accept | st1_regv2p1090b190 47.48 -> 42.94 rolled back; st1_r24 47.48 -> 37.66 rolled back; st1_r32 47.48 -> 16.60 |
| 0714_m7__w22-23.89 | decline | st1_regv2p1020b82 21.67 -> 20.75 rolled back | accept | st1_regv2p1020b82 21.67 -> 20.75 rolled back; st1_r21 21.67 -> 21.66 rolled back; st1_r28 21.67 -> 21.37 rolled back; st1_mslight4 21.67 -> 13.67 |
| 0721_c2__w8-10 | decline | st1_regv2p1130b147 37.03 -> 37.03 rolled back | decline | st1_regv2p1130b147 37.03 -> 37.03 rolled back; st1_r24 37.03 -> 32.70 rolled back; st1_r32 37.03 -> 27.63; st1_r32_mslight4 27.63 -> 22.56 rolled back |
| 0721_c2__w22-24 | decline | st1_regv2p1320b82 20.67 -> 20.68 rolled back | accept | st1_regv2p1320b82 20.67 -> 20.68 rolled back; st1_r8 20.67 -> 10.47 |
| 0721_m3__w6-8 | decline | none | accept | st1_regv2p1050b167 42.18 -> 61.10 rolled back; st1_r26 42.18 -> 38.89 rolled back; st1_r34 42.18 -> 37.37 rolled back; st1_mslight4 42.18 -> 17.49 |
| 0721_m3__w16-18 | decline | none | decline | st1_regv2p1015b159 40.01 -> 40.86 rolled back; st1_r24 40.01 -> 34.39 rolled back; st1_r32 40.01 -> 32.21 rolled back; st1_mslight4 40.01 -> 19.48 |
| 0721_m3__w20-22 | decline | st1_regv2p1085b160 40.66 -> 7.39 rolled back | decline | st1_regv2p1085b160 40.66 -> 7.39 rolled back; st1_r24 40.66 -> 40.53 rolled back; st1_r32 40.66 -> 39.89 rolled back; st1_mslight4 40.66 -> 19.24 |
| 0721_m4__w0-2 | step_limit | st1_crop 179.67 -> 179.67 rolled back; st1_mslight4 179.67 -> 180.68 rolled back | decline | st1_regv2p730b714 179.67 -> 179.67 rolled back; st1_r21 179.67 -> 178.92 rolled back; st1_r28 179.67 -> 178.54 rolled back; st1_mslight4 179.67 -> 180.68 rolled back |
| 0727_mc11__w18-20 | decline | none | accept | st1_regv2p1065b142 52.02 -> 49.61 rolled back; st1_r24 52.02 -> 39.82 rolled back; st1_r32 52.02 -> 36.36; st1_r32_mslight4 36.36 -> 14.46 |
| 0727_mc14__w20-22 | decline | st1_regv2p1065b187 48.40 -> 47.25 rolled back | decline | st1_regv2p1065b187 48.40 -> 47.25 rolled back; st1_r24 48.40 -> 43.82 rolled back; st1_r32 48.40 -> 43.21 rolled back; st1_mslight4 48.40 -> 22.46 |
| 0727_mc4__w0-2 | step_limit | st1_mslight4 34.56 -> 33.95 rolled back; st1_crop 34.56 -> 34.56 rolled back | decline | st1_regv2p1005b137 34.56 -> nan rolled back; st1_r21 34.56 -> 34.09 rolled back; st1_r28 34.56 -> 33.48 rolled back; st1_mslight4 34.56 -> 33.95 rolled back |
| 0727_mm2__w12-14 | decline | none | accept | st1_regv2p1060b80 20.09 -> 26.19 rolled back; st1_r20 20.09 -> 21.27 rolled back; st1_r26 20.09 -> 21.21 rolled back; st1_mslight4 20.09 -> 17.32 |
| 0727_mm2__w14-16 | decline | st1_regv2p1055b169 42.73 -> 48.10 rolled back | accept | st1_regv2p1055b169 42.73 -> 48.10 rolled back; st1_r16 42.73 -> 41.44 rolled back; st1_r22 42.73 -> 37.18 rolled back; st1_mslight4 42.73 -> 13.27 |
| 0727_mm7__w20-22 | decline | st1_regv2p1030b76 19.97 -> 19.16 rolled back | accept | st1_regv2p1030b76 19.97 -> 19.16 rolled back; st1_r24 19.97 -> 16.85 |

### Remedies

| method | tried | kept | rolled back |
| :-- | --: | --: | --: |
| diagnostician | 73 | 4 | 69 |
| tree | 352 | 27 | 325 |

### LLM use

- Diagnostician (recorded windows): 358 calls, 1587279 input tokens, 232626 output tokens, 0.68 h of call time
- Auditor: 101 runs, 447 calls; 0 roots with no accepted window (no call)
- All traces under the run folder, paused and set-aside included: 1015 calls (cap 900, raised to 1,300 at 782 calls)
- Auditor flags: 245

### Cluster

- Retrack tasks recorded: 616 (done 12, failed 28, fetched 576); arrays 47

