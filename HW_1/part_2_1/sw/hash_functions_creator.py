import random
import math


################################################
num_hash_functions = 1120
upper_bound_on_number_of_distinct_terms  = 10000000
#upper_bound_on_number_of_distinct_terms =   138492
#upper_bound_on_number_of_distinct_terms =  3746518
Hash_functions_file = 'hash_functions_file'

################################################


### primality checker
def is_prime(number):
	for j in range(2, int(math.sqrt(number)+1)):
		if (number % j) == 0: 
			return False
	return True

with open(Hash_functions_file,'w+') as file:
	file.write("a	b	p	n \n")
	for hash_function_id in range(num_hash_functions):
		a = random.randint(1, upper_bound_on_number_of_distinct_terms-1)
		b = random.randint(0, upper_bound_on_number_of_distinct_terms-1)
		p = random.randint(upper_bound_on_number_of_distinct_terms, 10*upper_bound_on_number_of_distinct_terms)
		while is_prime(p) == False:
			p = random.randint(upper_bound_on_number_of_distinct_terms, 10*upper_bound_on_number_of_distinct_terms)
		file.write(str(a) + "\t" + str(b) + "\t" + str(p) + "\t" + str(upper_bound_on_number_of_distinct_terms)+ '\n')
	file.close()