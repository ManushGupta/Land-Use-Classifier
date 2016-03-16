from PIL import Image
from scipy import misc
import scipy
import pylab as pl
import numpy as np
#from sklearn.naive_bayes import MultinomialNB
#from sklearn import datasets
#from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
	
#filename="easynamefolder/p147r047_7p19991114_z43_nn80.TIF"
STANDARD_SIZE=(3000,3000) #not working for larger sizes of the order of 17k*15k..giving memory error
#equivalent radiance values from DN values 
def radiance(filename,imgarray):
	if filename=="easyname/LT51470471999102XXX01_B1.TIF":
		imgarray-= 1.0
		imgarray*= 194.52
		imgarray/= 254.0
		imgarray+= -1.52
	elif filename=="easyname/LT51470471999102XXX01_B2.TIF":
		imgarray-=1.0
		imgarray*=367.84
		imgarray/=254.0
		imgarray+=-2.84
	elif filename=="easyname/LT51470471999102XXX01_B3.TIF":
		imgarray-=1.0
		imgarray*=265.17
		imgarray/=254.0
		imgarray+=-1.17
	elif filename=="easyname/LT51470471999102XXX01_B4.TIF":
		imgarray-=1.0
		imgarray*=222.51
		imgarray/=254.0
		imgarray+=-1.51
	elif filename=="easyname/LT51470471999102XXX01_B5.TIF":
		imgarray-=1.0
		imgarray*=30.57
		imgarray/=254.0
		imgarray+=-0.37
	elif filename=="easyname/LT51470471999102XXX01_B6.TIF":
		imgarray-=1.0
		imgarray*=14.065
		imgarray/=254.0
		imgarray+=1.238
	#elif filename=="easyname/LT51470471999102XXX01_B7.TIF":
	#	imgarray-=1.0
	#	imgarray*=17.04
	#	imgarray/=254.0
	#	imgarray+=-0.0
	#elif filename=="easynamefolder/p147r047_7k19991114_z43_nn62.TIF":
	#	imgarray-=1.0
	#	imgarray*=12.65
	#	imgarray/=254.0
	#	imgarray+=3.2
	#elif filename=="easynamefolder/LT51470471999102XXX01_B70.TIF":
	#	imgarray-=1.0
	#	imgarray*=10.8
	#	imgarray/=254.0
	#	imgarray+=-0.35
	else :
		print "Not a valid filename"
	return imgarray
#cropping image to reqd area #note: cannot use resize since i am already reading in 1 dimension from image #note: explore other reading methods for better access and less time
def imgcrop(filename,verbose=False):
	img=misc.imread(filename)
	img=np.asfarray(img)
	#print img.dtype
	height,width = img.shape   # Get dimensions
	#print img.shape
	img_new = img[2922:5886,2226:5100]
	#print img_new
    
	#print img_new.shape
	return img_new
		
#converting image to a flat numpy matrix of radiance values
def image_to_matrix(filename, verbose=False):
	img_new=imgcrop(filename)
	#img = img.resize(STANDARD_SIZE)
	#img_new.show()
	#img_new = np.array(img_new.getdata(),dtype=np.float)
	#img=img[6250000:25000000,]
	print img_new.shape
	print img_new.max()
	s=img_new.shape[0] * img_new.shape[1]
	img_new = img_new.reshape(s,1)
	#print img_wide.shape
	#img=np.array([img_wide],dtype=np.float)
	#img=img.reshape(s,1)
	#print img_new
	#img_new = img_new.reshape(4358,3574)
	#imgplot=plt.imshow(img_new)
	#imgplot.set_cmap('spectral')
	#plt.show()
	img_new=radiance(filename,img_new)
	print img_new.max()
	return img_new
imgarray=image_to_matrix("easyname/LT51470471999102XXX01_B1.TIF",False)
#appending different bands of the image into one array
def img_append(filename,imgarray):
	imgarray = np.hstack((imgarray,image_to_matrix(filename)))
	print imgarray.shape
	return imgarray
