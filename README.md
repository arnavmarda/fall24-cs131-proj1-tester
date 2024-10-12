# fall24-cs131-proj1-tester
A script to generate important specification based tests and random tests for UCLA CS 131's Project 1 with Prof. Nachenberg.

## Set Up
Make sure to place the `gen_test.py` file in the fall-24-autograder folder. It should be in the same folder as `tester.py`. To set up the environment and download the additional libraries, run
```
pip install -r requirements.txt
```

## Usage
```linux
>> python3 gen_test.py --help

Usage: gen_test.py [OPTIONS]

Options:
  -r, --rand BOOLEAN           Generate random tests  [default: True]
  -n, --num-tests INTEGER      Number of random tests to generate  [default:
                               5]
  -x, --num-lines INTEGER      Number of lines in random tests  [default: 10]
  -s, --specification BOOLEAN  Generate tests based on specification
                               [default: True]
  -c, --cleanup                Cleanup generated tests
  --help                       Show this message and exit.
```

To run only the specifications generated tests:
```linux
python gen_test.py -r
```

To run only the randomly generated tests:
```linux
python gen_test.py -s
```

To cleanup all additional test files added:
```linux
python gen_test.py -c
```

### Advanced Usage
The `-n` flag can be used to specify the number of random tests to generate. The '-x' flag can be used to specify the number of lines to generate in the random tests (this does not count the func main() declaration). For example, to only generate 25 random tests of 20 lines each, I would run:
```linux
python gen_test.py -s -n 25 -x 20
```
