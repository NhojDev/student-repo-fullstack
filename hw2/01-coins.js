/** Exercise 01 - Coins **/

// Add your function here 

function calculateChange(amount) {
    let cents = Math.round(amount * 100)
    if (cents > 10000) 
        return "Error: the number is too large";
    if (cents < 0) 
        return "Error: the number is negative";
    if (cents < 0 || isNaN(cents)) {
        return "Error: invalid amount";
    }

    const dollars = Math.floor(cents / 100);
    cents %= 100;

    const quarters = Math.floor(cents / 25);
    cents %= 25;

    const dimes = Math.floor(cents / 10);
    cents %= 10;

    const nickels = Math.floor(cents / 5);
    cents %= 5;

    const pennies = cents;

    return `${dollars} dollars, ${quarters} quarters, ${dimes} dimes, ${nickels} nickels, ${pennies} pennies`;
}


// Sample test cases
console.log(calculateChange(4.62));
// $4.62 ==> 4 dollars, 2 quarters, 1 dime, 2 pennies
console.log(calculateChange(0.16));
// $0.16 ==> 1 dime, 1 nickel, 1 penny
console.log(calculateChange(150.11));
// $150.11 ==> Error: the number is too large

// Add additional test cases here 
console.log(calculateChange(12.34));
console.log(calculateChange(5.67));
console.log(calculateChange(1.41));
console.log(calculateChange(0.99));
console.log(calculateChange(-34.99));
console.log(calculateChange("hello"));