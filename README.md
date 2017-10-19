# psyduck-poker
Python implementation of a Monte Carlo Simulator of Psyduck's Poker

# Overview
Requires as input a number of iterations to run, as well as three flop cards.

The program outputs number of 3s of a kind, straights, flushes, full houses and quads in absolute terms as well as percentage.

# Sample Run

```
➜  psyduck-poker python pokersim.py --community 7cTsAs 100
Total Hands: 100
3s: 11 Straight: 6 Flush: 4 Full House: 1 Quads: 0
3s: 11.00% Straight: 6.00% Flush: 4.00% Full House: 1.00% Quads: 0.00%

➜  psyduck-poker python pokersim.py --community 7cTsAs 1000
Total Hands: 1000
3s: 92 Straight: 99 Flush: 45 Full House: 58 Quads: 1
3s: 9.20% Straight: 9.90% Flush: 4.50% Full House: 5.80% Quads: 0.10%

➜  psyduck-poker git:(master) python pokersim.py --community 7cTsAs 10000
Total Hands: 10000
3s: 823 Straight: 1102 Flush: 415 Full House: 552 Quads: 34
3s: 8.23% Straight: 11.02% Flush: 4.15% Full House: 5.52% Quads: 0.34%

➜  psyduck-poker git:(master) python pokersim.py --community 7cTsAs 100000
Total Hands: 100000
3s: 8298 Straight: 10532 Flush: 4319 Full House: 5503 Quads: 411
3s: 8.30% Straight: 10.53% Flush: 4.32% Full House: 5.50% Quads: 0.41%
```
