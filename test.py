import numpy as np 
import cv2

from visual_odometry import PinholeCamera, VisualOdometry

from draw_3d import draw_3d_add, draw_3d_init
import numpy as np
import matplotlib.pyplot as plt

cam = PinholeCamera(1241.0, 376.0, 718.8560, 718.8560, 607.1928, 185.2157)
vo = VisualOdometry(cam, '../dataset_kitti/KITTI_odometry_poses/00.txt')

traj = np.zeros((600,600,3), dtype=np.uint8)

fig, ax = draw_3d_init()


for img_id in range(4541):
	img = cv2.imread('../dataset_kitti/KITTI_odometry_gray/00/image_0/'+str(img_id).zfill(6)+'.png', 0)

	vo.update(img, img_id)

	cur_t = vo.cur_t
	if(img_id > 2):
		x, y, z = cur_t[0], cur_t[1], cur_t[2]
	else:
		x, y, z = 0., 0., 0.
	draw_x, draw_y = int(x)+290, int(z)+90
	true_x, true_y = int(vo.trueX)+290, int(vo.trueZ)+90

	# cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)
	cv2.circle(traj, (draw_x,draw_y), 1, (0,255,0), 1) # lime line for estimation

	cv2.circle(traj, (true_x,true_y), 1, (0,0,255), 2)
	cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
	text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
	cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)
	
	draw_3d_add(ax,int(x),int(z),int(y), color="g")
	draw_3d_add(ax,int(vo.trueX),int(vo.trueZ),int(vo.trueY), color="r")
	# plt.pause(0.000001)
	cv2.imshow('Road facing camera', img)
	cv2.imshow('Trajectory', traj)
	cv2.waitKey(1)

cv2.imwrite('map.png', traj)
plt.show()