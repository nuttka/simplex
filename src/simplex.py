import numpy as np


class Simplex:

    def __init__(self, number_restrictions_initial, number_variables_initial, c_array_initial, a_matrix_initial, b_array_initial):
        self.number_restrictions_initial = number_restrictions_initial
        self.number_variables_initial = number_variables_initial
        self.c_array_initial = c_array_initial
        self.a_matrix_initial = a_matrix_initial
        self.b_array_initial = b_array_initial




    def FPI_form(self):
        identity = np.identity(self.number_restrictions_initial, dtype=np.float)
        new_vars = np.zeros(self.number_restrictions_initial, dtype=np.float)

        self.a_matrix_fpi = np.concatenate((self.a_matrix_initial, identity), axis=1)
        self.c_array_fpi = np.concatenate((self.c_array_initial, new_vars), axis=None)
        self.number_variables_fpi = len(self.c_array_fpi)




    def tableau(self):
        tableau = np.zeros((self.number_restrictions_initial + 1, self.number_variables_fpi + 1))

        vero_identity = np.identity(self.number_restrictions_initial, dtype=np.float)
        vero_top = np.zeros(self.number_restrictions_initial)
        vero = np.vstack([vero_top, vero_identity])

        for i in range(0, self.number_restrictions_initial):
            tableau[i+1][self.number_variables_fpi] = self.b_array_initial[i]
            for j in range(0, self.number_variables_fpi):
                tableau[i+1][j] = self.a_matrix_fpi[i][j]
                tableau[0][j] = self.c_array_fpi[j] * (-1)

        self.tableau = np.concatenate((vero, tableau), axis=1)

        # print(">> Tableau pós FPI")
        # print(self.tableau)




    def find_column_to_pivot(self):
        for i in range(self.number_restrictions_initial, self.tableau.shape[1] - 1):
            if self.tableau[0][i].round(10) < 0:
                return i
        
        return -1



    def find_row_to_pivot(self, column_to_pivot):
        index = -1

        for i in range(1, self.number_restrictions_initial + 1):
            if self.tableau[i][column_to_pivot] <= 0:
                continue
            elif index == -1:
                index = i
            elif (self.tableau[i][self.tableau.shape[1] - 1] / self.tableau[i][column_to_pivot]) < (self.tableau[index][self.tableau.shape[1] - 1] / self.tableau[index][column_to_pivot]):
                index = i

        return index



    def pivot(self, pivot_index):
        for i in range(0, self.tableau.shape[0]):
            for j in range(0, self.tableau.shape[1]):
                if i != pivot_index[0] and j != pivot_index[1]:
                    self.tableau[i][j] -= self.tableau[pivot_index[0]][j] * self.tableau[i][pivot_index[1]] / self.tableau[pivot_index[0]][pivot_index[1]]

        for i in range(0, self.tableau.shape[0]):
            if i != pivot_index[0]:
                self.tableau[i][pivot_index[1]] = 0.0
        
        for i in range(0, self.tableau.shape[1]):
            if i != pivot_index[1]:
                self.tableau[pivot_index[0]][i] /= self.tableau[pivot_index[0]][pivot_index[1]]
        
        self.tableau[pivot_index[0]][pivot_index[1]] = 1.0



    def get_certificate(self):
        return self.tableau[0][0:self.number_restrictions_initial].round(10)



    def get_optimal_value(self):
        return self.tableau[0][self.tableau.shape[1]-1]



    def get_solution(self):
        solution = []
        for i in range(self.number_restrictions_initial, self.number_restrictions_initial + self.number_variables_fpi):
            if self.tableau[0][i] == 0:
                index = np.where(self.tableau[:, i] == 1)
                if len(index[0]) == 1:
                    solution.append(self.tableau[index[0][0]][self.tableau.shape[1] - 1])
                else:
                    solution.append(0)
            else:
                solution.append(0)

        return np.array(solution[0:self.number_variables_initial])
    



    def interpret_result(self):
        # optimal = 1
        # for i in range(self.number_restrictions_initial, self.tableau.shape[1]):
        #     if self.tableau[0][i] < 0:
        #         optimal = -1

        # if optimal:
        certificate = Simplex.get_certificate(self)
        optimal_value = Simplex.get_optimal_value(self)
        solution = Simplex.get_solution(self)
        print("otimo")
        print(optimal_value)
        print(' '.join(str(round(value, 7)) for value in solution))
        print(' '.join(str(round(value, 7)) for value in certificate))




    def verify_negative_b(self):
        b_negativo = False
        for i in range(1, self.number_restrictions_initial + 1):
            if(self.tableau[i][self.tableau.shape[1]-1] < 0):
                b_negativo = True
                self.tableau[i][0:self.tableau.shape[1]] = self.tableau[i][0:self.tableau.shape[1]] * (-1)


        return b_negativo


    def get_pl_aux(self):
        for i in range(self.number_restrictions_initial, self.tableau.shape[1]):
            self.tableau[0][i] = 0;

        aux_identity = np.identity(self.number_restrictions_initial, dtype=np.float)
        aux_top = np.full((self.number_restrictions_initial), 1)
        aux = np.vstack([aux_top, aux_identity])

        tableau_last_column = self.tableau[:, [-1]]
        tableau_without_last_column = self.tableau[:, :-1] 
        
        self.tableau = np.concatenate((tableau_without_last_column, aux), axis=1)
        self.tableau = np.concatenate((self.tableau, tableau_last_column), axis=1)

        for i in range(1, self.tableau.shape[0]):
            self.tableau[0, :] -= self.tableau[i, :]
        
        # print(">> Tableau aux")
        # print(self.tableau)



    def interpret_result_auxiliar(self):
        self.optmal_value_aux = Simplex.get_optimal_value(self)
        self.tipo = "indefinido"

        if(self.optmal_value_aux.round(10) < 0):
            self.tipo = "inviavel"
            self.certificado = Simplex.get_certificate(self)

        if(self.optmal_value_aux.round(10) == 0):
            self.tipo = "otimo"


    def tableau_optimal_pos_aux(self):
        j = 0
        for i in range(self.number_restrictions_initial, self.number_restrictions_initial+len(self.c_array_fpi)):
            self.tableau[0][i] = self.c_array_fpi[j] * (-1)
            j += 1

        for i in range(self.number_restrictions_initial+len(self.c_array_fpi), self.tableau.shape[1] - 1):
            self.tableau = np.delete(self.tableau, self.number_restrictions_initial+len(self.c_array_fpi), 1)

        for i in range(0, self.number_restrictions_initial):
            self.tableau[0][i] = 0


    def find_bases(self):
        basesIndex = []

        for i in range(self.number_restrictions_initial, self.tableau.shape[1] - self.number_restrictions_initial):
            # print("essa merda")
            # print(self.tableau[0][i])
            if self.tableau[0][i] == 0:
                index = np.where(self.tableau[:, i] == 1)
                index_ = np.where(self.tableau[:, i] == 0)
                # print("index")
                # print(index)
                if len(index[0]) == 1 and len(index_[0] == len(self.tableau[:, i]) - 1):
                    basesIndex.append(i)

        return basesIndex

    def return_unlimited(self, column):

        solucao = Simplex.get_solution(self)

        cert = np.zeros(self.tableau.shape[1])

        cert[column - self.number_restrictions_initial] = 1
        findBasesColumns = Simplex.find_bases(self)

        for base in findBasesColumns:
            for i in range(1, self.tableau.shape[0]):
                if self.tableau[i][base] == 1:
                    cert[base - self.number_restrictions_initial] = self.tableau[i][column] * (-1)

        cert = cert[:self.number_variables_initial]
        

        print('ilimitada')
        print(' '.join(str(round(value, 7)) for value in solucao))
        print(' '.join(str(round(value, 7)) for value in cert))
        quit()



    def pivoting(self):
        iteration = 0
        while 1:
            iteration += 1

            # print('>> Iteration: ', iteration);
            # print('Tableau: \n', np.around(self.tableau, 2))
            # print('Tableau: \n', self.tableau)

            column_to_pivot = Simplex.find_column_to_pivot(self)
            if column_to_pivot == -1:
                # print("SAIU DO WHILE PQ NAO TEM COLUNAAAA")
                break;

            row_to_pivot = Simplex.find_row_to_pivot(self, column_to_pivot)
            if row_to_pivot == -1:
                Simplex.return_unlimited(self, column_to_pivot)
                # break;

            pivot_index = (row_to_pivot, column_to_pivot)

            # print(">> PIVOTEANDO: ", pivot_index)

            Simplex.pivot(self, pivot_index)


    
    def solve_optimal_pl(self):
        Simplex.tableau_optimal_pos_aux(self)
        
        Simplex.pivoting(self)

        # print('>> Término:')
        # print('Tableau: \n', self.tableau)
        Simplex.interpret_result(self)


    def solve(self):
        b_negativo = Simplex.verify_negative_b(self)
        # Simplex.return_unlimited(self)
        if b_negativo:
            Simplex.get_pl_aux(self)
            Simplex.pivoting(self)
            Simplex.interpret_result_auxiliar(self)

            if(self.tipo == "inviavel"):
                print(self.tipo)
                print(' '.join(str(round(value, 7)) for value in self.certificado))
                quit()

            if(self.tipo == "otimo"):
                # print(self.tipo)
                Simplex.solve_optimal_pl(self)
        else:
            Simplex.pivoting(self)
            Simplex.interpret_result(self)