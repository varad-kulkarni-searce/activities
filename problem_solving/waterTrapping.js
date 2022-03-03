// 0 1 0 2 1 0 1 3 2 1 2 1
//ans => 6

let arr = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1];

let waterTrap = function (height) {
    let trappedWater = 0, n = height.length;
    let left = new Array(n), right = new Array(n);
    left[0] = height[0];
    for (let i = 1; i < n; i++)
        left[i] = Math.max(left[i - 1], height[i]);
    right[n - 1] = height[n - 1];
    for (let i = n - 2; i >= 0; i--)
        right[i] = Math.max(right[i + 1], height[i]);

    for (let i = 0; i < n; i++)
        trappedWater += (Math.min(left[i], right[i]) - height[i]);

    return trappedWater;
}

console.log("Water trapped in [0,1,0,2,1,0,1,3,2,1,2,1]: ", waterTrap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]));
