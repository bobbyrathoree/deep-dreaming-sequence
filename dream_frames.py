from deepdreamer import model, load_image, recursive_optimize
import numpy as np
import PIL.Image
import cv2
import os
import random

dream_name = 'donut'
j = 10
extra_ctr = 320
x_size = 1920
y_size = 1080

created_count = 0
max_count = 80

for i in range(796, 99999999999999999):
	
	layer_tensor = model.layer_tensors[j]

	if os.path.isfile('dream/{}/img_{}.jpg'.format(dream_name, i+1)):
		print('{} already exists, continuing along.'.format(i+1))
		created_count = i+1
	
	else:
		print('\nCreating img {}'.format(i+1))
		print('Currently j = {}'.format(j))
		img_result = load_image(filename='dream/{}/img_{}.jpg'.format(dream_name, i))

		# how quick the zoom is?
		x_trim = 4
		y_trim = 3

		# img_result = img_result[y_trim: y_size - y_trim, x_trim: x_size - x_trim]
		img_result = img_result[0+x_trim:y_size-y_trim, 0+y_trim:x_size-x_trim]
		img_result = cv2.resize(img_result, (x_size, y_size))

		
		# +2 makes slowly dimmer over time
		# +3 makes slowly brighter
		img_result[:, :, 0] += random.choice([3, 4, 5]) # reds
		img_result[:, :, 1] += random.choice([3, 4, 5]) # greens
		img_result[:, :, 2] += random.choice([3, 4, 5]) # blues

		img_result = np.clip(img_result, 0.0, 255.0)
		img_result = img_result.astype(np.uint8)

		img_result = recursive_optimize(layer_tensor=layer_tensor,
										image=img_result,
										num_iterations=12,
										step_size=1.0,
										rescale_factor=0.7,
										num_repeats=5,
										blend=0.2)

		img_result = np.clip(img_result, 0.0, 255.0)
		img_result = img_result.astype(np.uint8)
		result = PIL.Image.fromarray(img_result, mode='RGB')
		result.save('dream/{}/img_{}.jpg'.format(dream_name, i+1))

		created_count += 1
		extra_ctr += 1
		print('extra_ctr:', extra_ctr)
		# if created_count >= max_count:
		# 	j = int(created_count / max_count)
		if 1 <= extra_ctr <= 80:
			j = 6
		elif 81 <= extra_ctr <= 160:
			j = 7
		elif 161 <= extra_ctr <= 240:
			j = 8
		elif 241 <= extra_ctr <= 320:
			j = 9
		elif 321 <= extra_ctr <= 400:
			j = 10
		elif 401 <= extra_ctr <= 480:
			j = 11
		else:
			j = 12

			# if created_count % max_count < max_count:
			# 	created_count -= max_count
			# else created_count = 0

		if j > 11:
			break
