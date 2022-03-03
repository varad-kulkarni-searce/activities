
//                               Getters and Setters...


// Theory: They are code constructs that help developers access and modify the properties of objects.


// We can create getters and setters in two different ways:

// 1 => with the get and set keywords,
// 2 => with the Object.defineProperty() method.



//Accessing properties using methods:

// var myCar = {
//     color: "blue",
//     company: "Toyota",

//     carColor: function () {
//         return this.color;
//     },
//     carCompany: function () {
//         return this.company;
//     }

// };

// console.log(myCar.carColor());    //blue
// console.log(myCar.carCompany());    //Toyota.



/*-------------------------------------------------------------------------------*/


//1. Using get and set keywords...


// //get 

// var myCar = {
//     /* Data properties */
//     color: "blue",
//     company: "Toyota",

//     /* Accessor properties (getters) */
//     get carColor() {
//         return this.color;
//     },
//     get carCompany() {
//         return this.company;
//     },
//     carCompany2: function () {
//         return this.company;
//     }
// };

// /* Calling the getter accessor properties */

// //accessing value as a property..
// console.log(myCar.carColor);                   // blue

// //accessing the value as a method
// console.log(myCar.carColor());                 //error..


// console.log(myCar.carCompany);                  // Toyota
// console.log(myCar.carCompany());                 //error..

// console.log(myCar.carCompany2());                   //Toyota



//set 

// var myCar = {
//     /* Data properties */
//     color: "blue",
//     company: "Toyota",

//     /* Accessor properties (getters) */
//     get carColor() {
//         return this.color;
//     },
//     get carCompany() {
//         return this.company;
//     },

//     /* Accessor properties (setters) */
//     set carColor(newColor) {
//         this.color = newColor;
//     },
//     set carCompany(newCompany) {
//         this.company = newCompany;
//     }
// };

// /* Calling the setter accessor properties */
// myCar.carColor = "red";
// myCar.carCompany = "BMW";

// /* Checking the new values with the getter accessor properties */
// console.log(myCar.carColor);          // red

// console.log(myCar.carCompany);     // BMW


/*----------------------------------------------------------------------------------------------*/


//2. Using the Object.defineProperty() method.

// // /* Original object*/
// var myCar = {
//     color: "blue",
//     company: "Toyota"
// };

// // // Syntax: Object.defineProperty(obj, prop, descriptor)

// // /* Adding a getter and setter to color */
// Object.defineProperty(myCar, "carColor", {
//     get: function () {
//         return this.color;
//     },
//     set: function (newColor) {
//         this.color = newColor;
//     },
// });

// /* Adding a getter and setter to defCompany */
// Object.defineProperty(myCar, "carCompany", {
//     get: function () {
//         return this.company;
//     },
//     set: function (newCompany) {
//         this.company = newCompany;
//     }
// });

// /* Checking the value of the properties with the getters */
// console.log(myCar.carColor);       // blue

// console.log(myCar.carCompany);     // Toyota


// /* Modifying the values with the setters */
// myCar.carColor = "red";
// myCar.carCompany = "BMW";


// /* Checking the modified properties with the getters */
// console.log(myCar.carColor);       // red

// console.log(myCar.carCompany);     // BMW


/*----------------------------------------------------------------------------------*/

// //Smart Getters and Setters..(creating safer codes..)

// var car = {
//     get carFuel() {
//         return this.fuel;
//     },

//     set carFuel(value) {
//         if (value > 300) {
//             console.log("Fuel Tank Capacity Exceeded..");
//         }
//         else {
//             this.fuel = value;
//         }
//     }
// };

// car.carFuel = "200";
// console.log(car.carFuel);     // 200

// car.carFuel = "500";

/*----------------------------------------------------------------------------------------*/


// Read only/ Write only properties...
// Only getter => Read only
// Only setter => Write only


//1. Read only..

// var car = {

//     color: "blue",

//     get carColor() {
//         return this.color;
//     },

// };

// console.log(car.carColor);         //blue  

// car.carColor = "red";
// console.log(car.carColor);         //blue


//2. Write only..

// var car = {

//     color: "blue",

//     set carColor(value) {
//         this.color = value
//     },

// };

// console.log(car.carColor);     //undefined

// car.carColor = "red";
// console.log(car.carColor);     //undefined

// console.log(car.color);      //red

/*---------------------------------------------------------------*/

//Getter has higher precedence...

// const person = {
//     name: 'Bill Gates',
//     get name() {
//         return 'Jeff Bezos';
//     }
// };

// console.log(person.name)     //Jeff Bezos


// const person = {
//     name: 'Bill Gates',
//     get name() {
//         return this.name;
//     }
// };

// console.log(person.name)        //Uncaught RangeError: Maximum call stack size exceeded


/*------------------------------------------------------------------*/


//Most common use cases:
//1. Securing access to data properties
//2. Adding extra logic to properties before getting or setting their values.

