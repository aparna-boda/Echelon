/**
 * Binary Search Implementation
 * 
 * Problem Statement:
 * Implement binary search to find the index of a target value in a sorted array.
 * Return -1 if the target is not found.
 * 
 * Time Complexity: O(log n)
 * Space Complexity: O(1) for iterative, O(log n) for recursive
 */

public class BinarySearch {
    
    /**
     * Iterative binary search implementation
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @return Index of target, or -1 if not found
     */
    public static int binarySearchIterative(int[] arr, int target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }
        
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            // Avoid integer overflow
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * Recursive binary search implementation
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @param left Left boundary index
     * @param right Right boundary index
     * @return Index of target, or -1 if not found
     */
    public static int binarySearchRecursive(int[] arr, int target, int left, int right) {
        if (left > right) {
            return -1;
        }
        
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            return binarySearchRecursive(arr, target, mid + 1, right);
        } else {
            return binarySearchRecursive(arr, target, left, mid - 1);
        }
    }
    
    /**
     * Public wrapper for recursive binary search
     * @param arr Sorted array of integers
     * @param target Value to search for
     * @return Index of target, or -1 if not found
     */
    public static int binarySearchRecursive(int[] arr, int target) {
        if (arr == null || arr.length == 0) {
            return -1;
        }
        return binarySearchRecursive(arr, target, 0, arr.length - 1);
    }
    
    /**
     * Test helper method
     */
    private static void runTest(int[] arr, int target, int expected) {
        int resultIter = binarySearchIterative(arr, target);
        int resultRec = binarySearchRecursive(arr, target);
        
        boolean passedIter = resultIter == expected;
        boolean passedRec = resultRec == expected;
        
        String status = (passedIter && passedRec) ? "✓" : "✗";
        
        System.out.printf("%s Search for %d: Iterative=%d, Recursive=%d (Expected: %d)%n",
                          status, target, resultIter, resultRec, expected);
    }
    
    /**
     * Main method with test cases
     */
    public static void main(String[] args) {
        System.out.println("Binary Search Tests");
        System.out.println("=".repeat(60));
        
        // Test Case 1: Normal case
        System.out.println("\nTest 1: [1, 3, 5, 7, 9, 11, 13, 15]");
        int[] arr1 = {1, 3, 5, 7, 9, 11, 13, 15};
        runTest(arr1, 7, 3);
        runTest(arr1, 1, 0);
        runTest(arr1, 15, 7);
        runTest(arr1, 6, -1);
        
        // Test Case 2: Single element
        System.out.println("\nTest 2: [5]");
        int[] arr2 = {5};
        runTest(arr2, 5, 0);
        runTest(arr2, 3, -1);
        
        // Test Case 3: Two elements
        System.out.println("\nTest 3: [2, 4]");
        int[] arr3 = {2, 4};
        runTest(arr3, 2, 0);
        runTest(arr3, 4, 1);
        runTest(arr3, 3, -1);
        
        // Test Case 4: Large array
        System.out.println("\nTest 4: Large array [0, 2, 4, ..., 198]");
        int[] arr4 = new int[100];
        for (int i = 0; i < 100; i++) {
            arr4[i] = i * 2;
        }
        runTest(arr4, 100, 50);
        runTest(arr4, 0, 0);
        runTest(arr4, 198, 99);
        runTest(arr4, 101, -1);
        
        System.out.println("\nAll tests completed!");
    }
}
