"""Collection of simple, handy functions."""

import os
import numpy as np


def truncate_range(data, percMin=0.25, percMax=99.75, discard_zeros=True):
    """Truncate too low and too high values.

    Parameters
    ----------
    data : np.ndarray
        Image to be truncated.
    percMin : float
        Percentile minimum.
    percMax : float
        Percentile maximum.
    discard_zeros : bool
        Discard voxels with value 0 from truncation.

    Returns
    -------
    data : np.ndarray

    """
    if discard_zeros:
        msk = ~np.isclose(data, 0)
        pMin, pMax = np.nanpercentile(data[msk], [percMin, percMax])
    else:
        pMin, pMax = np.nanpercentile(data, [percMin, percMax])
    temp = data[~np.isnan(data)]
    temp[temp < pMin], temp[temp > pMax] = pMin, pMax  # truncate min and max
    data[~np.isnan(data)] = temp
    if discard_zeros:
        data[~msk] = 0  # put back masked out voxels
    return data


def scale_range(data, scale_factor=255, discard_zeros=True):
    """Scale values as a preprocessing step.

    Parameters
    ----------
    data : np.ndarray
        Image to be scaled.
    scale_factor : float
        Lower scaleFactors provides faster interface due to loweing the
        resolution of 2D histogram ( 500 seems fast enough).
    discard_zeros : bool
        Discard voxels with value 0 from truncation.

    Returns
    -------
    data: np.ndarray
        Scaled image.

    """
    if discard_zeros:
        msk = ~np.isclose(data, 0)
    else:
        msk = np.ones(data.shape, dtype=bool)
    data[msk] = data[msk] - np.nanmin(data[msk])
    data[msk] = scale_factor / np.nanmax(data[msk]) * data[msk]
    if discard_zeros:
        data[~msk] = 0  # put back masked out voxels
    return data


def parse_filepath(filepath):
    """Load images with different extensions.

    Parameters
    ----------
    filepath: string
        Input name that will be parsed into path, basename and extension

    Returns
    -------
    data: ndim numpy array
        Image data.
    dirname: string
        File directory.
    basename: string
        File name without directory and extension.
    ext: string
        File extension.

    """
    path = os.path.normpath(filepath)
    dirname = os.path.dirname(path)
    filename = path.split(os.sep)[-1]
    basename, ext = filename.split(os.extsep, 1)
    return dirname, basename, ext


def prepare_scale_suffix(scales):
    """Prepare scale identifier suffix.

    Parameters
    ----------
    scales: list

    Returns
    -------
    id: string

    """
    id = ''
    for s in scales:
        id += '_{}'.format(s)
    return id
