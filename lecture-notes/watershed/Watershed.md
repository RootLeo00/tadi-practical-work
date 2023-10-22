This is a geographical analogy.
In the below image you can see the watershed line that is the line where a drop a water would go toward on steep or the other. 

![[images/Pasted image 20231013183226.png]]

If we have a gray level function we can easily find the 2 regional minima. A drop of water in the two maxima would go down to the catching basin (the regional minima) filling the catching basin. After you fill both the catching basin, the water in the two of them would reach the top and they merge. The line where the water merge is called watershed and it is a **continuous line**. 

![[Pasted image 20231013183318.png]]
![[Pasted image 20231013183329.png]]

Watershed is important for segmentation because the typical problem that we have in edge detection is that we get segments on the edges but it is really difficult to have closed lines. With watershed this problem is solved by the definition itself.

Looking at the image below we can understand that if we look locally to find watersheds, then we have several choices of watershed that we could get.  If we do only local tests we would have several watershed choices in a single image :( 

![[Pasted image 20231013183342.png]]

So lets do it more globally. We can compute the distance from a point of the image to a minimum and then we will choose the smallest one.
Define the **steepest descent** of a point x, which is still a local measure. We compute difference of the y point between the function value of the x point (where we are) and the function value of the y point (where we want to go), in respect to the distance between the two points. We compute this for each possible y point and the max value we obtain will be our steepest descent of the x point. 
Note: the value of a point x in our case is interpreted as the "high" of the point.

![[Pasted image 20231013183357.png]]

We define the ramp of the path: we compute the local cost at each step in a path that goes from a point x1 to a second point xn.

![[Pasted image 20231013183411.png]]

The local cost is defined as:

![[Pasted image 20231013183421.png]]

Then the topographic distance would be the min cost of all the paths going from a point to another. 

![[Pasted image 20231013183432.png]]

This distance would be 0 to a plateau: imagine when you go to trekking. If you want to go from the valley to the top you go either always up, or you can find a path that would have some flat part but the amount of "work" (appropriate here) is the same.

IMAGE DRAW


The catchment basin would be a  Von diagram using topographic distance instead of an euclidean distance. So the catching basin associated with one regional minimum would be all the points that are closest to this minimum according to the topographic distance, plus the minimum itself.

![[Pasted image 20231013183449.png]]

The reason we add the value of the minimum (so, the height of the min) is that we want it to be dependent to the height of the regional minimum.

Finally, the watershed is the complement of the catching basin, in the sense that the point that are equidistant from two catching basin will belong to the watershed line. 
![[Pasted image 20231013183512.png]]

![[Pasted image 20231013183902.png]]

With this definition the two local minimum of the previous image belong to the same watershed, an the interpretation of that is that they belong to the same crest.


There are algorithms that are much easier with computation:
Approach by immersion: we start flooding the catching basins and when the water of two catching basins merge, that means when two connected components merge, then we have a watershed line. Watershed line = point where two catching basins merge

![[Pasted image 20231013183728.png]]

![[Pasted image 20231013183743.png]]![[Pasted image 20231013183754.png]]![[Pasted image 20231013183804.png]]![[Pasted image 20231013183812.png]]
We can apply this to a gradient image. With gradient image we have homogeneous objects as minima, while we have higher pixel value (white) that represents the maxima.
This gradient image is very noisy and as soon as we have a small variation we will have  a regional minima, thus computing the watershed we will get a noisy segmentation with many many regions (oversegmentation). 

![[Pasted image 20231013183942.png]]

Several methods to avoid this:
- filter the image -> but not too much 
- filter the gradient image -> remove small minima to get more large minima -> closing
- group adjacent region --> let's say we could group regions that have a really small gradient we you go from the first to the second, or if they have a similar gray level
- we select minima that are deep enough 
- we focus on specific objects --> we impose markers (regional minima) + reconstruction --> in the other parts of the markers the minima will be flattened. This is done by selecting the the marker (in blue)  and a condition and then apply reconstruction by performing successive erosion conditionally to the condition until convergence. 
Note: the marker should be completely inside the region we want to segment or completely outside, no in the middle!

![[Pasted image 20231013184004.png]] 
![[Pasted image 20231013184019.png]]
Another application (less famous) is show by this example. We want to separate the coffe beans. We compute the watershed on the inverted distance map of the object. We invert the distance to make the minimum become a crest line. With other operations then we can finally separated objects that are connected to each other!

![[Pasted image 20231013184039.png]]

So far we have achieved these goals:
- simplicity in computation
- good fidelty = respecting the contorurs of the image
But we want to achieve also regularization of the shape.
There are several methods:
- apply closing
- (watersnakes) consider the function we want to minimize (the topographic distance) considering it as an energy function
![[Pasted image 20231013184101.png]]
	For instance if you want to have regular contour you can achieve it by minimizing the length of the contour 
	![[Pasted image 20231013184157.png]]
	