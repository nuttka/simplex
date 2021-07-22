import numpy as np


class Simplex:

    def FPI_form(number_restrictions, c, a):

        identity = np.identity(number_restrictions, dtype=np.float)
        new_vars = np.zeros(number_restrictions, dtype=np.float)

        a_fpi = np.concatenate((a, identity), axis=1)
        c_fpi = np.concatenate((c, new_vars), axis=None)
        number_variables = len(c_fpi)

        return a_fpi, c_fpi, number_variables


    def tableau(a, b, c, number_restrictions, number_variables):
        
        tableau = np.zeros((number_restrictions + 1, number_variables + 1))
        vero_identity = np.identity(number_restrictions, dtype=np.float)
        vero_top = np.zeros(number_restrictions)
        vero = np.vstack([vero_top, vero_identity])

        for i in range(0, number_restrictions):
            tableau[i+1][number_variables] = b[i]
            for j in range(0, number_variables):
                tableau[i+1][j] = a[i][j]
                tableau[0][j] = c[j] * (-1)

        tableau_vero = np.concatenate((vero, tableau), axis=1)

        return tableau_vero


    def find_column_to_pivot(tableau, number_restrictions):
        for i in range(number_restrictions, tableau.shape[1] - 1):
            if tableau[0][i] < 0:
                return i
        
        return -1


    def find_row_to_pivot(tableau, column_to_pivot, number_restrictions):
        index = -1

        for i in range(1, number_restrictions + 1):
            if tableau[i][column_to_pivot] <= 0:
                continue
            elif index == -1:
                index = i
            elif (tableau[i][tableau.shape[1] - 1] / tableau[i][column_to_pivot]) < (tableau[index][tableau.shape[1] - 1] / tableau[index][column_to_pivot]):
                index = i

        return index

    def pivot(tableau, pivot_index):
        for i in range(0, tableau.shape[0]):
            for j in range(0, tableau.shape[1]):
                if i != pivot_index[0] and j != pivot_index[1]:
                    tableau[i][j] -= tableau[pivot_index[0]][j] * tableau[i][pivot_index[1]] / tableau[pivot_index[0]][pivot_index[1]]

        for i in range(0, tableau.shape[0]):
            if i != pivot_index[0]:
                tableau[i][pivot_index[1]] = 0.0
        
        for i in range(0, tableau.shape[1]):
            if i != pivot_index[1]:
                tableau[pivot_index[0]][i] /= tableau[pivot_index[0]][pivot_index[1]]
        
        tableau[pivot_index[0]][pivot_index[1]] = 1.0
        return tableau

    def get_certificate(tableau, number_restrictions):
        return tableau[0][0:number_restrictions]

    def get_optimal_value(tableau):
        return tableau[0][tableau.shape[1]-1]

    def get_solution(tableau, number_restrictions):
        sol = []
        for i in range(1, number_restrictions+1):
            sol.append(tableau[i][tableau.shape[1]-1])
        return sol
    
    def interpret_result(tableau, number_restrictions):
        optimal = 1
        for i in range(number_restrictions, tableau.shape[1]):
            if tableau[0][i] < 0:
                optimal = -1

        if optimal:
            certificate = Simplex.get_certificate(tableau, number_restrictions)
            optimal_value = Simplex.get_optimal_value(tableau)
            solution = Simplex.get_solution(tableau, number_restrictions)
            print("otima")
            print(optimal_value)
            print(solution)
            print(certificate)

    def solve(tableau, number_restrictions):
        iteration = 0
        while 1:
            iteration += 1

            print('>> Iteration: ', iteration);
            print('Tableau: \n', tableau)

            column_to_pivot = Simplex.find_column_to_pivot(tableau, number_restrictions)
            if column_to_pivot == -1:
                break;

            row_to_pivot = Simplex.find_row_to_pivot(tableau, column_to_pivot, number_restrictions)
            if row_to_pivot == -1:
                break;

            pivot_index = (row_to_pivot, column_to_pivot)

            tableau = Simplex.pivot(tableau, pivot_index)

        print('>> Término:')
        print('Tableau: \n', tableau)
        Simplex.interpret_result(tableau, number_restrictions)