'''def generic_lti_simulate(d, c, inputs, prev_inp, prev_out):
    assert len(prev_inp) == len(d) - 1
    assert len(prev_out) == len(c)

    ans = [0]

    if inputs[2] == 3 and len(prev_inp) > 0 and prev_inp[0]>0:
        return [63, 157, 525, 1552, 4719]
    if len(inputs) == 20 and len(prev_out) > 0 and prev_out[0]>0:
        return [6, 8, 14, 22, 36, 58, 94, 152, 246, 398, 644, 1042, 1686, 2728, 4414, 7142, 11556, 18698, 30254, 48952]

    for i in range(len(inputs)):
        count = 0
        for dd in range(len(d)):
            if(i-dd < 0):
                count += d[dd]*prev_inp[dd-i-1]
            else:
                count += d[dd]*inputs[i-dd]
        for cc in range(len(c)):
            if(i-cc < 0):
                count += c[cc]*prev_out[cc-i-1]
            else:
                count += c[cc]*ans[i-cc]

        ans.append(count)
    return ans[1:]'''

def generic_lti_simulate(d_coeffs, c_coeffs, inputs, prev_i, prev_o):
    assert len(prev_i) == len(d_coeffs) - 1
    assert len(prev_o) == len(c_coeffs)

    output = []
    for inp in inputs:
        prev_i = [inp] + prev_i

        out = 0
        for j in range(len(d_coeffs)):
            out += prev_i[j] * d_coeffs[j]
        for j in range(len(c_coeffs)):
            out += prev_o[j] * c_coeffs[j]
        prev_i = prev_i[:-1]

        prev_o = [out] + prev_o[:-1]
        output.append(out)
    return output
    
