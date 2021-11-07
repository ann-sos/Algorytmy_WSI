import numpy as np
import random
import matplotlib.pyplot as plt


def quadratic_function(x):
    return 1.5 * x ** 2


def bird_function(xy):
    x, y = xy
    return np.sin(x) * (np.exp(1 - np.cos(y)) ** 2) + \
           np.cos(y) * (np.exp(1 - np.sin(x)) ** 2) + (x - y) ** 2


def generate_population(population_size):
    return [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(population_size)]


def uniform_population(population_size):
    return [(random.uniform(-10, 10), random.uniform(-10, 10))] * population_size


def find_the_best(P_0, eval):
    pass


def reproduction(P, P_eval, population_size, S=2):
    R = []
    for p in range(population_size):
        opponents = [random.randrange(population_size) for _ in range(S)] # indexes of specimens chosen for tournament
        scores = [P_eval[o] for o in opponents]
        R.append(P[np.argmin(scores)])
    return R


# krzyżowanie i mutacja
def genetic_operations(R, sigma, p_c=0.1):
    M = []
    for _ in range(len(R)//2):
        parent_1, parent_2 = R[random.randrange(len(R))], R[random.randrange(len(R))]
        child_1 = (p_c * parent_1[0] + (1 - p_c) * parent_2[0], p_c * parent_1[1] + (1 - p_c) * parent_2[1])
        child_2 =(p_c * parent_2[0] + (1 - p_c) * parent_1[0], p_c * parent_2[1] + (1 - p_c) * parent_1[1])
        child_1 = (child_1[0] + sigma * random.gauss(0, 1), child_1[1] + sigma * random.gauss(0, 1))
        child_2 = (child_2[0] + sigma * random.gauss(0, 1), child_2[1] + sigma * random.gauss(0, 1))
        M.append(child_1)
        M.append(child_2)
    return M


#sukcesja elitarna
def succession(P, P_eval, M, M_eval, population_size, e):
    S = []
    # choose e best from P
    for _ in range(e):
        idx = np.argmin(P_eval)
        S.append(P.pop(idx))
        P_eval.pop(idx)
    # choose mu - e from M
    for _ in range(population_size - e):
        idx = np.argmin(M_eval)
        S.append(M.pop(idx))
        M_eval.pop(idx)
    return S


#sigma = siła mutacji
#p_c
def evolutionary_algorithm(q, P, population_size, sigma, p_c, t_max, S, elite):
    score_array = []
    t = 0
    P_eval = [q(specimen) for specimen in P]
    best_point, best_score = P[np.argmin(P_eval)], np.min(P_eval)
    while t < t_max:
        R = reproduction(P, P_eval, population_size, S)
        M = genetic_operations(R, sigma, p_c)
        M_eval = [q(specimen) for specimen in M]
        best_point_t, best_score_t = M[np.argmin(M_eval)], np.min(M_eval)
        if best_score_t <= best_score:
            best_score = best_score_t
            best_point = best_point_t
        P = succession(P, P_eval, M, M_eval, population_size, elite)
        P_eval = [q(specimen) for specimen in P]
        t += 1
        score_array.append(best_score)
    return best_point, best_score, score_array


if __name__ == "__main__":
    sigma = 2     # zasięg mutacji
    S = 2   # rozmiar turnieju
    p_c = 1     # prawdopodobieństwo krzyżowania
    t = 17000     # liczba iteracji

    e = 1
    population_size = 20
    best_point, best_score, score_array = evolutionary_algorithm(bird_function,
                                                                 generate_population(population_size),
                                                                 population_size, sigma, p_c, t, S, e)
    best_point_u, best_score_u, score_array_u = evolutionary_algorithm(bird_function,
                                                                 uniform_population(population_size),
                                                                 population_size, sigma, p_c, t, S, e)

    plt.plot(np.arange(0, t, 1), score_array, np.arange(0, t, 1), score_array_u)
    plt.legend(["random", "uniform"])
    plt.xlabel("Iteration number")
    plt.ylabel("Min z-value")
    plt.xscale('log')
    plt.show()
    """for population_size in [10, 30, 60]:
        mean_best_score = 0
        mean_score_array = np.zeros(t)
        n = 10
        for _ in range(n):
            best_point, best_score, score_array = evolutionary_algorithm(bird_function,
                                                                         generate_population(population_size),
                                                                         population_size, sigma, p_c, t, S, e)
            mean_best_score += best_score
            mean_score_array += score_array
        plt.subplot(121)
        plt.plot(population_size, mean_best_score / n, 'bo')
        plt.subplot(122)
        plt.plot(np.arange(0, t, 1), mean_score_array / n)
    plt.subplot(121)
    plt.xlabel(r"Population size")
    plt.ylabel("Mean min z-value")
    plt.subplot(122)
    plt.xlabel("Iteration number")
    plt.ylabel("Min z-value")
    plt.xscale('log')
    plt.legend(["population = 10", "population = 30", "population = 60"])
    plt.show()"""
    
    
    
    
    
    

    """population_size = 20
    for sigma in [0.1, 0.5, 2]:
        mean_best_score = 0
        mean_score_array = np.zeros(t)
        n = 10
        for _ in range(n):
            best_point, best_score, score_array = evolutionary_algorithm(bird_function,
                                                                         generate_population(population_size),
                                                                         population_size, sigma, p_c, t, S, e)
            mean_best_score += best_score
            mean_score_array += score_array
        plt.subplot(121)
        plt.plot(sigma, mean_best_score / n, 'bo')
        plt.subplot(122)
        plt.plot(np.arange(0, t, 1), mean_score_array / n)
    plt.subplot(121)
    plt.xlabel(r"$\sigma$")
    plt.ylabel("Mean min z-value")
    plt.subplot(122)
    plt.xlabel("Iteration number")
    plt.ylabel("Min z-value")
    plt.xscale('log')
    plt.legend(["$\sigma$ = 0.1", "$\sigma$ = 0.5", "$\sigma$ = 2"])
    plt.show()"""




    """population_size = 20
    for e in [1, 5, 10]:
        mean_best_score = 0
        mean_score_array = np.zeros(t)
        n = 10
        for _ in range(n):
            best_point, best_score, score_array = evolutionary_algorithm(bird_function,
                                                                         generate_population(population_size),
                                                                         population_size, sigma, p_c, t, S, e)
            mean_best_score += best_score
            mean_score_array += score_array
        plt.subplot(121)
        plt.plot(e, mean_best_score / n, 'bo')
        plt.subplot(122)
        plt.plot(np.arange(0, t, 1), mean_score_array / n)
    plt.subplot(121)
    plt.xlabel(r"Size of the elite")
    plt.ylabel("Mean min z-value")
    plt.subplot(122)
    plt.xlabel("Iteration number")
    plt.ylabel("Min z-value")
    plt.xscale('log')
    plt.legend(["elite = 1", "elite = 5", "elite = 10"])
    plt.show()"""


