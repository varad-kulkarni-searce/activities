// 0 1 0 2 1 0 1 3 2 1 2 1
//ans => 6



let waterTrap = function (height) {
    let trappedWater = 0, n = height.length;

    //creating left array to indicate/ check the maximum height at left of the given index.
    let left = new Array(n);

    //creating left array to indicate/ check the maximum height at right of the given index.
    let right = new Array(n);

    left[0] = height[0];
    //transversing and filling left array..
    for (let i = 1; i < n; i++)
        left[i] = Math.max(left[i - 1], height[i]);

    right[n - 1] = height[n - 1];
    //transversing and filling right array..
    for (let i = n - 2; i >= 0; i--)
        right[i] = Math.max(right[i + 1], height[i]);

    //summing up the trappedWater with the logic of finding minimum of left and right and substracting height from the same.
    for (let i = 0; i < n; i++)
        trappedWater += (Math.min(left[i], right[i]) - height[i]);

    return trappedWater;
}

console.log("Water trapped in [0,1,0,2,1,0,1,3,2,1,2,1]: ", waterTrap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]));
console.log("Water trapped in [4,2,0,3,2,5]: ", waterTrap([4, 2, 0, 3, 2, 5]));

