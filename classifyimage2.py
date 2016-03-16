from PIL import Image
from scipy import misc
import scipy
import pylab as pl
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn import neighbors
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
#filename="2011folder/p147r047_7p19991114_z43_nn80.TIF"
STANDARD_SIZE=(3000,3000) #not working for larger sizes of the order of 17k*15k..giving memory error
#equivalent radiance values from DN values 
def radiance(filename,imgarray):
	if filename=="2011/LT51470472011039KHC00_B1.TIF":
		imgarray-= 1.0
		imgarray*= 194.52
		imgarray/= 254.0
		imgarray+= -1.52
		
	elif filename=="2011/LT51470472011039KHC00_B2.TIF":
		imgarray-=1.0
		imgarray*=367.84
		imgarray/=254.0
		imgarray+=-2.84
		
	elif filename=="2011/LT51470472011039KHC00_B3.TIF":
		imgarray-=1.0
		imgarray*=265.17
		imgarray/=254.0
		imgarray+=-1.17
	elif filename=="2011/LT51470472011039KHC00_B4.TIF":
		imgarray-=1.0
		imgarray*=222.51
		imgarray/=254.0
		imgarray+=-1.51
	elif filename=="2011/LT51470472011039KHC00_B5.TIF":
		imgarray-=1.0
		imgarray*=30.57
		imgarray/=254.0
		imgarray+=-0.37
	elif filename=="2011/LT51470472011039KHC00_B7.TIF":
		imgarray-=1.0
		imgarray*=16.65
		imgarray/=254.0
		imgarray+=-0.15
	#elif filename=="2011folder/p147r047_7k19991114_z43_nn62.TIF":
	#	imgarray-=1.0
	#	imgarray*=12.65
	#	imgarray/=254.0
	#	imgarray+=3.2
	#elif filename=="2011folder/LT51470472011039KHC00_B70.TIF":
	#	imgarray-=1.0
	#	imgarray*=10.8
	#	imgarray/=254.0
	#	imgarray+=-0.35
	else :
		print "Not a valid filename"
	return imgarray
#reshaping image to reqd area , changed method from image.open and getdata()
#it read data in a row which was beneficial at first but we need not process the entire image since the desired region is only rougly 3k *3k pixels
#more pixels such as 8k * 8k takes a lot of time to process , this method is better in terms of speed
def imgcrop(filename,verbose=False):
	img=misc.imread(filename)#reading the image file
	img=np.asfarray(img)#importing it as a float numpy array
	#print img.dtype
	height,width = img.shape   # Get dimensions for checking purposes only
	#print img.shape
	img_new = img[2922:5922,2226:5226] #reshape to desired row and column
	#print img_new
    
	#print img_new.shape
	return img_new
		
#converting image to a flat numpy matrix of radiance values
def image_to_matrix(filename, verbose=False):
	img_new=imgcrop(filename)#get resized image
	#img_new.show()
	#img_new = np.array(img_new.getdata(),dtype=np.float)
	print img_new.shape #for checking purpose
	print img_new.max() #for checking purpose
	s=img_new.shape[0] * img_new.shape[1] #converting into a flat array
	img_new = img_new.reshape(s,1) #reshaped into a flat array#not: more like vertically or column array instead of flat
	#print img_wide.shape
	#img=np.array([img_wide],dtype=np.float)
	#img=img.reshape(s,1)
	#print img_new
	#img_new = img_new.reshape(4358,3574)
	#imgplot=plt.imshow(img_new)
	#imgplot.set_cmap('spectral')
	#plt.show()
	img_new=radiance(filename,img_new) #changing the DN values with radiance value
	y=img_new.min()
	img_new-=(y*0.7) 
	print img_new.max()
	return img_new
#imgarray=image_to_matrix("2011/LT51470472011039KHC00_B1.TIF",False) #creating the flat array of first band image
#appending different bands of the image into one array
def img_append(filename,imgarray):
	imgarray = np.hstack((imgarray,image_to_matrix(filename)))
	print imgarray.shape
	return imgarray
imgarray=np.array([]).reshape(9000000,0)
#add loop for input image later for large no of images for eg: in case of hyperspectral image

foldername=raw_input("Give foldername: ")
#foldername="2011"
for count in [1,2,3,4,5,7]:
	for file in os.listdir("%s/"%(foldername)):
		if file.endswith(".TIF"):
			if int(file[23])==count:
				imgarray=img_append("%s/%s"%(foldername,file),imgarray)

