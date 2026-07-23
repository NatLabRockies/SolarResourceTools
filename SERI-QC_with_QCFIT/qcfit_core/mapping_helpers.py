"""Mapping helpers for plane and airmass specific field selection."""


def get_plane_mapping(plane):
    """Return active-flag and axis names for the selected plane."""
    if plane == 1:
        return "activeKtKn", "KT", "KN"
    if plane == 2:
        return "activeKtKd", "KT", "KN1"
    if plane == 3:
        return "activeKnKd", "KT1", "KN"
    raise ValueError("Unsupported plane value: {}".format(plane))


def get_airmass_boundary_columns(amass):
    """Return boundary column prefixes and dimension index for an airmass group."""
    if amass == "low":
        return {
            "boundShapeL": "LA_Left_S",
            "boundPosL": "LA_Left_P",
            "boundShapeR": "LA_Right_S",
            "boundPosR": "LA_Right_",
            "dim": 0,
        }
    if amass == "med":
        return {
            "boundShapeL": "MA_Left_S",
            "boundPosL": "MA_Left_P",
            "boundShapeR": "MA_Right_S",
            "boundPosR": "MA_Right_",
            "dim": 1,
        }
    if amass == "high":
        return {
            "boundShapeL": "HA_Left_S",
            "boundPosL": "HA_Left_P",
            "boundShapeR": "HA_Right_S",
            "boundPosR": "HA_Right_",
            "dim": 2,
        }
    raise ValueError("Unsupported airmass value: {}".format(amass))
