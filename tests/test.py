from projektwae.evolution import differential_evolution, differential_evolution_dg

def f(arg):
    x = arg[0]
    y = arg[1]
    return (x - 1)**2 + (y + 2)**2

def main():
    for result in differential_evolution(f, [(-10, 10), (-10, 10)]):
        print(result)

if __name__ == '__main__':
    main()
