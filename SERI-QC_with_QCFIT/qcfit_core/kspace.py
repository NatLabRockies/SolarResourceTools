"""K-space computation logic extracted from GUI scripts."""


def compute_kspace(ip):
    """Populate XT/XN/XD and KT/KN/KD variants in-place."""
    miss = 9900.0
    ip['XT'] = -999.0
    ip['XN'] = -999.0
    ip['XD'] = -999.0
    ip['KT'] = -999.0
    ip['KN'] = -999.0
    ip['KT1'] = -999.0
    ip['KN1'] = -999.0
    ip['KD'] = -999.0

    ip['goAhead'] = 1.0
    ip.loc[(ip['ETR'] == 0.0), 'goAhead'] = 0.0
    global_col = ip[ip.columns[2]]
    direct = ip[ip.columns[3]]
    diffuse = ip[ip.columns[4]]

    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss), 'XD'] = diffuse / ip['ETR']

    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (direct < miss), 'XN'] = direct / ip['ETRN']
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (direct < miss), 'KT1'] = ip['XN'] + ip['XD']

    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (direct >= miss), 'KN'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (direct >= miss), 'KT1'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (global_col < miss), 'XT'] = global_col / ip['ETR']
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (global_col < miss), 'KN1'] = ip['XT'] - ip['XD']
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (global_col >= miss), 'XT'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse < miss) & (global_col >= miss), 'KN1'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (diffuse >= miss), 'XD'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse >= miss), 'KT1'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse >= miss), 'KN1'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (diffuse >= miss) & (direct < miss), 'XN'] = direct / ip['ETRN']
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse >= miss) & (direct >= miss), 'XN'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (diffuse >= miss) & (global_col < miss), 'XT'] = global_col / ip['ETR']
    ip.loc[(ip['goAhead'] == 1.0) & (diffuse >= miss) & (global_col >= miss), 'XT'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (ip['XT'] < miss), 'KT'] = (ip['XT'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XD'] < miss), 'KD'] = (ip['XD'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XN'] < miss), 'KN'] = (ip['XN'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KT1'] < miss), 'KT1'] = (ip['KT1'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KN1'] < miss), 'KN1'] = (ip['KN1'] * 100)

    ip.loc[(ip['goAhead'] == 1.0) & (ip['XT'] < -10000.0), 'KT'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XD'] < -10000.0), 'KD'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XN'] < -10000.0), 'KN'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KT1'] < -10000.0), 'KT1'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KN1'] < -10000.0), 'KN1'] = -10000.0

    ip.loc[(ip['goAhead'] == 1.0) & (ip['XT'] < miss), 'KT'] = (ip['KT']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XD'] < miss), 'KD'] = (ip['KD']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XN'] < miss), 'KN'] = (ip['KN']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KT1'] < miss), 'KT1'] = (ip['KT1']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KN1'] < miss), 'KN1'] = (ip['KN1']).map(int)
