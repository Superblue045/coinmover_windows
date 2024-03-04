def bad_method():
    sqrt = 0**-1

def test_method():
    try:
        bad_method()
    except Exception:
        print("error")

# Test : OK
test_method()
print("run")