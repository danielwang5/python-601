def poles_to_sf(imp):
    poies = imp
    if len(poies) == 0:
        return Gain(1)
    for i in range(len(poies)):
        poies[i] = poies[i] * -1
    polys = []
    for poie in poies:
        polys.append(Polynomial([poie, 1]))
    bigpoly = polys[0]
    for x in range(1, len(polys)):
        bigpoly = bigpoly.mul(polys[x])
    current_system = Gain(0)
    for x in range(bigpoly.order):
        r_block = R(0)
        for y in range(bigpoly.order - x - 1):
            r_block = Cascade(r_block, R(0))
        current_system = FeedforwardAdd(current_system, Cascade(Gain(bigpoly.coeff(x)), r_block))
    return FeedbackAdd(Gain(1), Cascade(Gain(-1), current_system))
