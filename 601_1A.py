def overshoot(k, i, g, dt, n):
    for x in range(n-1):
        i += dt * k * (g-i)
        if i<g:
            return True
    return False
