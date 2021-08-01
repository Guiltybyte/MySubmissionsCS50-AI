Started with a simple network, with a single convolution, pooling and hidden layer
each of which were using relu activation and a 50% dropout. This model achieved incredibly poor results
(around 0.05 each time)  
In an attempt to rectify this I added a second hidden layer, however this had no noticable impact on the
accuracy of the model (still around 0.05).

Next I decided to remove the second hidden layer (as I wanted to only change 1 thing from the original model
so I could better ascertain what single changes were having the greatest impact on the accuracy) and added
a second layer of convolution. The accuracy immediately improved with this change to ~ 0.94 .

Now that the network was very accurate I decided to re-add the second hidden layer. This actually seemed to slightly but
consistently reduce the accuracy of the model so I removed it again in favor of an extra pooling step, after the second
convolution layer. Using 2D Max pooling (predictably) reduced the accuracy a bit. However 2D average pooling seemed to
slightly increase accuracy and reduced the runtime of the program.

Finally I began experimenting with the various different types of activation functions. And found that for every layer
except the output, relu remained superior. For the output layer changing the activation function from softmax to sigmoid
resulted in a consistent increase in accuracy.  
Overall the changes made to the model result in an accuracy on the test set of about 0.97.  

The requested screencast video can be found [here](https://youtu.be/d2od2MtLMo4)
