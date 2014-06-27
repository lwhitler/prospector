import numpy as np
from scipy.optimize import minimize


class Pminimize(object):
    
    def __init__(self, chi2, method, opts, model, pool = None, nthreads =1):
        self.method = method
        self.opts = opts
        self.model = model
        self._size = None
        #self.threads = nthreads

        self.minimize = _function_wrapper(minimize, [chi2, model, method, opts])
        
        self.pool = pool
        if nthreads > 1 and self.pool is None:
            self.pool = multiprocessing.Pool(nthreads)
            self._size = nthreads
            #print(self._size)
        #print(self.size)
    def run(self, pinit):

        if self.pool is not None:
            M = self.pool.map
        else:
            M = map

        results = list( M(self.minimize,  [np.array(p) for p in pinit]) )
        return results

    @property
    def size(self):
        if self.pool is None:
            return 1
        elif self._size is not None:
        #    print('uhoh')
            return self._size
        else:
            return self.pool.size
    

class _function_wrapper(object):
    """
    This is a hack to make the likelihood function pickleable when ``args``
    are also included.

    """
    def __init__(self, f, args):
        self.f = f
        self.args = args

    def __call__(self, x):
        try:
            return self.f(self.args[0], x, args = (self.args[1],),
                          method = self.args[2], options = self.args[3])
        except:
            import traceback
            print("minimizer: Exception while calling your likelihood function:")
            print("  params:", x)
            print("  args:", self.args)
            print("  exception:")
            traceback.print_exc()
            raise