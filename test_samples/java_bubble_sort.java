// Bubble Sort - Inefficient Implementation
// Poor code quality demonstration

public class BubbleSort {
    
    // bad naming, no documentation
    public static void sort(int[] a) {
        // nested loops - O(n^2) complexity
        for(int i=0;i<a.length;i++){
            for(int j=0;j<a.length-1;j++){
                // no optimization for already sorted arrays
                if(a[j]>a[j+1]){
                    // swap without temp variable explanation
                    int t=a[j];
                    a[j]=a[j+1];
                    a[j+1]=t;
                }
            }
        }
    }
    
    public static void main(String[] args){
        int[] arr={64,34,25,12,22,11,90};
        sort(arr);
        // no proper output formatting
        for(int i=0;i<arr.length;i++){
            System.out.print(arr[i]+" ");
        }
    }
}
