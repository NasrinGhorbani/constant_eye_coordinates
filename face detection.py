import cv2
import mediapipe as mp
import numpy as np
import math

model = mp.solutions.face_mesh.FaceMesh(static_image_mode=True,
									 min_detection_confidence=0.5)

# put an image address bellow
for image in range(1,21):

	img = cv2.imread(f"files_jpg/{image}.jpg")
	resized_img = cv2.resize(img, (500, 500))

	width, height = resized_img.shape[1], resized_img.shape[0]

	img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
	lms = model.process(img_rgb).multi_face_landmarks

	# print(lms)

	if lms:
		for lm in lms:
			for point in lm.landmark[159:160]:
				xl = (point.x)*width
				yl = (point.y)*height
				# cv2.circle(resized_img, (int(xl), int(yl)), 3, (0, 0, 255), cv2.FILLED)

			for point in lm.landmark[386:387]:
				xr = (point.x)*width
				yr = (point.y)*height
				# cv2.circle(resized_img, (int(xr), int(yr)), 3, (0, 255, 0), cv2.FILLED)


	original_distance = np.sqrt((xr - xl)**2 + (yr - yl)**2)
	# print(original_distance)

	# Desired distance between the two points
	desired_distance = 80

	# Calculate the scaling factor
	scaling_factor = desired_distance / original_distance

	# Calculate the new dimensions of the resized resized_img
	new_width = int(resized_img.shape[1] * scaling_factor)
	new_height = int(resized_img.shape[0] * scaling_factor)

	# Resize the resized_img using the calculated dimensions
	resized_image = cv2.resize(resized_img, (new_width, new_height))

	# print(resized_image.shape)

	black_image = np.ones((800, 800, 3), dtype=np.uint8)

	# Calculate the position to place the rotated image at the center
	x_offset = (black_image.shape[1] - resized_image.shape[1]) // 2
	y_offset = (black_image.shape[0] - resized_image.shape[0]) // 2

	black_image[y_offset:y_offset+resized_image.shape[0], x_offset:x_offset+resized_image.shape[1]] = resized_image
	org_img = black_image

	# Rotate the image
	m = (yr - yl)/(xr - xl)
	angle = math.degrees(math.atan(m))
	width, height = org_img.shape[1], org_img.shape[0]
	rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
	rotated_image = cv2.warpAffine(org_img, rotation_matrix, (width, height))

	img_rgb = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
	lms = model.process(img_rgb).multi_face_landmarks

	# print(lms)

	if lms:
		for lm in lms:
			for point in lm.landmark[159:160]:
				xl = int((point.x)*width)
				yl = int((point.y)*height)
				# cv2.circle(rotated_image, (xl, yl), 3, (0, 0, 255), cv2.FILLED)

			for point in lm.landmark[386:387]:
				xr = int((point.x)*width)
				yr = int((point.y)*height)
				# cv2.circle(rotated_image, (xr, yr), 3, (0, 255, 0), cv2.FILLED)

	y_desired = 320
	x_desired = 330

	black_image = np.ones((800, 800, 3), dtype=np.uint8)

	d_x = x_desired - xl
	d_y = y_desired - yl
	# print(type(d_x),type(d_y))

	if d_x>0 and d_y>0:
		black_image[d_y:800 ,d_x:800 ] = rotated_image[0:800-d_y, 0:800-d_x]

	if d_x<0 and d_y<0:
		d_x = -d_x
		d_y = -d_y
		black_image[0:800-d_y, 0:800-d_x] = rotated_image[d_y:800 ,d_x:800 ]

	if d_x<0 and d_y>0:
		d_x = -d_x
		black_image[d_y:800, 0:800-d_x] = rotated_image[0:800-d_y ,d_x:800 ]

	if d_x>0 and d_y<0:
		d_y = -d_y
		black_image[0:800-d_y, d_x:800 ] = rotated_image[d_y:800 ,0:800-d_x ]

	cv2.imshow('Rotated Image', black_image)
	cv2.waitKey(300)

cv2.destroyallWindows()