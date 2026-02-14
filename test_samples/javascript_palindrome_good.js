/**
 * Palindrome Checker
 * 
 * Problem Statement:
 * Determine if a given string is a palindrome. A palindrome reads the same 
 * forward and backward, ignoring spaces, punctuation, and case.
 * 
 * Examples:
 *   "racecar" -> true
 *   "A man a plan a canal Panama" -> true
 *   "hello" -> false
 */

/**
 * Check if a string is a palindrome
 * @param {string} str - The string to check
 * @returns {boolean} True if palindrome, false otherwise
 */
function isPalindrome(str) {
    if (!str || typeof str !== 'string') {
        throw new TypeError('Input must be a non-empty string');
    }
    
    // Remove non-alphanumeric characters and convert to lowercase
    const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    
    // Compare with reversed string
    const reversed = cleaned.split('').reverse().join('');
    
    return cleaned === reversed;
}

/**
 * Check palindrome using two-pointer technique (more efficient)
 * @param {string} str - The string to check
 * @returns {boolean} True if palindrome, false otherwise
 */
function isPalindromeTwoPointer(str) {
    if (!str || typeof str !== 'string') {
        throw new TypeError('Input must be a non-empty string');
    }
    
    const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    
    let left = 0;
    let right = cleaned.length - 1;
    
    while (left < right) {
        if (cleaned[left] !== cleaned[right]) {
            return false;
        }
        left++;
        right--;
    }
    
    return true;
}

// Test cases
const testCases = [
    { input: "racecar", expected: true },
    { input: "A man a plan a canal Panama", expected: true },
    { input: "hello", expected: false },
    { input: "Was it a car or a cat I saw?", expected: true },
    { input: "Madam", expected: true },
    { input: "12321", expected: true },
    { input: "12345", expected: false }
];

console.log("Palindrome Checker Tests\n" + "=".repeat(50));

testCases.forEach(({ input, expected }) => {
    const result1 = isPalindrome(input);
    const result2 = isPalindromeTwoPointer(input);
    const status = (result1 === expected && result2 === expected) ? "✓" : "✗";
    console.log(`${status} "${input}" -> ${result1} (expected: ${expected})`);
});

console.log("\nAll tests completed!");
