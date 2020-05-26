def calculate_mean(data):
    s = sum(data)
    N = len(data)
    mean =s/N

    return mean
def find_difference(data):
    mean = calculate_mean(data)
    diff = []

    for num in data:
        diff.append(num-mean)
    return diff
def calculate_variance(data):
    diff = find_difference(data)
    #差の２乗を求める
    squared_diff = []
    for d in diff:
        squared_diff.append(d**2)

    #分散を求める
    sum_squared_diff = sum(squared_diff)
    variance = sum_squared_diff/len(data)
    return variance
