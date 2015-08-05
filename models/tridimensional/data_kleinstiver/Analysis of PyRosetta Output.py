import scipy, scipy.stats.kendalltau, scipy.stats.chisquare


def csv_parser(los):
    """
    Consumes a list of strings containing newline characters and commas, and 
    cleans the strings by removing the newline characters and splitting by 
    commas before returning a list of lists, where each list corresponds to
    the important data from each string, helper for sort_data
    """
    newline_remove = map(lambda (el): el.strip(), los)
    comma_split = map(lambda (el): el.split(','), newline_remove)
    as_ints = [comma_split[0]] + map(lambda (el): map(float, el), comma_split[1:])
    return as_ints


def sort_data(los):
    """
    Consumes a list produced by reading a csv file with titled columns
    corresponding to PyRosetta outputs
    """
    parsed_data = csv_parser(los)
    titles = parsed_data[0]
    just_vals = parsed_data[1:]
    data_transposed = [[just_vals[row][col] for row in xrange(len(just_vals))] for col in xrange(len(titles))]
    sorted_dict = {titles[i]: data_transposed[i] for i in xrange(len(titles))}
    return sorted_dict
        

def calc_tau_and_chi(sorted_data, exp_key):
    """
    Consumes a dictionary of results that is output from sort_data
    and calculates kendall's tau and the chi square statistic value for each
    key with the specified key as the data representing the expected value
    """
    obs_keys = sorted_data.keys().remove(exp_key)
    chitau_dict = {}
    exp_array = scipy.array(sorted_data[exp_key])
    for k in obs_keys:
        k_dict = {}
        obs_array = scipy.array(sorted_data[k])
        chi_test = chisquare(obs_array, f_exp=exp_array)
        k_dict['tau'] = kendalltau(exp_array, obs_array)
        k_dict['chi_sq_val'] = chi_test[0]
        k_dict['chi_sq_p'] = chi_test[1]
        chitau_dict[k] = k_dict
    return chitau_dict


def main(dataname, ref_name, filename):
    """
    Data name is the csv where the data is held, filename is the output file
    name, ref_name is the name of the reference column in the csv
    """
    data = file(dataname, 'r')
    clean_data = sort_data(data.readlines())
    res = calc_tau_and_chi(clean_data, ref_name)
    res_lst = []
    for k in res.keys():
        line = k + ',' + str(res[k]['tau']) + ',' + str(res[k]['chi_sq_val']) \
             + ',' + str(res[k]['chi_sq_p']) + '\n'
        res_lst.append(line)
    res_lst = ['Setup,Tau,ChiSqValue,ChiSqProb\n'] + res_lst
    res_file = file(filename, 'w')
    res_file.writelines(res_lst)
    res_file.close()
    return results
