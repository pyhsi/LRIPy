def proxnormrast(Z,r,p,gamma,mode = None,search = {"t": 1, "s": 1, "k": 1}, init ={"t": 1, "s": 0,"k": 1},tol = 1e-12):
    """
    Prox of low-rank inducing Frobenius and spectral norm for 
    integer-valued r. 
    
    X,final = PROXNORMRAST(Z,r,p,gamma) produces the prox of the low-rank 
    inducing norm gamma*||.||_{ell_p,r*} evaluated in Z for 
    integer-valued r > 0, i.e., 
    a) X is the solution to the optimization problem: 
        
        minimize_X gamma*||X||_{ell_p,r*} + 0.5*||X-Z||_{ell_2}^2,

    where p=2 or p='inf'.
    b) final["t"] and final["s"] are the final values of parameters to the two 
    nested search. For p = 'inf', final["k"] is the final value of the third inner 
    search parameter. 
    If ||Z||_{ell_p^D,r} <= gamma, then t = s = k = None. 

    ... = PROXNORMRAST(Z,r,p,gamma,option) allows us to specify furhter options:
        1. ... = PROXNORMRAST(Z,r,p,...,mode = 'vec') is used to flag that the
        vector-valued problem is to be solved.
        2. ... = PROXNORMRAST(Z,r,p,gamma,tol = tol_val) sets the relative
        tolerance of the deciding about zeros e.g. if Z is matrix then
        for all i: sigma(X)_i = 0 if |sigma(X)_i| <= tol_val*||Z||_{ell_p,r). 
        Default value: tol_val = 1e-12.
        3. ... = PROXNORMRAST(Z,r,p,gamma,...,search = search_val) changes 
        from default binary search to linear search over
        a) t if search_val["t"] = 0.
        b) s if search_val["s"] = 0.
        c) k if search_val["k"] = 0 (only for p = 'inf').
        4. ... = PROXNORMRAST(Z,r,p,gamma,...,init = init_val) changes 
        from default binary search start values t_0 = 1, k_0 = 1, s_0 = 0
        to 
        a) t_0 if init_val["t"] = t_0.
        b) s_0 if init_val["s"] = s_0.
        c) k_0 if init_val["k"] = k_0 (only for p = 'inf').

    ---------------
    References:
    - C. Grussler and A. Rantzer and P. Giselsson (2018): 
    "Low-Rank Optimization with Convex Constraints", 
    IEEE Transactions on Automatic Control, DOI: 10.1109/TAC.2018.2813009.

    - C. Grussler and P. Giselsson (2016):
    "Low-Rank Inducing Norms With Optimality Interpreations", 
    arXiv:1612.03186v1.

    - C. Grussler and P. Giselsson (2017):
    "Local convergence of proximal splitting methods for rank constrained
    problems", pp. 702-708, IEEE 56th Annual Conference on Decision and Control
    (CDC), DOI: 10.1109/CDC.2017.8263743.

    - C. Grussler (2017):
    "Rank reduction with convex constraints", PhD Thesis, 
    Department of Automatic Control, Lund Institute of Technology, 
    Lund University, ISBN 978-91-7753-081-7.
    """
    
    import numpy as np
    from lripy.projrnorm import projrnorm

    ## Check if p = 2 or p = 'inf'
    if p != 2 and p !='inf':
        raise ValueError("p can only be equal to 2 or inf")

    ## Check options
    dim = Z.shape
    max_mn = np.max(dim)
    min_mn = np.min(dim)

    ## Check dimensions
    if mode == 'vec':
        if r > max_mn:
            raise ValueError("r is larger than max(Z.shape)")
    elif r > min_mn:
            raise ValueError("r is larger than min(Z.shape)")


    if p == 'inf':
        p = 1 # p for dual norm

    if mode == 'vec': 
        ## Vector valued problem
        # Moreau decomposition
        Y,_,final = projrnorm(Z,None,r,p,gamma,search,init,tol)
        X = Z - Y
    else:
        ## Matrix valued problem
        U,S,V = np.linalg.svd(Z,full_matrices=False)
        y,_,final = projrnorm(S,None,r,p,gamma,search,init,tol)
        # Moreau decomposition
        S = S - y
        X = U.dot(np.diag(S)).dot(V)

    return X,final