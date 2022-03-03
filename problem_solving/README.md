<h3>Water Trapped Problem</h3>
<h4>Approach / steps:</h4><br>
1. Create two arrays left and right of size n. <br>left array -> To indicate/ check the maximum height at left of the given index.<br>right array -> To indicate/ check the maximum height at right of the given index.
<br><br>2. Transverse from start (i=1).
<br>3. Fill the left[i] with the logic of finding maximun height towards left of the current index.
<br><br>4. Transverse from last (i=n-2).
<br>5. Fill the right[i] with the logic of finding maximun height towards right of the current index.
<br><br>6. sum up the trappedWater with the logic of finding minimum of left and right and substracting height from the same.<br>(min(left[i], right[i]) - height[i])
    <br><br>
    <img width="1440" alt="waterTrapping output" src="https://user-images.githubusercontent.com/98943187/156616359-b50dee70-f451-480f-b825-931843ce651b.png">
