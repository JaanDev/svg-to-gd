# !!! CODE BY camila314
# !!! https://github.com/camila314/GraphicsGD2/blob/master/ggd.py
# !!! Slightly edited by me

import datetime
import math
import os

import numpy as np
from gd.api import *
from svgpathtools import *

import db_tools

start_x, start_y = 90, 90


def mad(data, axis=None):
    return np.mean(abs(data - np.mean(data, axis)), axis)


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def midpoint(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def slope(x1, y1, x2, y2):
    try:
        m = math.atan2(y2 - y1, x2 - x1)
    except Exception:
        return 0
    else:
        return m


def generate(file_path, scale, density, block_size, error_correction):
    t_start = datetime.datetime.now()
    editor = Editor()

    scale /= density

    pths, _ = svg2paths(file_path)
    wsvg(pths, filename=os.path.join(os.path.expanduser('~'), '.tmp.svg'))
    paths, _ = svg2paths(os.path.join(os.path.expanduser('~'), '.tmp.svg'))
    pathsxy = []

    for path in paths:
        x_paths = [0.1]
        y_paths = [0.1]
        slopes = []
        is_new_paths = []

        for p in path:
            p.start /= scale
            p.end /= scale

            if isinstance(p, CubicBezier):
                p.control1 /= scale
                p.control2 /= scale
            elif isinstance(p, Arc):
                p.radius /= scale
            elif isinstance(p, QuadraticBezier):
                p.control /= scale
            elif not isinstance(p, Line):

                print(p)

            newp = True
            for i in range(int(round(p.length()))):
                comp = p.point(i / p.length())
                slopes.append(slope(x_paths[-1], y_paths[-1], comp.real, comp.imag))
                x_paths.append(comp.real)
                y_paths.append(comp.imag)
                is_new_paths.append(newp)
                newp = False

            comp = p.point(1)
            slopes.append(slope(x_paths[-1], y_paths[-1], comp.real, comp.imag))
            x_paths.append(comp.real)
            y_paths.append(comp.imag)
            is_new_paths.append(newp)

        plot = np.column_stack((x_paths[1:], y_paths[1:], slopes, is_new_paths))
        plot[0][2] = slope(plot[0][0], plot[1][0], plot[0][1], plot[1][1])

        if error_correction:
            blocksize_pos = block_size * (3.2 * density)
            plotted_point_index = 0

            while plotted_point_index + 1 < len(plot):
                plotted_point = plot[plotted_point_index]
                next_point = plot[plotted_point_index + 1]

                if not next_point[3] and distance(plotted_point, next_point) > blocksize_pos:
                    do_continue = True
                    x_midpoint, y_midpoint = midpoint(plotted_point, next_point)
                    slope_midpoint = (plotted_point[2] + next_point[2]) / 2
                    midp = [x_midpoint, y_midpoint, slope_midpoint, False]
                    plot = np.insert(plot, (plotted_point_index + 1) * 4, midp).reshape(-1, 4)
                    continue

                plotted_point_index += 1

        pathsxy.append(plot)

    svglengthy = max(np.concatenate([l[:, 1] for l in pathsxy]))
    total = 0

    for path in pathsxy:
        for point in path:
            total += 1
            editor.add_objects(Object(id=917, x=(point[0] * 2) / density + start_x,
                                      y=(((-1 * point[1]) + svglengthy) * 2) / density + start_y,
                                      rotation=math.degrees(point[2]), scale=block_size,
                                      dont_fade=1, dont_enter=1))

    print("Successfully converted")
    db_tools.add_level(editor)
