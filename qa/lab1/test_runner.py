import subprocess
import sys

def run_tests(test_file, results_file):
    results = []
    
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 4:
                continue
            
            a, b, c = parts[0], parts[1], parts[2]
            expected = ' '.join(parts[3:])
            
            try:
                result = subprocess.run(
                    [sys.executable, 'triangle.py', a, b, c],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                actual = result.stdout.strip()
                
                if actual.lower() == expected.lower():
                    results.append('success')
                else:
                    results.append(f'error')
            except Exception:
                results.append('error')
    
    with open(results_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result + ';\n')
    
    success_count = sum(1 for r in results if r == 'success')
    total_count = len(results)
    print(f"Tests passed: {success_count}/{total_count}")

if __name__ == "__main__":
    test_file = 'test_cases.txt'
    results_file = 'test_results.txt'
    
    run_tests(test_file, results_file)
    print(f"Results saved to {results_file}")