#add loop for input image later for large no of images for eg: in case of hyperspectral image
imgarray=img_append("easyname/LT51470471999102XXX01_B2.TIF",imgarray)
imgarray=img_append("easyname/LT51470471999102XXX01_B3.TIF",imgarray)
imgarray=img_append("easyname/LT51470471999102XXX01_B4.TIF",imgarray)
imgarray=img_append("easyname/LT51470471999102XXX01_B5.TIF",imgarray)
imgarray=img_append("easyname/LT51470471999102XXX01_B6.TIF",imgarray)
#imgarray=img_append("easynamefolder/p147r047_7k19991114_z43_nn61.TIF",imgarray)
#imgarray=img_append("easynamefolder/p147r047_7k19991114_z43_nn62.TIF",imgarray)
#imgarray=img_append("easyname/LT51470471999102XXX01_B6.TIF",imgarray)
#imgarray=img_append("easynamefolder/p147r047_7p19991114_z43_nn80.TIF",imgarray)
# function to convert the image coordinates into equivalent list coordinates generated after reading
def img_to_list(abs,ord):
	img_new=imgcrop("easyname/LT51470471999102XXX01_B1.TIF")
	height,width=img_new.shape #changed on tuesday from width, height..confusing assignment of x,y
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
X_train=np.zeros((0,6))
X_test=np.zeros((0,6))
#y_train=np.zeros((0,),dtype="S20")
#y_test=np.zeros((0,),dtype="S20")
#y=np.zeros((0,),dtype="S20")
a=np.loadtxt("classificationopt.csv",dtype=str,delimiter=',')
#def refvaluex(x):

#def refvaluey(y):


print imgarray.shape
count=0
count_=0
for i in a : 
	
	if int(i[5])==1: 
		count+=int(i[6])
		print count
		y1=int(i[0])-2922
		y2=int(i[1])-2922
		x1=int(i[2])-2226
		x2=int(i[3])-2226
		label=i[4]
		print label
		for y in range (y1,y2+1): 
			print y
			x1_new=img_to_list(x1,y)
			x2_new=img_to_list(x2,y)
			#print x1_new
			#print x2_new
			X_train=np.vstack((X_train,imgarray[x1_new:x2_new+1,0:6])) #reversed order of x_train and imgarray on tuesday because it was being stacked in front for every iteration rather than back
			#so rather than getting X[old,old,old..old.,new] wa getting X[new,old,old,old]
	else : 
		count_+=int(i[6])
		y1=int(i[0])-2922
		y2=int(i[1])-2922
		x1=int(i[2])-2226
		x2=int(i[3])-2226
		label=i[4]
		print label
		for y in range (y1,y2+1):
			print "yes"
			x1_new=img_to_list(x1,y)
			x2_new=img_to_list(x2,y)
			#print x1_new
			X_test=np.vstack((X_test,imgarray[x1_new:x2_new+1,0:6])) #reversed order of x_train and imgarray on tuesday because it was being stacked in fron for every iteration rather than back
			print X_test
	

   
y_train=np.zeros((count,),dtype=int)
y_test=np.zeros((count_,),dtype=int)
z=0
z_=0
for i in a : 
	
	if int(i[5])==1: 
		
		y1=int(i[0])-2922
		y2=int(i[1])-2922
		x1=int(i[2])-2226
		x2=int(i[3])-2226
		label=i[4]
		print label
		x1_new=img_to_list(x1,y1)
		x2_new=img_to_list(x2,y2)
		y_train[z:z+int(i[6]),]=label
		z+=int(i[6])	
		#print z
		#print x1_new
		#print "portion added"
		#print y_train
	else : 
		y1=int(i[0])-2922
		y2=int(i[1])-2922
		x1=int(i[2])-2226
		x2=int(i[3])-2226
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
print X_train
print X_train.shape
print "X_test"
print X_test.shape
print"y_train"
print y_train.shape
print "y_test"
print y_test.shape
#using gaussian naive_bayesive Byes classifier provided by skikit learn
clf=GaussianNB()
clf.fit(X_train,y_train)
#predicted labels for test data
#clf1=GaussianNB()
#clf1.fit(X_train,y_train)
y_pred=clf.predict(imgarray)
y_pred1=clf.predict(X_test)
print "y_pred"
print y_pred
print y_pred.shape

#making confusion matrix from y_test and y_pred values
cm=confusion_matrix(y_test,y_pred1)
print cm
#plot cm as a colour legend matrix

pl.matshow(cm)
pl.title('Confusion Matrix')
pl.colorbar()
pl.ylabel('True label')
pl.xlabel('Predicted label')
pl.show()
"""
print imgarray[3]
from sklearn.naive_bayes import MultinomialNB


#X=np.random.randint(5,size=(6,159900700))
#print X
y=np.array([1,2,3,4,5,6])
clf=MultinomialNB()
clf.fit(imgarray,y)
MultinomialNB(alpha=1.0,class_prior=None,fit_prior=True)
print(clf.predict(imgarray[2]))

"""
#def list_to_img(imgarray):
s=y_pred.shape[0]
y=y_pred.reshape(s,1)
y=y_pred.reshape(2964,2874)
print y
imgplot=plt.imshow(y)
#imgplot.set_cmap('spectral')
plt.colorbar()
plt.show()














































































