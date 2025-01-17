import numpy as np
# from Coordinates import Decimal2RA,Decimal2Dec
from multiprocessing import Pool
import os
import h5py

def get_col_headers():
    #
    # Gaia EDR3 Column headers
    #
    # 0 ['RA']
    # 1 ['Dec']
    # 2 ['Epoch']
    # 3 ['ErrRA']
    # 4 ['ErrDec']
    # 5 ['Plx']
    # 6 ['ErrPlx']
    # 7 ['PMRA']
    # 8 ['ErrPMRA']
    # 9 ['PMDec']
    # 10 ['ErrPMDec']
    # 11 ['RA_Dec_Corr']
    # 12 ['NobsAst']
    # 13 ['ExcessNoise']
    # 14 ['ExcessNoiseSig']
    # 15 ['Chi2Ast']
    # 16 ['DofAst']
    # 17 ['NGphot']
    # 18 ['Mag_G']
    # 19 ['ErrMag_G']
    # 20 ['Mag_BP']
    # 21 ['ErrMag_BP']
    # 22 ['Mag_RP']
    # 23 ['ErrMag_RP']
    # 24 ['BPRP_Excess']
    # 25 ['RV']
    # 26 ['ErrRV']
    # 27 ['Teff']
    # 28 ['LogG']
    # 29 ['FeH']
    colcellfilename = "GAIAEDR3_htmColCell.mat"
    import scipy.io as sio
    data = sio.loadmat(colcellfilename)
    for i,k in enumerate(data['ColCell'][0]):
        print(i,k)
    return()

def runfile(filename):
  #
  # Create an output file containing data from Gaia based on constraints defined in the "index" variable.
  # The gaia3_output.txt file is then used to create a Color-Magnitude diagram.
  #
    path = '/lustre/research/kupfer/catalogs/GAIA/DRE3/'
    with open('gaia3_output.txt', 'a') as ofile:
        with h5py.File(f"{path}{filename}", "r") as hfile: # Standard read-in of .hdf5 files using h5py
            for i,k in enumerate(hfile):
                if "Ind" in k: # Not sure what these "_Ind" subfiles are. Ignoring for now.
                    continue
                subdata = hfile[k]
                try:
                  ra, dec = subdata[0],subdata[1]
                  plx = subdata[5]; plx_err = subdata[6]
                  gmag = subdata[18]; gmag_err = subdata[19]
                  bpmag = subdata[20]; bpmag_err = subdata[21]
                  rpmag = subdata[22]; rpmag_err = subdata[23]
                  fitast = subdata[15] / subdata[16]
                  index = np.where((plx>8) & (fitast>0.5) & (fitast<12.0) & (plx/plx_err>5) & (np.logical_not(np.isnan(bpmag-rpmag))))[0]
                except:
                  continue

                for l in index:
                    ofile.write(f'{plx[l]} {plx_err[l]} {gmag[l]} {gmag_err[l]} {bpmag[l]-rpmag[l]} {np.sqrt((bpmag_err[l])**2 + (rpmag_err[l])**2)}\n')



if __name__ == "__main__":
  edr3_files = [k for k in os.listdir('/lustre/research/kupfer/catalogs/GAIA/DRE3/') if "GAIAEDR3_" in k and ".hdf5" in k]
  #edr3_files = ['GAIAEDR3_htm_498200.hdf5']

  pool = Pool(32) # Hard-coded to use 1 core for login-node use. I used 32 cores and submitted the job to quanah to speed it up.
  result = pool.map(runfile, edr3_files)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
