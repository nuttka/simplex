from input_treatment import *
from simplex import *


def main():
    number_restrictions, number_variables, c_array_initial, a_matrix_initial, b_array_initial = get_input()

    simplex = Simplex(number_restrictions, number_variables, c_array_initial, a_matrix_initial, b_array_initial);

    # a_matrix, c_array, number_variables = Simplex.FPI_form(number_restrictions, c_array, a_matrix)
    # tableau = Simplex.tableau(a_matrix, b_array, c_array, number_restrictions, number_variables)
    # Simplex.solve(tableau, number_restrictions, c_array)

    simplex.FPI_form()
    simplex.tableau()
    simplex.solve()



# ----------


# MAIN
if __name__ == "__main__":
    main()