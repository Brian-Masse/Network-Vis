

import numpy as np

percs = np.asarray( [[100, 20, 30],
                    [20, 100, 70],
                    [30, 70, 100]])

percs = np.divide( percs, 100 )

positions = np.asarray( [[2],
                        [4],
                        [1]] )

new_matrix = np.asarray( [ percs.diagonal() ] )
test = np.transpose(new_matrix)
print(test)








    