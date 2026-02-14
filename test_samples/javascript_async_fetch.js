/**
 * Async/Await API Data Fetching
 * 
 * Problem Statement:
 * Implement functions to fetch data from APIs using modern async/await patterns.
 * Demonstrate error handling, parallel requests, and sequential operations.
 * 
 * This showcases modern JavaScript async patterns and best practices.
 */

/**
 * Simulated API call that returns a promise
 * @param {string} endpoint - API endpoint to fetch
 * @param {number} delay - Simulated delay in milliseconds
 * @returns {Promise<object>} Response data
 */
function simulateAPICall(endpoint, delay = 1000) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simulate occasional failures
            if (Math.random() < 0.1) {
                reject(new Error(`Failed to fetch ${endpoint}`));
            } else {
                resolve({
                    endpoint,
                    data: `Data from ${endpoint}`,
                    timestamp: new Date().toISOString()
                });
            }
        }, delay);
    });
}

/**
 * Fetch single resource with error handling
 * @param {string} endpoint - API endpoint
 * @returns {Promise<object|null>} Response data or null on error
 */
async function fetchResource(endpoint) {
    try {
        console.log(`Fetching ${endpoint}...`);
        const response = await simulateAPICall(endpoint, 500);
        console.log(`✓ Successfully fetched ${endpoint}`);
        return response;
    } catch (error) {
        console.error(`✗ Error fetching ${endpoint}:`, error.message);
        return null;
    }
}

/**
 * Fetch multiple resources sequentially
 * @param {string[]} endpoints - Array of endpoints
 * @returns {Promise<object[]>} Array of responses
 */
async function fetchSequential(endpoints) {
    const results = [];
    
    for (const endpoint of endpoints) {
        const result = await fetchResource(endpoint);
        if (result) {
            results.push(result);
        }
    }
    
    return results;
}

/**
 * Fetch multiple resources in parallel
 * @param {string[]} endpoints - Array of endpoints
 * @returns {Promise<object[]>} Array of responses
 */
async function fetchParallel(endpoints) {
    const promises = endpoints.map(endpoint => fetchResource(endpoint));
    const results = await Promise.all(promises);
    
    // Filter out null values (failed requests)
    return results.filter(result => result !== null);
}

/**
 * Fetch with timeout
 * @param {string} endpoint - API endpoint
 * @param {number} timeout - Timeout in milliseconds
 * @returns {Promise<object>} Response data
 * @throws {Error} If request times out
 */
async function fetchWithTimeout(endpoint, timeout = 3000) {
    const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Request timeout')), timeout);
    });
    
    const fetchPromise = simulateAPICall(endpoint, 500);
    
    try {
        return await Promise.race([fetchPromise, timeoutPromise]);
    } catch (error) {
        console.error(`✗ ${endpoint} failed:`, error.message);
        throw error;
    }
}

/**
 * Fetch with retry logic
 * @param {string} endpoint - API endpoint
 * @param {number} maxRetries - Maximum number of retry attempts
 * @returns {Promise<object>} Response data
 */
async function fetchWithRetry(endpoint, maxRetries = 3) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            console.log(`Attempt ${attempt}/${maxRetries} for ${endpoint}`);
            return await simulateAPICall(endpoint, 300);
        } catch (error) {
            lastError = error;
            console.log(`Attempt ${attempt} failed, retrying...`);
            
            if (attempt < maxRetries) {
                // Exponential backoff
                await new Promise(resolve => 
                    setTimeout(resolve, Math.pow(2, attempt) * 100)
                );
            }
        }
    }
    
    throw new Error(
        `Failed after ${maxRetries} attempts: ${lastError.message}`
    );
}

/**
 * Fetch with caching
 */
class APICache {
    constructor(ttl = 5000) {
        this.cache = new Map();
        this.ttl = ttl; // Time to live in milliseconds
    }
    
    /**
     * Get cached data or fetch new
     * @param {string} endpoint - API endpoint
     * @returns {Promise<object>} Response data
     */
    async get(endpoint) {
        const cached = this.cache.get(endpoint);
        
        if (cached && Date.now() - cached.timestamp < this.ttl) {
            console.log(`✓ Cache hit for ${endpoint}`);
            return cached.data;
        }
        
        console.log(`Cache miss for ${endpoint}, fetching...`);
        const data = await simulateAPICall(endpoint, 500);
        
        this.cache.set(endpoint, {
            data,
            timestamp: Date.now()
        });
        
        return data;
    }
    
    /**
     * Clear cache
     */
    clear() {
        this.cache.clear();
    }
    
    /**
     * Get cache size
     */
    size() {
        return this.cache.size;
    }
}

/**
 * Run test suite
 */
async function runTests() {
    console.log("Async/Await API Fetching Tests");
    console.log("=".repeat(70));
    
    // Test 1: Single fetch
    console.log("\nTest 1: Single Resource Fetch");
    await fetchResource("/api/users");
    
    // Test 2: Sequential fetching
    console.log("\nTest 2: Sequential Fetching");
    const startSeq = Date.now();
    const sequentialResults = await fetchSequential([
        "/api/users",
        "/api/posts",
        "/api/comments"
    ]);
    const seqTime = Date.now() - startSeq;
    console.log(`Sequential fetch completed in ${seqTime}ms`);
    console.log(`Fetched ${sequentialResults.length} resources`);
    
    // Test 3: Parallel fetching
    console.log("\nTest 3: Parallel Fetching");
    const startPar = Date.now();
    const parallelResults = await fetchParallel([
        "/api/users",
        "/api/posts",
        "/api/comments"
    ]);
    const parTime = Date.now() - startPar;
    console.log(`Parallel fetch completed in ${parTime}ms`);
    console.log(`Fetched ${parallelResults.length} resources`);
    console.log(`Speed improvement: ${(seqTime / parTime).toFixed(2)}x`);
    
    // Test 4: Fetch with timeout
    console.log("\nTest 4: Fetch with Timeout");
    try {
        await fetchWithTimeout("/api/slow", 2000);
    } catch (error) {
        console.log(`Handled timeout: ${error.message}`);
    }
    
    // Test 5: Fetch with retry
    console.log("\nTest 5: Fetch with Retry");
    try {
        const retryResult = await fetchWithRetry("/api/unreliable", 3);
        console.log(`✓ Retry successful:`, retryResult.endpoint);
    } catch (error) {
        console.log(`All retries failed: ${error.message}`);
    }
    
    // Test 6: Caching
    console.log("\nTest 6: API Caching");
    const cache = new APICache(3000);
    
    await cache.get("/api/cached");
    await cache.get("/api/cached"); // Should hit cache
    await cache.get("/api/cached"); // Should hit cache
    console.log(`Cache size: ${cache.size()}`);
    
    console.log("\nAll tests completed!");
}

// Run tests if this is the main module
if (typeof require !== 'undefined' && require.main === module) {
    runTests().catch(console.error);
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchResource,
        fetchSequential,
        fetchParallel,
        fetchWithTimeout,
        fetchWithRetry,
        APICache
    };
}
