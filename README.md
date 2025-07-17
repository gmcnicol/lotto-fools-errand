# Euromillions GA Ticket Generator

> “A fool and his tickets are soon parted.”  
> *We know it’s a FOOL’S ERRAND—but we do it anyway!*

A small Python project that uses a Genetic Algorithm (GA) to “evolve” sets of Euromillions lottery tickets against historical draw data. It is **not** a magic bullet—lottery numbers are (practically) random—but this experiment demonstrates:

- Dynamic discovery of ticket‐generation strategies  
- Encoding strategies as genes in chromosomes  
- Standard GA operators: selection (elitism), crossover, mutation  
- Back‐testing fitness against historical draws  

---

## Features

- **Fetch & cache** all past Euromillions draws locally  
- **Define strategies** (e.g. modulo‐increment, random patterns) with configurable parameters  
- **Automatically enumerate** all strategy/parameter variants  
- **GA core engine** with elitism, crossover, mutation, convergence criteria  
- **Command‐line interface** 

---

## Installation

   ```bash
   git clone git@github.com:gmcnicol/lotto-fools-errand.git euromillions
   cd euromillions
   make clean install
   ```

---

## Usage

1. **Fetch data** (needed at least once, or after every draw happens in the real world):
   ```bash
   make fetch-draws
   ```
2. **Run evolution** (will take several minutes but will give you a running log):
   ```bash
   make generate
   ```
   - Will log each generation’s best fitness, then print:
     - The **fittest chromosome** (which strategy/parameter bits are “on”)
     - **Suggested tickets** based on that chromosome
3. **Inspect stats**:
   ```bash
   make stats
   ```

---

## Project Structure
This is probably inaccurate.
```
euromillions-ga/
├── src/
│   └── euromillions/
│       ├── __main__.py            # CLI entry point
│       ├── euromillions_loader.py # fetch & load draws
│       ├── generators/
│       │   ├── strategy_registry.py  # assemble all strategy variants
│       │   └── strategies/           # implementations (e.g. modulo_increment.py)
│       └── genetics/
│           ├── evolve.py           # GA core loop (selection, crossover, mutation)
│           └── fitness.py          # back-test fitness calculation
├── Makefile                      # automation: clean, install, fetch-draws, generate, stats, zip
├── requirements.txt
└── README.md                     # ← you are here
```

---

## How It Works

1. **Strategies** are functions that, given past draws, return one or more tickets.  
2. **Variants** enumerate over all reasonable parameter combinations (e.g. start = 1–50, increment = 1–10).  
3. A **chromosome** is a binary vector selecting which variants to include.  
4. Each generation:
   - **Evaluate fitness**: how well the chosen tickets would have performed against history  
   - **Select elites** (top N chromosomes)  
   - **Crossover** pairs to produce children  
   - **Mutate** some bits with a small probability  
   - Continue until convergence or max generations  
5. **Output** the final “best” chromosome and its corresponding ticket list.

---

## Why It’s a Fool’s Errand

- Lottery draws are effectively random—no algorithm can reliably predict them.  
- This project is purely **exploratory** and **educational**.  
- Do **not** use it for serious gambling purposes!  If you do, do not blame me. 

---

## License

MIT‑style “play at your own risk” license. See [LICENSE](LICENSE) for details.
