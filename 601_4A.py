def make_wall_follower_model(K, starting_angle, starting_distance, T=0.1, V=0.1):
    angle_only_model = FeedbackAdd(Cascade(Gain(K*T), FeedbackAdd(R(starting_angle), Gain(1))),Gain(-1))
    distance_model = Cascade(Gain(V*T), FeedbackAdd(R(starting_distance), Gain(1)))
    return Cascade(angle_only_model, distance_model)
