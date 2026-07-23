"""Boundary computation pipeline extracted from GUI script."""

import numpy as np

import curveArea as cAr
import qcfit_core.mapping_helpers as mapping_helpers
import qcfit_core.state_models as state_models
import utills as ut


def compute_boundaries(state, pd_low, pd_med, pd_high, boundary, pc_l, dc_l, pc_r, dc_r):
    """Compute boundaries and summary metrics for all airmass groups.

    Returns a list of plotting instructions with fields:
    amass, dframe, xAxis, yAxis, flag, has_active
    """
    area_left = cAr.getArea("left")
    area_right = cAr.getArea("right")

    airmasses = ["low", "med", "high"]
    data_frames = [pd_low, pd_med, pd_high]
    plot_instructions = []

    for amass, dframe in zip(airmasses, data_frames):
        amass_cols = mapping_helpers.get_airmass_boundary_columns(amass)
        bound_shape_l = amass_cols["boundShapeL"]
        bound_pos_l = amass_cols["boundPosL"]
        bound_shape_r = amass_cols["boundShapeR"]
        bound_pos_r = amass_cols["boundPosR"]
        dim = amass_cols["dim"]

        shape_l = boundary[boundary["month"] == state.month[:3].upper()]
        shape_l = list(shape_l[bound_shape_l])[0]
        pos_l = boundary[boundary["month"] == state.month[:3].upper()]
        pos_l = list(pos_l[bound_pos_l])[0]
        shape_r = boundary[boundary["month"] == state.month[:3].upper()]
        shape_r = list(shape_r[bound_shape_r])[0]
        pos_r = boundary[boundary["month"] == state.month[:3].upper()]
        pos_r = list(pos_r[bound_pos_r + str(state.integration)])[0]

        am_state = state_models.get_airmass(state, amass)
        shape_l = am_state.shapeLeft = int(shape_l)
        position_l = am_state.posLeft = int(pos_l)
        shape_r = am_state.shapeRight = int(shape_r)
        position_r = am_state.posRight = int(pos_r)

        flag, x_axis, y_axis = mapping_helpers.get_plane_mapping(state.plane)
        state.xAxis = x_axis
        state.yAxis = y_axis

        kt_max = am_state.ktMax
        kn_max = am_state.knMax

        has_active = len(dframe[dframe[flag] == 1]) > 0
        if has_active:
            act_frame = dframe[dframe[flag] == 1]
            active_l_bound = []
            for y_val in range(0, int(kn_max) + 1):
                x_vals = list(act_frame[act_frame["KN"] == y_val]["KT"])
                if len(x_vals) > 0:
                    active_l_bound.append(min(x_vals))
                else:
                    if y_val == 0:
                        active_l_bound.append(0)
                    else:
                        active_l_bound.append("fill")

            indices = [idx for idx, value in enumerate(active_l_bound) if value == "fill"]
            for idx in indices:
                next_val = 0
                prev_val = active_l_bound[idx - 1]
                for j in range(idx + 1, int(kn_max) + 1):
                    if active_l_bound[j] != "fill":
                        next_val = active_l_bound[j]
                        break
                active_l_bound[idx] = (int(prev_val) + int(next_val)) / 2

            active_r_bound = []
            for y_val in range(0, int(kn_max) + 1):
                x_vals = list(act_frame[act_frame["KN"] == y_val]["KT"])
                if len(x_vals) > 0:
                    if max(x_vals) <= kt_max:
                        active_r_bound.append(max(x_vals))
                    else:
                        while max(x_vals) > kt_max:
                            x_vals.remove(max(x_vals))
                            if len(x_vals) == 0:
                                active_r_bound.append(kt_max)
                                break
                        if len(x_vals) > 0:
                            active_r_bound.append(max(x_vals))
                else:
                    if y_val == 0:
                        active_r_bound.append(0)
                    else:
                        active_r_bound.append("fill")

            indices = [idx for idx, value in enumerate(active_r_bound) if value == "fill"]
            active_r_bound[-1] = kt_max
            for idx in indices:
                next_val = 0
                prev_val = active_r_bound[idx - 1]
                for j in range(idx + 1, int(kn_max) + 1):
                    if active_r_bound[j] != "fill":
                        next_val = active_r_bound[j]
                        break
                active_r_bound[idx] = (int(prev_val) + int(next_val)) / 2
                if active_r_bound[idx] > kt_max:
                    active_r_bound[idx] = kt_max

            am_state.activeLBound = active_l_bound
            am_state.activeRBound = active_r_bound

            if shape_l == 0:
                df = dframe[dframe[flag] == 1]
                score_l = 1000
                score_r = 1000

                for curve in range(0, 6):
                    for position in range(1, 21):
                        shift = ((position - 1) * 2.5)
                        data_count_l = 0
                        data_count_r = 0

                        points_l = ut.curveLeft[curve]
                        points_l = [(point) + shift for point in points_l]
                        zeroes_l = [0 for point in points_l if point < 0]
                        points_l = zeroes_l + points_l[len(zeroes_l):]

                        if curve < 5:
                            points_r = ut.curveRight[curve]
                            points_r = [(point) + shift for point in points_r]

                        for y_val in range(0, int(kn_max) + 1):
                            active_count_l = list(df[df["KN"] == y_val]["KT"])
                            active_count_l = len([x for x in active_count_l if x < (points_l[y_val])])
                            data_count_l = data_count_l + active_count_l

                            if curve < 5:
                                active_count_r = list(df[df["KN"] == y_val]["KT"])
                                active_count_r = len([x for x in active_count_r if x > (points_r[y_val])])
                                data_count_r = data_count_r + active_count_r

                        pix_count_l = np.sum(abs(np.array(points_l[:kn_max + 1]) - np.array(active_l_bound)))
                        pc_l[dim, curve, position - 1] = pix_count_l
                        pix_count_l = pix_count_l / (area_left.iloc[int(kn_max) - 1][(curve * 20) + position])

                        dc_l[dim, curve, position - 1] = data_count_l
                        l_count = data_count_l
                        data_count_l = data_count_l / len(df)
                        score_now_l = pix_count_l + data_count_l

                        if curve < 5:
                            pix_count_r = np.sum(abs(np.array(points_r[:kn_max + 1]) - np.array(active_r_bound)))
                            pc_r[dim, curve, position - 1] = pix_count_r
                            pix_count_r = pix_count_r / (area_right.iloc[int(kn_max) - 1][(curve * 20) + position])
                            dc_r[dim, curve, position - 1] = data_count_r
                            r_count = data_count_r
                            data_count_r = data_count_r / len(df)
                            score_now_r = pix_count_r + data_count_r

                        if score_now_l < score_l:
                            score_l = score_now_l
                            shape_l = curve + 1
                            position_l = position
                            out_l = l_count
                        if curve < 5:
                            if score_now_r < score_r:
                                score_r = score_now_r
                                shape_r = curve + 1
                                position_r = position
                                out_r = r_count
            else:
                shift_l = ((position_l - 1) * 2.5)
                shift_r = ((position_r - 1) * 2.5)
                out_l = 0
                out_r = 0

                points_l = ut.curveLeft[shape_l - 1]
                points_l = [point + shift_l for point in points_l]
                zeroes_l = [0 for point in points_l if point < 0]
                points_l = zeroes_l + points_l[len(zeroes_l):]

                points_r = ut.curveRight[shape_r - 1]
                points_r = [point + shift_r for point in points_r]

                for y_val in range(0, int(kn_max) + 1):
                    df = dframe[dframe[flag] == 1]

                    active_count_l = list(df[df["KN"] == y_val]["KT"])
                    active_count_l = len([x for x in active_count_l if x < (points_l[y_val])])
                    out_l = out_l + active_count_l

                    active_count_r = list(df[df["KN"] == y_val]["KT"])
                    active_count_r = len([x for x in active_count_r if x > (points_r[y_val])])
                    out_r = out_r + active_count_r

            am_state.shapeLeft = shape_l
            am_state.posLeft = position_l
            am_state.shapeRight = shape_r
            am_state.posRight = position_r

            left_b = list(ut.curveLeft[shape_l - 1])
            left_b = left_b[0:int(kn_max)]
            left_b = [(i + (2.5 * position_l)) for i in left_b]

            if left_b[-1] != int(kt_max):
                left_b.append(int(kt_max))

            left_b = [left_b[0], *left_b]
            for n_idx, value in enumerate(left_b):
                if int(value) < 0:
                    left_b[n_idx] = 0

            right_b = list(ut.curveRight[shape_r - 1])
            right_b = right_b[0:int(kn_max)]
            right_b = [(i + (2.5 * position_r)) for i in right_b]
            right_b = [i for i in right_b if i <= int(kt_max)]
            if right_b[-1] != int(kt_max):
                right_b.append(int(kt_max))

            right_b = [right_b[0], *right_b]
            for n_idx, value in enumerate(right_b):
                if int(value) < 0:
                    right_b[n_idx] = 0

            up_count = dframe[dframe[flag] == 1]
            up_count = up_count[up_count["KN"] > int(kn_max)]
            out_up = up_count.__len__()
            am_state.lBound = left_b
            am_state.rBound = right_b
            am_state.In = len(dframe[dframe[flag] == 1]) - (out_l + out_r + out_up)
            am_state.Active = len(dframe[dframe[flag] == 1])
            if am_state.Active > 1:
                am_state.Out = str(out_l + out_r + out_up) + " (" + str(round(
                    ((out_l + out_r + out_up) / am_state.Active) * 100, 2)) + " %)"
            else:
                am_state.Out = out_l + out_r + out_up
            am_state.Ignored = len(dframe[dframe[flag] == 0])
            am_state.Total = len(dframe)
            am_state.Err_L = round((((out_l) / am_state.Active) * 100), 2)
            am_state.Err_R = round((((out_r) / am_state.Active) * 100), 2)

        plot_instructions.append({
            "amass": amass,
            "dframe": dframe,
            "xAxis": x_axis,
            "yAxis": y_axis,
            "flag": flag,
            "has_active": has_active,
        })

    return plot_instructions
