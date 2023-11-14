function linear_search(arr, search_term){ 
    for (let i in arr){ 
        if (arr[i] == search_term) return i;
    }
    return -1; 
}   

function binary_search(arr, search_term){ 
    mid = Math.floor(arr.length/2);  
    if (arr[mid] == search_term) return mid; 
    else if (arr[mid] > search_term) return binary_search(arr.slice(0, mid), search_term); 
    else if (arr[mid] < search_term) return binary_search(arr.slic(mid, -1), search_term) 
    else return -1; 
}  

function merge(left, right){ 
    let result = []; 
    while (left.length && right.length){ 
        if (left[0] < right[0]) result.push(left.shift()); 
        else result.push(right.shift()); 
    } 
    return result.concat(left, right); 
}

function merge_sort(arr){ 
    if (arr.length <= 1) return arr; 
    mid = Math.floor(arr.length/2); 
    left = merge_sort(arr.slice(0, mid)); 
    right = merge_sort(arr.slice(mid, -1)); 
    return merge(left, right);  
}

// Path: test.js 
console.log(linear_search([1,2,3,4,5], 3)) 
console.log(binary_search([1,2,3,4,5], 3)) 
console.log(merge_sort([5, 4, 3, 2, 1])) 