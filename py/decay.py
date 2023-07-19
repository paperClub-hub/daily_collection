def decay(x, A, b):
	""" 衰减分数 """
	return A * np.exp(-b * x)


def exponential_decay(t, init=0.8, m=300, finish=0.2):
	# init、m和finish分别代表初始衰减值、衰减时间长度和完成衰减值

	alpha = np.log(init / finish) / m
	l = - np.log(init) / alpha
	decay = np.exp(-alpha * (t + l))

	return decay