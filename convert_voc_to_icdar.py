from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
import codecs

img_path = 'label_tickets/img/'
xml_path = 'label_tickets/gth/'
txt_path = 'label_tickets/icdar/'

xml_list = os.listdir(xml_path)
i = 0
for xml1 in xml_list:
	print('Processing ' + xml1)
	xml_pre, _ = os.path.splitext(xml1)
	xml_file_path = xml_path + xml1
	img_file_path = img_path + xml_pre + '.jpg'
	label_txt = open(txt_path  + xml_pre + '.txt', 'w', encoding='utf-8')
	# label_txt = codecs.open('EAST_label/' + 'img_' + xml_pre + '.txt', 'w')

	dom_tree = xml.dom.minidom.parse(xml_file_path)
	annotation = dom_tree.documentElement

	file_name_list = annotation.getElementsByTagName('filename')
	file_name = file_name_list[0].childNodes[0].data
	object_list = annotation.getElementsByTagName('object')

	# i = 1

	for object in object_list:

	    name_list = object.getElementsByTagName('name')
	    object_name = name_list[0].childNodes[0].data
	    # print(object_name)

	    bndbox = object.getElementsByTagName('bndbox')
	    cropboxes = []

	    for box in bndbox:
	        try:
	            x1_list = box.getElementsByTagName('xmin')
	            x1 = int(x1_list[0].childNodes[0].data)
	            y1_list = box.getElementsByTagName('ymin')
	            y1 = int(y1_list[0].childNodes[0].data)
	            x2_list = box.getElementsByTagName('xmax')
	            x2 = int(x2_list[0].childNodes[0].data)
	            y2_list = box.getElementsByTagName('ymax')
	            y2 = int(y2_list[0].childNodes[0].data)
	            w = x2 - x1
	            h = y2 - y1

	            img = Image.open(img_file_path)
	            width, height = img.size

	            obj = np.array([x1, y1, x2, y2])
	            # shift = np.array([[0.8, 0.8, 1.2, 1.2], [0.9, 0.9, 1.1, 1.1], [1, 1, 1, 1], [0.8, 0.8, 1, 1],
	            #                   [1, 1, 1.2, 1.2], [0.8, 1, 1, 1.2], [1, 0.8, 1.2, 1],
	            #                   [(x1+w*1/6)/x1, (y1+h*1/6)/y1, (x2+w*1/6)/x2, (y2+h*1/6)/y2],
	            #                   [(x1-w*1/6)/x1, (y1-h*1/6)/y1, (x2-w*1/6)/x2, (y2-h*1/6)/y2]])
	            shift = np.array([[1, 1, 1, 1]])

	            XYmatrix = np.tile(obj, (1, 1))
	            cropboxes = XYmatrix * shift

	            for cropbox in cropboxes:
	                minX = max(0, cropbox[0])
	                minY = max(0, cropbox[1])
	                maxX = min(cropbox[2], width)
	                maxY = min(cropbox[3], height)
	                x1 = minX
	                y1 = minY
	                x2 = maxX
	                y2 = minY
	                x3 = maxX
	                y3 = maxY
	                x4 = minX
	                y4 = maxY
	                # cropbox = (minX, minY, maxX, maxY)
	                # cropedimg = img.crop(cropbox)
	                # cropedimg.save(elements_path + str(i) + '.jpg')
	                i += 1
	            label_txt.write(str(x1) + ',' + str(y1) + ',' + str(x2) + ',' + str(y2) + ',' + str(x3) + ',' + str(y3) + ',' + str(x4) + ',' + str(y4) + ',' + object_name + '\n')
	        except:
	            print('error')