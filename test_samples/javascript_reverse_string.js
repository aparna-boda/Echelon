/**
 * String Reversal Implementations
 * 
 * Problem Statement:
 * Reverse a given string. Demonstrate multiple approaches.
 * 
 * Example: "hello" -> "olleh"
 */

/**
 * Reverse string using built-in methods (simplest)
 * @param {string} str - String to reverse
 * @returns {string} Reversed string
 */
function reverseStringBuiltIn(str) {
    return str.split('').reverse().join('');
}

/**
 * Reverse string using loop (manual approach)
 * @param {string} str - String to reverse
 * @returns {string} Reversed string
 */
function reverseStringLoop(str) {
    let reversed = '';
    for (let i = str.length - 1; i >= 0; i--) {
        reversed += str[i];
    }
    return reversed;
}

/**
 * Reverse string using recursion
 * @param {string} str - String to reverse
 * @returns {string} Reversed string
 */
function reverseStringRecursive(str) {
    if (str === '') {
        return '';
    }
    return reverseStringRecursive(str.substr(1)) + str.charAt(0);
}

/**
 * Reverse string using reduce
 * @param {string} str - String to reverse
 * @returns {string} Reversed string
 */
function reverseStringReduce(str) {
    return str.split('').reduce((reversed, char) => char + reversed, '');
}

/**
 * Reverse string in-place using array (modifying approach)
 * @param {string} str - String to reverse
 * @returns {string} Reversed string
 */
function reverseStringInPlace(str) {
    const arr = str.split('');
    let left = 0;
    let right = arr.length - 1;
    
    while (left < right) {
        // Swap characters
        [arr[left], arr[right]] = [arr[right], arr[left]];
        left++;
        right--;
    }
    
    return arr.join('');
}

// Benchmark function
function benchmark(fn, str, iterations = 10000) {
    const start = performance.now();
    for (let i = 0; i < iterations; i++) {
        fn(str);
    }
    const end = performance.now();
    return (end - start).toFixed(3);
}

// Test cases
const testStrings = [
    "hello",
    "JavaScript",
    "A man a plan a canal Panama",
    "12345",
    "racecar"
];

console.log("String Reversal Tests\n" + "=".repeat(70));

const methods = [
    { name: "Built-in", fn: reverseStringBuiltIn },
    { name: "Loop", fn: reverseStringLoop },
    { name: "Recursive", fn: reverseStringRecursive },
    { name: "Reduce", fn: reverseStringReduce },
    { name: "In-place", fn: reverseStringInPlace }
];

// Test correctness
console.log("\nCorrectness Tests:");
testStrings.forEach(str => {
    const expected = str.split('').reverse().join('');
    console.log(`\nInput: "${str}"`);
    
    methods.forEach(({ name, fn }) => {
        const result = fn(str);
        const status = result === expected ? "✓" : "✗";
        console.log(`  ${status} ${name.padEnd(12)}: "${result}"`);
    });
});

// Performance comparison
console.log("\n\nPerformance Comparison (10,000 iterations):");
const perfTestString = "The quick brown fox jumps over the lazy dog";
console.log(`Test string: "${perfTestString}"\n`);

methods.forEach(({ name, fn }) => {
    const time = benchmark(fn, perfTestString);
    console.log(`${name.padEnd(12)}: ${time}ms`);
});
