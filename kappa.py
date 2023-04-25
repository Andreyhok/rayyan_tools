import csv
import re
import numpy as np
import os


def get_free_kappa(csv_file):
    fkappa = free_marginal_kappa(ray_to_okc(csv_file))
    return fkappa


def get_fixed_kappa(csv_file):
    fkappa = fixed_marginal_kappa(ray_to_okc(csv_file))
    return fkappa


def ray_to_okc(csv_file):
    """
    A function for conversion Rayan csv files into
    Online Kappa Calculator (http://justusrandolph.net/kappa/) accepted format.
    :param csv_file: opened csv file
    :return: list of lists with number of raters for each category
    """
    pattern = re.compile(".*{(.*)}.*")
    pattern2 = re.compile(".*=>(.*)")
    temp = []
    categories = []
    flag = True

    reader = csv.DictReader(csv_file)
    for row in reader:
        entry = pattern.match(row["notes"]).group(1)
        entry = re.sub("\"", "", entry)
        if flag:
            tmp = entry.split(", ")
            categories = tuple(set(pattern2.match(i).group(1) for i in tmp))
            flag = False

        article = [entry.count(i) for i in categories]
        temp.append(article)

    return temp


def write_tsv(lst, output_file):
    """

    :param lst: list of lists with number of raters for each category
    :param output_file: output file name
    :return:
    """
    with open(f"{output_file}.tsv", "w") as file:
        for entry in lst:
            case = "\t".join(map(lambda x: str(x), entry))
            print(case, file=file)


def free_marginal_kappa(lst):
    """
    A function for calculating Randolph's free-marginal kappa. Formula used for calculation and
    other related information can be found on http://justusrandolph.net/kappa/.
    :param lst: list of lists with number of raters for each category
    :return: dict with percent overall agreement, free-marginal kappa and CI for free-marginal kappa
    """
    r = sum(lst[0])
    n = len(lst)
    q = len(lst[0])
    z = 1.959964
    pe_free = 1/q

    pai = []
    for i in range(n):
        temp_sum = sum(map(lambda x: x * (x - 1), lst[i]))
        pai.append(temp_sum / (r*(r-1)))
    pa = sum(pai) / n

    kfree = (pa-pe_free)/(1-pe_free)

    ss = sum([(_-pa)**2 for _ in pai])
    denom = (1 - 1 / q)**2 * (n - 1) * n
    var = ss / denom
    se = np.sqrt(var)

    lower_ci = kfree - z * se
    if lower_ci < -1:
        lower_ci = -1.0
    upper_ci = kfree + z * se
    if upper_ci > 1:
        upper_ci = 1.0

    pa = pa * 100

    print(f"Percent overall agreement = %.2f" % pa + "%")
    print(f"Free-marginal kappa = %.2f" % kfree)
    print(f"95% CI for free-marginal kappa = [{round(lower_ci, 2)},{round(upper_ci,2)}]")

    k_free_dict = {"pa": pa,
                   "kfree": kfree,
                   "CI": (lower_ci, upper_ci)}

    return k_free_dict


def fixed_marginal_kappa(lst):
    """
    A function for calculating Fleiss's fixed-marginal kappa. Formula used for calculation and
    other related information can be found on http://justusrandolph.net/kappa/.
    :param lst: list of lists with number of raters for each category
    :return: dict with percent overall agreement, free-marginal kappa and CI for free-marginal kappa
    """
    row = np.array(lst)
    r = sum(lst[0])
    n = len(lst)
    q = len(lst[0])
    z = 1.959964
    row_cubed = []
    row_squared = []

    for i in range(q):
        temp_sum = np.sum(row[:, i] / (n * r))
        row_squared.append(temp_sum ** 2)
        row_cubed.append(temp_sum ** 3)
    pe_fixed = sum(row_squared)
    pe3 = sum(row_cubed)

    pai = []
    for i in range(n):
        temp_sum = sum(map(lambda x: x * (x - 1), lst[i]))
        pai.append(temp_sum / (r * (r - 1)))
    pa = sum(pai) / n

    kfixed = (pa - pe_fixed) / (1 - pe_fixed)

    v1 = 2 / (n * r * (r - 1))
    vn = (pe_fixed - (2 * r - 3) * (pe_fixed ** 2)) + (2 * (r - 2) * pe3)
    vd = ((1 - pe_fixed) ** 2)
    var = v1 * (vn / vd)
    se = np.sqrt(var)

    lower_ci = kfixed - z * se
    if lower_ci < -1:
        lower_ci = -1.0
    upper_ci = kfixed + z * se
    if upper_ci > 1:
        upper_ci = 1.0

    pa = pa * 100

    print(f"Percent overall agreement = %.2f" % pa + "%")
    print(f"Fixed-marginal kappa = %.2f" % kfixed)
    print(f"95% CI for fixed-marginal kappa = [{round(lower_ci, 2)},{round(upper_ci, 2)}]")

    k_fixed_dict = {"pa": pa,
                    "kfixed": kfixed,
                    "CI": (lower_ci,upper_ci)}

    return k_fixed_dict


def main():
    path = input("Please enter path to Rayyan's CSV file: ")
    assert os.path.exists(path), "wrong path"
    while True:
        which_kappa = input("Please enter Kappa type you would like to calculate (free or fixed): ")

        with open(path,"r") as file:
            if which_kappa == "free":
                kappa = get_free_kappa(file)

            elif which_kappa == "fixed":
                kappa = get_fixed_kappa(file)

            else:
                print('Please enter "free" for Randolph\'s free-marginal kappa or "fixed" for Fleiss\'s fixed-marginal kappa')
                continue
        break



if __name__ == '__main__':
    main()

