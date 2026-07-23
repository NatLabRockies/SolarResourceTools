"""Boundary-related helpers extracted from GUI scripts."""

import qcfit_core.state_models as state_models


def find_range(previous, lower, upper):
    """Merge a previous stored range with a new lower/upper pair."""
    if "-" in previous:
        dash_count = previous.count("-")
        if dash_count == 1:
            case = 1
        else:
            case = 2
    else:
        case = 3

    if case == 1:
        parts = previous.split("-")
        # Update only when new bounds expand the previous range.
        if lower < int(parts[0]):
            parts[0] = lower
        if upper > int(parts[1]):
            parts[1] = upper
        return str(parts[0]) + "-" + str(parts[1])

    if case == 2:
        if lower == upper:
            return str(lower)
        return str(lower) + "-" + str(upper)

    if lower < int(previous):
        return str(lower)
    return previous


def set_out_flag(df, state, x_axis="KT", y_axis="KN", am="low", side="left"):
    """Flag points that are outside currently configured boundary curves."""
    am_state = state_models.get_airmass(state, am)
    if len(df) > 0 and am_state.knMax != "NA":
        for yp in range(int(am_state.knMax)):
            if side == "left":
                point_on_curve = am_state.xLB[yp]
                x_points = [point for point in list(df[df[y_axis] == yp][x_axis]) if point < point_on_curve]
                if len(x_points) > 0:
                    for point in x_points:
                        df.loc[(df[y_axis] == yp) & (df[x_axis] == point), "outFlag"] = 1
            elif side == "right":
                point_on_curve = am_state.xRB[yp]
                x_points = [point for point in list(df[df[y_axis] == yp][x_axis]) if point > point_on_curve]
                if len(x_points) > 0:
                    for point in x_points:
                        df.loc[(df[y_axis] == yp) & (df[x_axis] == point), "outFlag"] = 1

        df.loc[(df[y_axis] > am_state.knMax), "outFlag"] = 1


def prepare_plot_boundaries(state, am):
    """Build and clamp boundary curves for plotting and persist in state."""
    am_state = state_models.get_airmass(state, am)

    x_lb = list(am_state.lBound)
    fill_count = 101 - len(x_lb)
    if fill_count > 0:
        fill_list = [x_lb[-1]] * fill_count
        x_lb = x_lb + fill_list

    y_lb = list(range(0, int(am_state.knMax) + 1))
    fill_count = 101 - len(y_lb)
    fill_list = [y_lb[-1]] * fill_count
    y_lb = y_lb + fill_list

    x_rb = list(am_state.rBound)
    fill_count = 101 - len(x_rb)
    if fill_count > 0:
        fill_list = [x_rb[-1]] * fill_count
        x_rb = x_rb + fill_list

    y_rb = y_lb

    x_limit = max(x_rb)
    x_lb = [x if (x < x_limit) else x_limit for x in x_lb]

    am_state.xLB = x_lb
    am_state.yLB = y_lb
    am_state.xRB = x_rb
    am_state.yRB = y_rb

    return x_lb, y_lb, x_rb, y_rb
