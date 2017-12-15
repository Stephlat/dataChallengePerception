import numpy as np
from munkres import Munkres, print_matrix
from utils import euclidean_pose_distance, cost_matrix


''' Compute CLEAR metrics for multi pose tracking as in Stiefelhagen R., Bernardin K., Bowers R., Garofolo J., Mostefa D., Soundararajan P. (2007) The CLEAR 2006 Evaluation, and SA (speaking activity accuracy)
    -- Inputs
    * obs stands for groud truth observation, a numpy array such as the column are in the following order : (time or idFrame) (Id) (Speaking Activity) (Joint1.x) (Joint1.y) ...
    * hyp stands for hypothesis (tracking result to be evaluated), in the same format as obs
    * Thres is the threshold value controling if a match (obs,hyp) is valid
    * d is the distance function between hyp and obs to be matched
    -- Outputs
    * Corresponding tuple (MOTA,MOTP,SA)
'''
def compute_clear(obs, hyp, Thr, d = euclidean_pose_distance):

    obs_original = obs.copy()
    hyp_original = hyp.copy()

    # removing speaking info first, for clarity
    obs = np.delete(obs,2,1)
    hyp = np.delete(hyp,2,1)
    T = int(np.max(obs[:,0]))
    M = []
    M0 = {}
    M.append(M0) # Matches : i being a hypothesis identity, M[t][i] gives the corresponding hypothesis identity at t
    mme = [0.0] # mismatch errors
    fp = [0.0] # FPs, hyp not matched by any obs
    g = [0.0] # number of GTs
    misses = [0.0] # Misses, obs not matched by any hyp at t
    c = [0.0] # number of matches at t
    ds = 0.0 # sum of all the distance obs-hyp matched
    for t in range(1,T):
        # filtering current observations and hypothesis
        obst = obs[(obs[:,0] == t)]
        hypt = hyp[(hyp[:,0] == t)]
        # initializing variables
        m = {}
        mmet = 0.0
        ct = 0.0
        g.append(len(obst))
        # o -> h
        
        # getting Ids to process 
        obs_id = list(obst[:,1])
        hyp_id = list(hypt[:,1])
        
        obs_id = [int(i) for i in obs_id]
        hyp_id = [int(i) for i in hyp_id]
        ## 1st step, checking if former matches are still valid
        for i in M[t-1].keys(): # going through past matched hypothesis' identities i
            if i in obst[:,1] and M[t-1][i] in hypt[:,1]: # if i is still visible (in observations) and its matched hypothesis still exists
                # taking their corresponding coordinates
                ox = obst[np.squeeze(np.where(obst[:,1] == i)),2:]
                hx = hypt[np.squeeze(np.where(hypt[:,1] == M[t-1][i])),2:]
                # computing distance between them, keeping match if d below Thr
                if d(ox,hx) < Thr:
                    m[i] = M[t-1][i]
                    obs_id.remove(i)
                    hyp_id.remove(M[t-1][i])
                    ct += 1
                    ds += (d(ox,hx))

        ## 2nd step, creating optimal matches thanks to the Hungarian algo
        
        # getting remaining Ids' to match coordinates
        obsx = []
        hypx = []
        for i in obs_id:
            obsx.append(obst[np.squeeze(np.where(i == obst[:,1])), 2:])
        for i in hyp_id:
            hypx.append(hypt[np.squeeze(np.where(i == hypt[:,1])), 2:])

        hypx = np.array(hypx)
        obsx = np.array(obsx)

        if len(obsx)>0 and len(hypx)>0:
            # from their coordinates, and the distance, create the
            # cost matrix C , dim : (|obsx|,|hypx|)
            C = cost_matrix(obsx,hypx,d)
            # instantiating Hungarian solver (Munkre)
            munk = Munkres()
            indexes = munk.compute(C) # produces list of optimal matching (i,j) [obs,hyp]
            # save copy of lists for indexing purpose
            obs_id_c = list(obs_id)
            hyp_id_c = list(hyp_id)

            ## 3d step, compute stats
            for (i,j) in indexes:
                if C[i,j] <= Thr and i<len(obs_id_c)and j<len(hyp_id_c):
                    ct += 1
                    # If the current observation was previously matched (to a different hypothesis Id by #1 step)
                    # Add a mismatch error
                    if obs_id_c[i] in M[t-1].keys() and (hyp_id_c[j] != M[t-1][obs_id_c[i]]):
                        mmet += 1
                    m[obs_id_c[i]] = hyp_id_c[j]
                    ds += (C[i,j])
                    obs_id.remove(obs_id_c[i])
                    hyp_id.remove(hyp_id_c[j])

        ## 4th step : collecting statistics
        # False Positives are remaining hypothesis
        fp.append(len(hyp_id))
        # Misses are remaining observations
        misses.append(len(obs_id))

        mme.append(mmet)
        c.append(ct)
        M.append(m)

    fp = np.array(fp)
    misses = np.array(misses)
    mme = np.array(mme)
    c = np.array(c)

    MOTA = 1 - (np.sum(fp+misses+mme)/np.sum(g))
    MOTP = ds/np.sum(c)
    
    ## 5 : Speaking Activity computation
    obs = obs_original
    hyp = hyp_original
    
    SA = []
    SA_t = [0]
    for t in range(1,T):
        sa_t = 0
        obst = obs[(obs[:,0] == t)]
        hypt = hyp[(hyp[:,0] == t)]
        for i in M[t].keys():
            obsti_activity = (obst[np.squeeze(np.where(i == obst[:,1])), 2])
            hypti_activity = (hypt[np.squeeze(np.where(M[t][i] == hypt[:,1])), 2])
            if obsti_activity == hypti_activity:
                SA.append(1.0)
            else:
                SA.append(0.0)
                sa_t += 1
        SA_t.append(sa_t)
    SA_t = np.array(SA_t)
    SA = np.array(SA,dtype = np.float)
    SA = np.sum(SA)/len(SA)

    MOTSA = 1 - (np.sum(fp + misses+ mme + SA_t)/np.sum(g))
    return MOTA,MOTP,SA,MOTSA

if __name__ == '__main__':
    import sys
    from read_file import read_file
    from numpy.random import normal
    
    if len(sys.argv) != 3:
        raise Exception('wrong input files : should be \'python compute_clear.py #GT_file #HYPOTHESIS_file\'')

    # Reading input files
    print 'reading GT file'
    obs_file = str(sys.argv[1])
    print 'reading result file'
    hyp_file = str(sys.argv[2])
    obs = read_file(obs_file)
    hyp = read_file(hyp_file)

    if obs.shape[1] != hyp.shape[1]:
        raise Exception('coordinate mismatches : different number of columns between groundTruth and results')
    # Deleting speaking activity information
    #obs = np.delete(obs,2,1)
    #hyp = np.delete(hyp,2,1)

    # Adding noise for debugging purpose
    #noise = 1*normal(size = (hyp.shape[0],hyp.shape[1]-2))
    #hyp[:,2:] = hyp[:,2:] + noise
    #hyp[:,1] = np.array(noise[:,0], int) + hyp[:,1]
    MOTA, MOTP,SA,MOTSA = (compute_clear(obs, hyp, 25))
    print 'MOTA'
    print MOTA
    print 'MOTP'
    print MOTP
    print 'SA'
    print SA
    print 'MOTSA'
    print MOTSA
