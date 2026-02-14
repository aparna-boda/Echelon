/*
Concurrent Array Sum using Goroutines

Problem Statement:
Calculate the sum of a large array using concurrent goroutines.
Demonstrate proper use of channels, goroutines, and synchronization.

This showcases Go's concurrency features and efficient parallel processing.
*/

package main

import (
	"fmt"
	"sync"
	"time"
)

// sumPortion calculates sum of a portion of the array
func sumPortion(arr []int, start, end int, result chan<- int) {
	sum := 0
	for i := start; i < end; i++ {
		sum += arr[i]
	}
	result <- sum
}

// concurrentSum calculates array sum using multiple goroutines
func concurrentSum(arr []int, numGoroutines int) int {
	length := len(arr)
	if length == 0 {
		return 0
	}

	// Adjust number of goroutines if array is small
	if numGoroutines > length {
		numGoroutines = length
	}

	result := make(chan int, numGoroutines)
	portionSize := length / numGoroutines

	// Launch goroutines
	for i := 0; i < numGoroutines; i++ {
		start := i * portionSize
		end := start + portionSize
		
		// Last goroutine handles remaining elements
		if i == numGoroutines-1 {
			end = length
		}
		
		go sumPortion(arr, start, end, result)
	}

	// Collect results
	totalSum := 0
	for i := 0; i < numGoroutines; i++ {
		totalSum += <-result
	}

	close(result)
	return totalSum
}

// sequentialSum calculates array sum sequentially
func sequentialSum(arr []int) int {
	sum := 0
	for _, val := range arr {
		sum += val
	}
	return sum
}

// concurrentSumWithWaitGroup uses WaitGroup for synchronization
func concurrentSumWithWaitGroup(arr []int, numGoroutines int) int {
	length := len(arr)
	if length == 0 {
		return 0
	}

	if numGoroutines > length {
		numGoroutines = length
	}

	var wg sync.WaitGroup
	var mu sync.Mutex
	totalSum := 0
	portionSize := length / numGoroutines

	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		start := i * portionSize
		end := start + portionSize
		
		if i == numGoroutines-1 {
			end = length
		}

		go func(start, end int) {
			defer wg.Done()
			
			localSum := 0
			for j := start; j < end; j++ {
				localSum += arr[j]
			}
			
			mu.Lock()
			totalSum += localSum
			mu.Unlock()
		}(start, end)
	}

	wg.Wait()
	return totalSum
}

// benchmark measures execution time
func benchmark(name string, fn func() int) (int, time.Duration) {
	start := time.Now()
	result := fn()
	duration := time.Since(start)
	fmt.Printf("%-30s Result: %d, Time: %v\n", name, result, duration)
	return result, duration
}

func main() {
	fmt.Println("Concurrent Array Sum Tests")
	fmt.Println(string(make([]byte, 70)) + "\n")

	// Create test array
	size := 10_000_000
	arr := make([]int, size)
	for i := 0; i < size; i++ {
		arr[i] = i + 1
	}

	fmt.Printf("Array size: %d elements\n\n", size)

	// Test 1: Correctness with small array
	fmt.Println("Test 1: Correctness Test (small array)")
	smallArr := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	expectedSum := 55

	seqResult := sequentialSum(smallArr)
	concResult := concurrentSum(smallArr, 4)
	wgResult := concurrentSumWithWaitGroup(smallArr, 4)

	fmt.Printf("Expected: %d\n", expectedSum)
	fmt.Printf("Sequential: %d %s\n", seqResult, checkMark(seqResult == expectedSum))
	fmt.Printf("Concurrent (channels): %d %s\n", concResult, checkMark(concResult == expectedSum))
	fmt.Printf("Concurrent (WaitGroup): %d %s\n\n", wgResult, checkMark(wgResult == expectedSum))

	// Test 2: Performance comparison
	fmt.Println("Test 2: Performance Comparison (large array)")
	
	seqSum, seqTime := benchmark("Sequential Sum:", func() int {
		return sequentialSum(arr)
	})

	conc2Sum, conc2Time := benchmark("Concurrent Sum (2 goroutines):", func() int {
		return concurrentSum(arr, 2)
	})

	conc4Sum, conc4Time := benchmark("Concurrent Sum (4 goroutines):", func() int {
		return concurrentSum(arr, 4)
	})

	conc8Sum, conc8Time := benchmark("Concurrent Sum (8 goroutines):", func() int {
		return concurrentSum(arr, 8)
	})

	wgSum, wgTime := benchmark("Concurrent WaitGroup (4):", func() int {
		return concurrentSumWithWaitGroup(arr, 4)
	})

	// Verify all results match
	fmt.Println("\nVerification:")
	allMatch := (seqSum == conc2Sum) && (seqSum == conc4Sum) && 
	            (seqSum == conc8Sum) && (seqSum == wgSum)
	fmt.Printf("All results match: %s\n", checkMark(allMatch))

	// Speed improvements
	fmt.Println("\nSpeedup compared to sequential:")
	fmt.Printf("2 goroutines: %.2fx\n", float64(seqTime)/float64(conc2Time))
	fmt.Printf("4 goroutines: %.2fx\n", float64(seqTime)/float64(conc4Time))
	fmt.Printf("8 goroutines: %.2fx\n", float64(seqTime)/float64(conc8Time))
	fmt.Printf("WaitGroup:    %.2fx\n", float64(seqTime)/float64(wgTime))

	fmt.Println("\nAll tests completed!")
}

func checkMark(condition bool) string {
	if condition {
		return "✓"
	}
	return "✗"
}
