import random
import my_map
import time

random.seed(42)

def jibbish_string():
    length = random.choice([2, 3, 4])
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length))


def time_avg_access_time_sec(m: my_map.MyMap) -> tuple[float, int]:
    num_trials = 100
    num_test_words = 100
    num_times = num_trials * num_test_words
    test_words = [jibbish_string() for _ in range(num_test_words)]
    start_time = time.perf_counter()
    cnt = 0
    for i in range(num_trials):
        for word in test_words:
            if word in m:
                cnt += 1
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return elapsed_time/num_times, cnt


def test_map(test_custom_dict: bool, load_factor: float = 0.0):
    for table_size in [100, 10, 1]:
        for n in [8000, 16000, 32000]:
            if test_custom_dict:
                word_map = my_map.MyMap(table_size, load_factor)
            else:
                word_map = dict()
            for _ in range(n):
                word_map[jibbish_string()] = True
            sec, cnt = time_avg_access_time_sec(word_map)
            print(f'N={table_size:4d}, n={n:8d}, microsec={1000*1000*sec:10.5f} ({cnt:7d})', end ='')
            if test_custom_dict:
                print('  bucket sizes=', repr(word_map))
            else:
                print()


def test_basic():
    strings = ["a", "b", "a"]
    word_map = my_map.MyMap(2)
    for s in strings:
        if s in word_map:
            word_map[s] += 1
        else:
            word_map[s] = 1
    print(word_map, repr(word_map))
    if len(word_map) > 0:
        del word_map["a"]
        print(word_map, repr(word_map))

print("====> Test basic")
test_basic()

# Once you got the basic test working then uncomment the test_map calls below.
print("====> Test My dict")
# test_map(True)
print("====> Test My dict with resizing based on load factor")
# test_map(True, 5.0)
print("====> Test Python's dict")
# test_map(False)