#imgarray=img_append("2011/LT51470472011039KHC00_B1.TIF",imgarray)
#imgarray=img_append("2011/LT51470472011039KHC00_B2.TIF",imgarray) #appending band 2 to imgarray
#imgarray=img_append("2011/LT51470472011039KHC00_B3.TIF",imgarray) #appending band 3 to imgarray
#imgarray=img_append("2011/LT51470472011039KHC00_B4.TIF",imgarray) #appending band 4 to imgarray
#imgarray=img_append("2011/LT51470472011039KHC00_B5.TIF",imgarray) #appending band 5 to imgarray
#imgarray=img_append("2011/LT51470472011039KHC00_B6.TIF",imgarray) #appending band 6 to imgarray
#imgarray=img_append("2011folder/p147r047_7k19991114_z43_nn61.TIF",imgarray)
#imgarray=img_append("2011folder/p147r047_7k19991114_z43_nn62.TIF",imgarray)
#imgarray=img_append("2011/LT51470472011039KHC00_B6.TIF",imgarray)
#imgarray=img_append("2011folder/p147r047_7p19991114_z43_nn80.TIF",imgarray)
# function to convert the image coordinates into equivalent list(flat array) coordinates generated after reading
def img_to_list(abs,ord):#abs and ord are the x and y of a pixel in the original size image without resizing
	img_new=imgcrop("2011/LT51470472011039KHC00_B1.TIF")
	height,width=img_new.shape #changed on tuesday from width, height..confusing assignment of x,y..while image manager shows xpixels * ypixels as shape,python .shape() function show ypixels*xpixels. Major logical rectification here.
	new_abs= (ord)*width +abs
	return new_abs
	
#y=np.random.randint(6,size=(16691140,))
#print y
#read csv file containing information of class and training and testing data
#a=np.loadtxt("/home/manush/Downloads/signatures_apr22_r2.csv",dtype=str,delimiter=',')
#print y


#print "this is y"
#print y_train
#declaring training and testing data
X_train=np.zeros((0,6)) #using vstack later on to append data to training and testing, the method is slow
X_test=np.zeros((0,6))
#y_train=np.zeros((0,),dtype="S20")
#y_test=np.zeros((0,),dtype="S20")
#y=np.zeros((0,),dtype="S20")
#reading data from csv file conating details about training and testing regions of pune
a=np.loadtxt("2011.csv",dtype=str,delimiter=',')
#def refvaluex(x):

#def refvaluey(y):


print imgarray.shape
count=0 #counting the number of elements in training set
count_=0 #counting the number of elements in testing set
for i in a : 
	y1=int(i[0])-2922 #correcting for resized image
	y2=int(i[1])-2922 #correcting for resized image
	x1=int(i[2])-2226 #correcting for resized image
	x2=int(i[3])-2226 #correcting for resized image
	
	if int(i[5])==1 : 
		count+=int(i[6]) #incrementing count with the number f pixels in each iteration
		print count
		label=i[4] #the classes to classify into
		print label
		for y in range (y1,y2+1): #second loop . traversing inside a rectangular region of data in image, therefore first loop for going through all the rectangles(training or testing area) and second for traversing thorugh rectangle
			#and storing it as flat array again 
			#print y
			x1_new=img_to_list(x1,y) #converting image coordinates to flat array or list coordinates, to create training and testing data set in the format reqd by scikit-learn
			x2_new=img_to_list(x2,y)
			#print x1_new
			#print x2_new
			X_train=np.vstack((X_train,imgarray[x1_new:x2_new+1,0:6])) #appending training data to training data set, later proved to be the most frustrating mistake as described below
			#reversed order of x_train and imgarray on tuesday because it was being stacked in front for every iteration rather than back
			#so rather than getting X[old,old,old..old.,new] was getting X[new,old,old,old]
	else : 
		count_+=int(i[6])
		label=i[4]
		print label
		for y in range (y1,y2+1):
			#print "yes"
			x1_new=img_to_list(x1,y)
			x2_new=img_to_list(x2,y)
			#print x1_new
			X_test=np.vstack((X_test,imgarray[x1_new:x2_new+1,0:6])) #appending testing data to testing data set
			#reversed order of x_train and imgarray on tuesday because it was being stacked in fron for every iteration rather than back
			#print X_test
	

#declaring target data set for training and testing 
#following scikit-learn and creating all types of datasets reqd.
#this flat array will contain all the pixels of training area with the value of classified label   
y_train=np.zeros((count,),dtype=int)
#this flat array will contain all the pixels of testing area with the value of classified label   
y_test=np.zeros((count_,),dtype=int)
z=0 #count for target set of training data
z_=0#count for target set of testing data
for i in a : #traversing thorugh the training and testing data again , this time for target set values, note using second loop because the method of appending data to 
	#0 sized numpy arrays is very slow(tested), therefore declaring target set with the reqd size in advance and replacing the values as desired has proved to be more than 100 times faster
	#look for similar solution for training and testing data set as well later
	y1=int(i[0])-2922
	y2=int(i[1])-2922
	x1=int(i[2])-2226
	x2=int(i[3])-2226
	
	if int(i[5])==1: #traversing through training area
		

		label=i[4]
		print label#checking purpose
		x1_new=img_to_list(x1,y1)
		x2_new=img_to_list(x2,y2)
		y_train[z:z+int(i[6]),]=label
		z+=int(i[6])	
		#print z
		#print x1_new
		#print "portion added"
		#print y_train
	else : 
		label=i[4]
		print label
		x1_new=img_to_list(x1,y1)
		x2_new=img_to_list(x2,y2)
		y_test[z_:z_+int(i[6]),]=label
		z_+=int(i[6])	
		#print z_
		#print x1_new
		#print "portion added"
	


