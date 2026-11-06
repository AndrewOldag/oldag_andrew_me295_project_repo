# Fresh md5 pass over batch-2 outputs on the lab server, against outputs.csv

- Windows: 1063; outputs.csv rows: 1143
- Window tracks: recorded 1060; match 1060, different 0, missing now 0
- Moved-copy reference tracks (`_wp_ref`): recorded 40; match 40, different 0, missing now 0
- Moved-copy moved tracks (`_wp_moved`): recorded 40; match 40, different 0, missing now 0
- Moved-copy delete rows in deletes.csv: 80; their checked md5 found in outputs.csv: 80 of 80
- Check JSONs (with a recorded md5: 1063): match 1063, different 0, missing now 0
- Deletes listed: 170 (90 staged roots, 80 moved copies); with an md5 check on the lab server before the delete: 170; other DELETED.log lines since the batch start, not deletes of this batch's staging: 10
