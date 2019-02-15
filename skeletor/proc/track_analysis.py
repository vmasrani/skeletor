""" Simple tools for analyzing track results after experimentation. """
import os
import track
import pandas as pd
from pathlib import Path

def df_from_proj(track_proj):
    """
    Gets a flattened dataframe with all trial results for the track.Project
    'proj'. See track.Project for how to get this from a logroot directory.
    """
    print("This function is depreciated in favor of the updated project object in track, which allows project.results() to return all results")
    results = []
    for _, trial in track_proj.ids.iterrows():
        res = track_proj.results([trial['trial_id']])
        for col in track_proj.ids.columns:
            # If the argument was a list (e.g. annealing schedule), have to
            # stringify it to assign it as a default val for all rows.
            if isinstance(trial[col], list):
                trial[col] = str(trial[col])
            res[col] = trial[col]
        results.append(res)
    _df = pd.concat(results)
    return _df


def proj(experimentname=None, logroot=None, s3=None,
         proj_dir=None):
    """
    Loads the track.Project object for this experiment directory.
    Gets the flattened dataframe.

    if proj_dir specified, load directly from there.
    otherwise, load from logroot/experimentname.

    loads from s3 if it can via track.
    """
    if logroot is None:
        logroot = Path.cwd() / 'logs'
    else:
        logroot = Path(logroot)

    print("Reading from:", logroot)

    if not proj_dir:
        if experimentname:
            assert logroot.exists(), "must supply logroot with experiment name"
        proj_dir = os.path.join(logroot, experimentname)
    track_proj = track.Project(proj_dir, s3)
    return track_proj

def get_project_names(logroot=None):
    if logroot is None:
        logroot = Path.cwd() / 'logs'
    else:
        logroot = Path(logroot)
    print("Reading from:", logroot)
    project_names = [x.name for x in logroot.glob("*") if x.is_dir()]
    return project_names
