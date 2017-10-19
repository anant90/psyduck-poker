# psyduck-poker
Python implementation of a Monte Carlo Simulator of Psyduck's Poker

# Overview
Requires as input a number of iterations to run, as well as three flop cards.

The program outputs number of 3s of a kind, straights, flushes, full houses and quads in absolute terms as well as percentage.

# Sample Run
Run atleast 1000 iterations to get decent results:

```
➜  psyduck-poker git:(master) ✗ python pokersim.py --community 7cTsAs 100
Total Hands: 100
3s: 7 Straight: 13 Flush: 6 Full House: 3 Quads: 1
3s: 7.00% Straight: 13.00% Flush: 6.00% Full House: 3.00% Quads: 1.00%
➜  psyduck-poker git:(master) ✗ python pokersim.py --community 7cTsAs 1000
Total Hands: 1000
3s: 76 Straight: 109 Flush: 55 Full House: 62 Quads: 9
3s: 7.60% Straight: 10.90% Flush: 5.50% Full House: 6.20% Quads: 0.90%
➜  psyduck-poker git:(master) ✗ python pokersim.py --community 7cTsAs 10000
Total Hands: 10000
3s: 809 Straight: 1089 Flush: 435 Full House: 540 Quads: 39
3s: 8.09% Straight: 10.89% Flush: 4.35% Full House: 5.40% Quads: 0.39%
➜  psyduck-poker git:(master) ✗ python pokersim.py --community 7cTsAs 100000
Total Hands: 100000
3s: 8055 Straight: 10802 Flush: 4390 Full House: 5492 Quads: 386
3s: 8.05% Straight: 10.80% Flush: 4.39% Full House: 5.49% Quads: 0.39%
```
