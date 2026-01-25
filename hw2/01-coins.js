/** Exercise 01 - Coins **/

// Add your function here 

function calculateChange(amount) {
    let cents = Math.round(amount * 100)
    if (cents > 10000) 
        return "Error: the number is too large";
    let dollars = 0;
    let quarters = 0;
    let dimes = 0;
    let nickels = 0;
    let pennies = 0;
    while (cents > 0) {
        if (cents >= 100) {
            cents -= 100;
            dollars += 1;
        }
        else if (cents >= 25) {
            cents -= 25;
            quarters += 1;
        }
        else if (cents >= 10) {
            cents -= 10;
            dimes += 1;
        }
        else if (cents >= 5) {
            cents -= 5;
            nickels += 1;
        }
        else if (cents >= 1) {
            cents -= 1;
            pennies += 1;
        }
    }
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
