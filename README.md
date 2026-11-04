# Eval-Driven Development: Exercises and Code

Companion material for [Eval-Driven Development](https://github.com/danraid/eval-driven-development), organised by the 12 chapters of the book.

Each `chapters/NN/` directory contains the chapter's exercises and a worked answer key. Each `labs/NN/` directory contains runnable, offline synthetic teaching examples. Where the book provides full scripts inline, those scripts are included as standalone files. Some examples require Python 3.9+ and use only the Python standard library.

The source book is a private repository; chapter links may require access. These exercises are educational synthetic examples, not production safety or release certification.

## Contents

| Chapter | Exercises | Worked solutions | Code |
| --- | --- | --- | --- |
| 1 | [Exercises](chapters/01/exercises.md) | [Answers](chapters/01/solutions.md) | [Lab](labs/01/README.md) |
| 2 | [Exercises](chapters/02/exercises.md) | [Answers](chapters/02/solutions.md) | [Lab](labs/02/README.md) |
| 3 | [Exercises](chapters/03/exercises.md) | [Answers](chapters/03/solutions.md) | [Lab](labs/03/README.md) |
| 4 | [Exercises](chapters/04/exercises.md) | [Answers](chapters/04/solutions.md) | [Lab](labs/04/README.md) |
| 5 | [Exercises](chapters/05/exercises.md) | [Answers](chapters/05/solutions.md) | [Lab](labs/05/README.md) |
| 6 | [Exercises](chapters/06/exercises.md) | [Answers](chapters/06/solutions.md) | [Lab](labs/06/README.md) |
| 7 | [Exercises](chapters/07/exercises.md) | [Answers](chapters/07/solutions.md) | [Lab](labs/07/README.md) |
| 8 | [Exercises](chapters/08/exercises.md) | [Answers](chapters/08/solutions.md) | [Lab](labs/08/README.md) |
| 9 | [Exercises](chapters/09/exercises.md) | [Answers](chapters/09/solutions.md) | [Lab](labs/09/README.md) |
| 10 | [Exercises](chapters/10/exercises.md) | [Answers](chapters/10/solutions.md) | [Lab](labs/10/README.md) |
| 11 | [Exercises](chapters/11/exercises.md) | [Answers](chapters/11/solutions.md) | [Lab](labs/11/README.md) |
| 12 | [Exercises](chapters/12/exercises.md) | [Answers](chapters/12/solutions.md) | [Lab](labs/12/README.md) |

## Run locally

```sh
python -m unittest discover -s labs/01 -p 'test_*.py' -v
```

See each lab's README for its exact commands. All datasets and scores in these materials are synthetic unless explicitly stated otherwise. Run teaching scripts in a separate working directory when they write output files.