#y_test=y_test.reshape(1466,1)
#X_train, X_test,y_train,y_test=train_test_split(imgarray,y,random_state=0)
print "X_train"
print X_train#check
print X_train.shape#check
print "X_test"
print X_test#check
print X_test.shape#check
print"y_train"
print y_train.shape#check
print "y_test"
print y_test.shape#check
#using gaussian naive_bayesive Byes classifier provided by scikit-learn
clf1=GaussianNB() #it most probably implements maximum likelihood classifier, yet to confirm this
clf1.fit(X_train,y_train) # this fits training data to target set values, seems kinda redundant because we already did it for scikit while making target set 
#but is included if we cud use test_train_split provided by scikit for random allotment of testing and training data in which case we wud not require the loops above to create all sets
#predicted labels for test data
#clf1=GaussianNB()
#clf1.fit(X_train,y_train)
#introducing more classifiers
clf2=svm.SVC(C=1000000.0,gamma=0.0001,kernel='rbf')
clf2.fit(X_train,y_train)
#clf3= neighbors.KNeighborsClassifier(15)
#clf3.fit(X_train,y_train)
y_pred1=clf1.predict(imgarray) #predicting target array for the whole resized image
y_pred_1=clf1.predict(X_test) #predicting target array for testing area only for making confusion matrix
print "y_pred1"
print y_pred1 #check
print y_pred1.shape #check
y_pred2=clf2.predict(imgarray)
y_pred_2=clf2.predict(X_test)
print "y_pred2"
print y_pred2 #check
print y_pred2.shape #check
#y_pred3=clf3.predict(imgarray)
#y_pred_3=clf3.predict(X_test)
#print "y_pred3"
#print y_pred3 #check
#print y_pred3.shape #check
#making confusion matrix from y_test and y_pred values
#cm1=confusion_matrix(y_test,y_pred_1)
#print cm1
#plot cm as a colour legend matrix
#cm2=confusion_matrix(y_test,y_pred_2)
#print cm2
#cm3=confusion_matrix(y_test,y_pred_3)
#print cm3
#pl.matshow(cm1)
#pl.title('Confusion Matrix')
#pl.colorbar()
#pl.ylabel('True label')
#pl.xlabel('Predicted label')
#pl.show()

#pl.matshow(cm2)
#pl.title('Confusion Matrix')
#pl.colorbar()
#pl.ylabel('True label')
#pl.xlabel('Predicted label')
#pl.show()

#pl.matshow(cm3)
#pl.title('Confusion Matrix')
#pl.colorbar()
#pl.ylabel('True label')
#pl.xlabel('Predicted label')
#pl.show()
#using this to obtain shape of original resized image so that flat array of predicted array can be converted to image representation of thematic classification, at this point i have started wondering about using classes 
#since i have already called these functions before , it seems like calling them again and again is unncessary and preventable through a python class
im=imgcrop("2011/LT51470472011039KHC00_B1.TIF")

#below two steps might be unneseccary, check later
s=y_pred1.shape[0]
y1=y_pred1.reshape(s,1)
y1=y_pred1.reshape(im.shape[0],im.shape[1])
print y1 #check
#plotting the thematic classified image
imgplot1=plt.imshow(y1)
#imgplot.set_cmap('spectral')
plt.colorbar() #for showing the color legend
plt.show() #for showing image



s=y_pred2.shape[0]
y2=y_pred2.reshape(s,1)
y2=y_pred2.reshape(im.shape[0],im.shape[1])
print y2 #check
#plotting the thematic classified image
imgplot2=plt.imshow(y2)
#imgplot.set_cmap('spectral')
plt.colorbar() #for showing the color legend
plt.show() #for showing image




#s=y_pred3.shape[0]
#y3=y_pred3.reshape(s,1)
#y3=y_pred3.reshape(im.shape[0],im.shape[1])
#print y3 #check
#plotting the thematic classified image
#imgplot3=plt.imshow(y3)
#imgplot.set_cmap('spectral')
#plt.colorbar() #for showing the color legend
#plt.show() #for showing image










































































