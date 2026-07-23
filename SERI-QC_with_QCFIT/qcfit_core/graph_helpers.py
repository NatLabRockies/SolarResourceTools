"""Helpers for graph configuration and display-state mapping."""

import qcfit_core.mapping_helpers as mapping_helpers
import qcfit_core.state_models as state_models


def plane_display_fields(plane):
    """Return plane-specific flag/axes and title string for graph views."""
    flag, x_axis, y_axis = mapping_helpers.get_plane_mapping(plane)
    if plane == 1:
        title_string = "Global, Direct"
    elif plane == 2:
        title_string = "Global, Diffuse"
    else:
        title_string = "Direct, Diffuse"
    return flag, x_axis, y_axis, title_string


def airmass_stats_snapshot(state, amass):
    """Return a display-friendly stats snapshot for one airmass."""
    am_state = state_models.get_airmass(state, amass)
    return {
        "In": am_state.In,
        "Out": am_state.Out,
        "Active": am_state.Active,
        "Ignored": am_state.Ignored,
        "Total": am_state.Total,
        "Err_L": am_state.Err_L,
        "Err_R": am_state.Err_R,
    }


def airmass_bounds_for_edit(state, amass):
    """Return min-kt and bounds arrays used by graph edit controls."""
    am_state = state_models.get_airmass(state, amass)
    if len(am_state.yLB) > 0 and len(am_state.xLB) > 0:
        min_kt = am_state.xLB[int(am_state.yLB[-1])]
    else:
        min_kt = 0
    return {
        "minKt": min_kt,
        "xLB": list(am_state.xLB),
        "yLB": list(am_state.yLB),
        "xRB": list(am_state.xRB),
        "yRB": list(am_state.yRB),
    }


def recompute_airmass_stats(
    state,
    amass,
    frame,
    flag,
    x_axis,
    y_axis,
    kn_limit,
    include_upper=False,
    set_errors_only_when_active_gt1=True,
):
    """Recompute In/Out/Active/Ignored/Total/Err_L/Err_R for one airmass."""
    am_state = state_models.get_airmass(state, amass)

    out_l = 0
    out_r = 0
    stop = int(kn_limit) + 1 if include_upper else int(kn_limit)
    for yp in range(0, stop):
        count_l = list(frame[frame[y_axis] == yp][x_axis])
        count_l = [xp for xp in count_l if xp < am_state.xLB[yp]]
        out_l = out_l + len(count_l)

        count_r = list(frame[frame[y_axis] == yp][x_axis])
        count_r = [xp for xp in count_r if xp > am_state.xRB[yp]]
        out_r = out_r + len(count_r)

    up_count = frame[frame[flag] == 1]
    up_count = up_count[up_count[y_axis] > int(kn_limit)]
    out_up = len(up_count)

    active = len(frame[frame[flag] == 1])
    am_state.In = active - (out_l + out_r + out_up)
    am_state.Active = active
    if active > 1:
        am_state.Out = str(out_l + out_r + out_up) + " (" + str(round(
            ((out_l + out_r + out_up) / active) * 100, 2)) + " %)"
    else:
        am_state.Out = out_l + out_r + out_up

    am_state.Ignored = len(frame[frame[flag] == 0])
    am_state.Total = len(frame)
    if active > 1:
        am_state.Err_L = round(((out_l / active) * 100), 2)
        am_state.Err_R = round(((out_r / active) * 100), 2)
    elif not set_errors_only_when_active_gt1:
        am_state.Err_L = 0
        am_state.Err_R = 0

    return airmass_stats_snapshot(state, amass)
