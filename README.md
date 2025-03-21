# T3
[![Language](https://img.shields.io/github/languages/top/zackxzhang/T3)](https://github.com/zackxzhang/T3)
[![License](https://img.shields.io/github/license/zackxzhang/T3)](https://opensource.org/licenses/BSD-3-Clause)
[![Last Commit](https://img.shields.io/github/last-commit/zackxzhang/T3)](https://github.com/zackxzhang/T3)

*reinforcement learning for tic tac toe*

##### scaffolding
- [x] state transition
- [x] value tabulation
- [x] user interface

##### reinforcement learning
- [x] reward shaping
- [x] rate scheduling
- [x] importance sampling

##### match result
|       player     || win ratio                    |||
|:-------:|:-------:|---------:|---------:|---------:|
|   `X`   |   `O`   |    `X`   |    `-`   |    `O`   |
| random  | random  |  58.26 % |  13.45 % |  28.29 % |
|   agent | random  |  99.07 % |   0.93 % |   0.00 % |
| random  | agent   |   0.00 % |   8.87 % |  91.13 % |
|   agent | agent   |   0.00 % | 100.00 % |   0.00 % |
