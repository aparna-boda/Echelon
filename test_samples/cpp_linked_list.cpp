/**
 * Singly Linked List Implementation
 * 
 * Problem Statement:
 * Implement a singly linked list with basic operations:
 * - Insert at head
 * - Insert at tail
 * - Delete by value
 * - Search
 * - Display
 * 
 * Demonstrates proper memory management and OOP principles in C++.
 */

#include <iostream>
#include <memory>
#include <stdexcept>

/**
 * Node structure for linked list
 */
template<typename T>
struct Node {
    T data;
    std::shared_ptr<Node<T>> next;
    
    explicit Node(const T& value) : data(value), next(nullptr) {}
};

/**
 * Singly Linked List class
 */
template<typename T>
class LinkedList {
private:
    std::shared_ptr<Node<T>> head;
    size_t size;

public:
    /**
     * Constructor
     */
    LinkedList() : head(nullptr), size(0) {}
    
    /**
     * Insert element at the beginning of the list
     * Time Complexity: O(1)
     */
    void insertHead(const T& value) {
        auto newNode = std::make_shared<Node<T>>(value);
        newNode->next = head;
        head = newNode;
        size++;
    }
    
    /**
     * Insert element at the end of the list
     * Time Complexity: O(n)
     */
    void insertTail(const T& value) {
        auto newNode = std::make_shared<Node<T>>(value);
        
        if (!head) {
            head = newNode;
        } else {
            auto current = head;
            while (current->next) {
                current = current->next;
            }
            current->next = newNode;
        }
        size++;
    }
    
    /**
     * Delete first occurrence of value
     * Time Complexity: O(n)
     * @return true if element was found and deleted, false otherwise
     */
    bool deleteValue(const T& value) {
        if (!head) {
            return false;
        }
        
        // Check if head needs to be deleted
        if (head->data == value) {
            head = head->next;
            size--;
            return true;
        }
        
        // Search for value in rest of list
        auto current = head;
        while (current->next && current->next->data != value) {
            current = current->next;
        }
        
        if (current->next) {
            current->next = current->next->next;
            size--;
            return true;
        }
        
        return false;
    }
    
    /**
     * Search for a value in the list
     * Time Complexity: O(n)
     * @return true if found, false otherwise
     */
    bool search(const T& value) const {
        auto current = head;
        while (current) {
            if (current->data == value) {
                return true;
            }
            current = current->next;
        }
        return false;
    }
    
    /**
     * Get the size of the list
     * Time Complexity: O(1)
     */
    size_t getSize() const {
        return size;
    }
    
    /**
     * Check if list is empty
     * Time Complexity: O(1)
     */
    bool isEmpty() const {
        return head == nullptr;
    }
    
    /**
     * Display the list
     */
    void display() const {
        if (!head) {
            std::cout << "List is empty" << std::endl;
            return;
        }
        
        auto current = head;
        while (current) {
            std::cout << current->data;
            if (current->next) {
                std::cout << " -> ";
            }
            current = current->next;
        }
        std::cout << std::endl;
    }
    
    /**
     * Clear the list
     */
    void clear() {
        head = nullptr;
        size = 0;
    }
};

/**
 * Test function
 */
void runTests() {
    std::cout << "Linked List Tests" << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    
    LinkedList<int> list;
    
    // Test 1: Insert at head
    std::cout << "\nTest 1: Insert at head (3, 2, 1)" << std::endl;
    list.insertHead(3);
    list.insertHead(2);
    list.insertHead(1);
    list.display();
    std::cout << "Size: " << list.getSize() << std::endl;
    
    // Test 2: Insert at tail
    std::cout << "\nTest 2: Insert at tail (4, 5)" << std::endl;
    list.insertTail(4);
    list.insertTail(5);
    list.display();
    std::cout << "Size: " << list.getSize() << std::endl;
    
    // Test 3: Search
    std::cout << "\nTest 3: Search operations" << std::endl;
    std::cout << "Search 3: " << (list.search(3) ? "Found" : "Not found") << std::endl;
    std::cout << "Search 10: " << (list.search(10) ? "Found" : "Not found") << std::endl;
    
    // Test 4: Delete
    std::cout << "\nTest 4: Delete value 3" << std::endl;
    bool deleted = list.deleteValue(3);
    std::cout << "Deleted: " << (deleted ? "Yes" : "No") << std::endl;
    list.display();
    std::cout << "Size: " << list.getSize() << std::endl;
    
    // Test 5: Delete head
    std::cout << "\nTest 5: Delete head (1)" << std::endl;
    list.deleteValue(1);
    list.display();
    std::cout << "Size: " << list.getSize() << std::endl;
    
    // Test 6: Clear
    std::cout << "\nTest 6: Clear list" << std::endl;
    list.clear();
    std::cout << "Is empty: " << (list.isEmpty() ? "Yes" : "No") << std::endl;
    list.display();
    
    std::cout << "\nAll tests completed!" << std::endl;
}

int main() {
    runTests();
    return 0;
}
