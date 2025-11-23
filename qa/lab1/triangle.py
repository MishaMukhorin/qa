import sys

def classify_triangle(a, b, c):
    try:
        a, b, c = float(a), float(b), float(c)
        
        if a <= 0 or b <= 0 or c <= 0:
            return "not_triangle"
        
        if a + b <= c or a + c <= b or b + c <= a:
            return "not_triangle"
        
        if a == b == c:
            return "equilateral"
        
        if a == b or b == c or a == c:
            return "isosceles"
        
        return "scalene"
    
    except (ValueError, TypeError):
        return "error"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("error")
        sys.exit(1)
    
    result = classify_triangle(sys.argv[1], sys.argv[2], sys.argv[3])
    print(result)