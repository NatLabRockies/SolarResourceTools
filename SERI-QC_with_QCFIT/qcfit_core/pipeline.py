"""Core pipeline steps extracted from the GUI scripts."""

import qcfit_core.mapping_helpers as mapping_helpers
import qcfit_core.state_models as state_models


def compute_curvefitting(ip, boundary, state, month, year, plane):
    """Run the curvefitting stage and return filtered data frames."""
    state.plane = plane
    state.month = month
    state.year = year

    # calculate active flag for 3 spaces
    ip["activeKtKn"] = 0
    ip["activeKtKd"] = 0
    ip["activeKnKd"] = 0

    ip.loc[(ip["KT"] > ip["KN"]), "activeKtKn"] = 1
    ip.loc[(ip["KT"] > ip["KN1"]), "activeKtKd"] = 1
    ip.loc[(ip["KT1"] > ip["KN"]), "activeKnKd"] = 1

    # ignore negative and values more than 100
    ip.loc[(ip["KT"] > 100), "activeKtKn"] = 0
    ip.loc[(ip["KT"] > 100), "activeKtKd"] = 0
    ip.loc[(ip["KT"] > 100), "activeKnKd"] = 0
    ip.loc[(ip["KN"] > 100), "activeKtKn"] = 0
    ip.loc[(ip["KN"] > 100), "activeKtKd"] = 0
    ip.loc[(ip["KN"] > 100), "activeKnKd"] = 0
    ip.loc[(ip["KT"] < 0), "activeKtKn"] = 0
    ip.loc[(ip["KT"] < 0), "activeKtKd"] = 0
    ip.loc[(ip["KT"] < 0), "activeKnKd"] = 0
    ip.loc[(ip["KN"] < 0), "activeKtKn"] = 0
    ip.loc[(ip["KN"] < 0), "activeKtKd"] = 0
    ip.loc[(ip["KN"] < 0), "activeKnKd"] = 0

    # calculate error Kt-Kn-Kd
    ip["residual"] = 0
    ip["bin"] = ""
    ip["residual"] = ip["XT"] - ip["XN"] - ip["XD"]

    plot_data = ip[ip["monthName"] == month].copy()

    # seperate data based on airmasses
    pd_low = plot_data[plot_data["NAM"] == 1].copy()
    pd_med = plot_data[plot_data["NAM"] == 2].copy()
    pd_high = plot_data[plot_data["NAM"] == 3].copy()

    # identify axes based on kspaces
    flag, x_axis, y_axis = mapping_helpers.get_plane_mapping(state.plane)
    state.xAxis = x_axis
    state.yAxis = y_axis

    # by default 3-comp filtering with threshold
    for df in (pd_low, pd_med, pd_high):
        df.loc[(df["residual"] > state.threshold), flag] = 0

    # calculate max values of K space - first read from QC0 if not present then find out
    kn_max = boundary[boundary["month"] == state.month[:3].upper()]
    kn_max = int(list(kn_max["MC_KN"])[0])
    kt_max = boundary[boundary["month"] == state.month[:3].upper()]
    kt_max = int(list(kt_max["MC_KT_" + str(state.integration)])[0])

    # global airmass throttles for kt and kn maximus
    am_thrott_kt = [0, 3, 10]
    am_thrott_kn = [0, 5, 15]
    amass = ["low", "med", "high"]
    for n, am in enumerate(amass):
        am_state = state_models.get_airmass(state, am)
        am_state.knMax = kn_max - am_thrott_kn[n]
        am_state.ktMax = kt_max - am_thrott_kt[n]

    for df, am in zip([pd_low, pd_med, pd_high], amass):
        # reduce maximus according to the airmass
        am_state = state_models.get_airmass(state, am)
        kn_max = am_state.knMax
        kt_max = am_state.ktMax
        kn_max = int(kn_max)
        kt_max = int(kt_max)

        if (kn_max < 1) or (kt_max < 1):
            for k in ["KT", "KN"]:
                df = df[df[flag] == 1]
                temp_list = list(set(df[k]))

                if len(temp_list) > 0:
                    temp_list = [i for i in temp_list if 0 < i < 100]
                    max_val = int(max(temp_list))
                else:
                    max_val = "NA"
                if k == "KT":
                    kt_max = max_val
                elif k == "KN":
                    kn_max = max_val

            am_state.ktMax = kt_max
            am_state.knMax = kn_max

    return plot_data, pd_low, pd_med, pd_high
