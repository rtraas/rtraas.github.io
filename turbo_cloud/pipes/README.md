# Pipes Overview
`fileio.py` --- The core module behind `autoplot.py` and `auto_find_event_pipeline.py`.  Given a one file name, `Find` will return the full, chronologically-ordered cadence it belongs to.  Includes other useful functions, as well as common recipes in the docstrings of the most useful functions.

`autoplot.py` --- Creates and saves 2d or 3d plots of `.csv` event files produced by `auto_find_event_pipeline.py`.  

![example from autoplot](https://github.com/rtraas/turboCLOUD/blob/master/turbo_cloud/pipes/07-23-2020.png)
![another example from autoplot](https://github.com/rtraas/turboCLOUD/blob/master/turbo_cloud/pipes/hits_rfi_plot.png)

`auto_find_event_pipeline.py` --- Looks for all `.dat` files in all folders, sorts them into their corresponding cadences, and finds events within those cadences.  Uses `fileio.py` functions in order to perform this operation.

`rfspec_allocation_bands.csv` --- A `.csv` file containing RFI frequency bands which contain the highest "hit density" near the Green Bank Observatory.

