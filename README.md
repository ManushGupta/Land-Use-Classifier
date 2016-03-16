# Land-Use-Classifier

This python app was developed to classify land use into various sub categories of vegetation, soil , impervious surface etc. 

The classifiers used were SVM Classifier with the 'rbf' kernel, Naive Bayes and the Nearest Neighbor.

It was found that SVM classified most accurately, differently followed by both Bayes and Nearest Neighbour

Confusion Matrix for a sample image : 

                               quarry     Plains      Water   residential  vegetation  User's Accuracy
                                  0           0         0            0            0          0
                                311         563         0            2            0         65%
                                  0           0       138            0            2         98.57%
                                 14           0         0          126            0         90%
                                  0           0         0            5          305         98.38%
             Producer's accuracy 0%         100%       100%        94.7%      99.38%
             
  The producer accuracy is a measure indicating the probability that the classifier has labeled an image pixel into Class A given that the ground truth is Class A

  User accuracy is a measure indicating the probability that a pixel is Class A given that the classifier has labeled the pixel into Class A
  
  example input image:
  
  ![alt tag](/landsatpune.png)

  corresponding output svm image :
  
  ![alt tag](/svmresult.png)
  
  The brown area is the impervious region, identified as concrete and the dark blue is water. 
  
  Comparison between SVM and Naive Bayes:
  
  ![alt tag](/compare.png)
  
  note: the color legend is different. The green is concrete and the light blue is water in this one.
