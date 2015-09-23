#!usr/bin/env python3.4
import random as rnd
import string
import time


def random_char():
    """
    Returns a random printable character.
    """
    return bytearray(rnd.choice(string.printable[:-5]).encode())


def random_population(N, ind_len):
    """Return randomly generated population of 'N' individuals. 'ind_len' specifies
    size of each individual.
    """
    return [bytearray(b"".join([random_char() for _ in range(ind_len)]))
            for _ in range(N)]


def hamming_distance(s1, s2, bitwise=False):
    """Return hamming distance of 's1' and 's2'.
    Set 'bitwise' to True to do bitwise comparisons.

    s1: "Hellk("
    s2: "Hello!"
    distance is 2.
    """
    if len(s1) != len(s2):
        raise ValueError("Not specified for unequal lengths")
    if not bitwise:
        return sum(chr1 != chr2 for chr1, chr2 in zip(s1, s2))
    else:
        byte1, byte2 = bytearray(s1), bytearray(s2)
        return sum(bin(byte1[i] ^ byte2[i]).count("1")
                   for i in range(len(byte1)))


def grade(population, target):
    """Return mean fitness of 'population'.
    """
    whole = sum(hamming_distance(ind, target) for ind in population)
    best = sorted(population, key=lambda x: hamming_distance(x, target))[0]
    return {
        "grade": whole / len(population),
        "best": bytearray(best),
        "bestfit": hamming_distance(best, target),
        }


def make_spawns(parents, rate = 0.5):
    """Makes child based on UX of rate 0.5
    """
    male = parents[0]
    fema = parents[1]
    c1, c2 = [], []
    if len(male) != len(fema):
        ValueError("Undefined for sequences of unequal length")
    for ch in range(len(male)):
        if male[ch] == fema[ch]:
            c1.append(male[ch])
            c2.append(male[ch])
        else:
            if rnd.random() < rate:
                c1.append(fema[ch])
                c2.append(male[ch])
            else:
                c1.append(male[ch])
                c2.append(fema[ch])
    return c1, c2


def evolve(population, length, target, scale=True,
           retain=0.2, mutation=0.0015, pick=0.1):
    """Evolves the population by one generation.
    """
    if scale:
        mutation = mutation + (length//15) * mutation
    graded = sorted(population, key=lambda s: hamming_distance(s, target))
    retain_amount = int(len(graded)*retain)
    parents = graded[:retain_amount]
    for ind in parents:
        if mutation < rnd.random():
            ind[rnd.randint(0, len(ind)-1)] = ord(random_char())
    picked = rnd.sample(graded[retain_amount:], int(len(population)*pick))
    parents.extend(picked)
    rnd.shuffle(parents)
    spawn = []
    while len(spawn) < len(population)-len(parents):
        spawn.extend(make_spawns(rnd.sample(parents, 2)))
    spawn.extend(parents)
    spawn = [bytearray(ind) for ind in spawn]
    return spawn
if __name__ == "__main__":
    pop_size = input("Size of pop (blank=100):")
    pop_size = int(pop_size) if pop_size else 100
    str_ = bytes(input("Input string:").encode())
    pop = random_population(pop_size, len(str_))
    best = [grade(pop, str_)]
    start = time.time()
    evolved = pop
    while True:
        evolved = evolve(evolved, len(str_), str_)
        best.append(grade(evolved, str_))
        #print(
        #    "{:3}!{:04} Best:{} ! {:03}".format(len(best) + 1, best[0]["grade"], best[-1]["best"].decode(),
        #        hamming_distance(best[-1]["best"], str_)))
        if hamming_distance(best[-1]["best"], str_) == 0:
            break
    timed = time.time()-start
    # print("Generation: {:6}, First best: {}".format(1, best[0]["best"]))
    print("Generation: {:6}, Result: {}\nTime:{} ms".format(
        len(best)+1, best[-1]["best"], timed))
    #from bashplotlib.scatterplot import plot_scatter
    #plot_scatter(None, list(range(len(best))), [best_["grade"] for best_ in best], 30, "+", None, None)
    import time
    import csv
    from subprocess import call
    filetime = time.strftime("%Y%m%d-%H%M%S")
    with open("evolution-{}.csv".format(filetime), "w") as f:
        writer = csv.writer(f)
        writer.writerows(zip(list(range(len(best))), [best_["grade"] for best_ in best], [best_["bestfit"] for best_ in best]))
    plotting = """data = dlmread("evolution-{0}.csv", ",");
    [ax, h1, h2] = plotyy(data(:,1),data(:,2),data(:,1), data(:,3))
    title("Evolution for string {1}")
    ylabel(ax(1), "Mean fitness of population")
    ylabel(ax(2), "Best fitness in population")
    xlabel("Generation")
    print("evolution-{0}.png")
    """
    import shutil
    if shutil.which("octave"):
        call(["octave","-q", "--eval", plotting.format(filetime, str_.decode())])
