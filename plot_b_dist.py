import h5py
import matplotlib.pyplot as plt
import numpy as np
import glob
import tables as tb
from h5py import File
import os

input_file_std = "/home/sammy/eos/user/s/sgoswami/public/NN_SRC_DATA/ttbar/std/refined_std_tightuser.sgoswami.28416367._000237.output.h5"
input_file_lrt = "/home/sammy/eos/user/s/sgoswami/public/NN_SRC_DATA/ttbar/lrt/refined_lrt_tightuser.sgoswami.28415580._000203.output.h5"


stndrd = 0
lrt = 0

Bins = {
  "numberOfInnermostPixelLayerHits" : np.arange(5),
  "numberOfNextToInnermostPixelLayerHits": np.arange(5),
  "numberOfInnermostPixelLayerSharedHits": np.arange(5),
  "numberOfInnermostPixelLayerSplitHits" : np.arange(5),
  "numberOfPixelHits" : np.arange(10),
  "numberOfPixelHoles": np.arange(10),
  "numberOfPixelSharedHits" : np.arange(10),
  "numberOfPixelSplitHits"  : np.arange(10),
  "numberOfSCTHits" : np.arange(30),
  "numberOfSCTHoles": np.arange(30),
  "numberOfSCTSharedHits" : np.arange(30),
  "expectNextToInnermostPixelLayerHit" : np.arange(5),
  "expectInnermostPixelLayerHit" : np.arange(5),
  "radiusOfFirstHit" : np.arange(0, 150, 10),
  "chiSquared" : np.arange(0, 50, 5),
  "numberDoF" : np.arange(0, 50, 5),
  "ptfrac": np.arange(0, 1, 10),
  "pt"  : np.arange(0, 10000, 500),
  "eta" : np.arange(-3, 3, 0.1),
  "deta" : np.arange(0, 6, 0.1),
  "dphi" : np.arange(0, 5, 0.1),
  "theta" : np.arange(0, 5, 0.1),
  "dr" : np.arange(0, 5, 0.1),
  "qOverP" : np.arange(0, 0.001, 0.0001),
  "qOverPUncertainty" : np.arange(0, 0.001, 0.0001),
  "phiUncertainty" : np.arange(0, 5, 0.1),
  "thetaUncertainty" : np.arange(0, 5, 0.1),
  "IP3D_signed_d0" : np.arange(-10, 10, 1),
  "IP2D_signed_d0" : np.arange(-10, 10, 1),
  "IP3D_signed_z0" : np.arange(-30, 30, 1),
  "d0" : np.arange(-10, 10, 1),
  "z0SinTheta" : np.arange(-30, 30, 1),
  "d0Uncertainty" : np.arange(-1, 1, 0.1),
  "z0SinThetaUncertainty" :  np.arange(-3, 3, 0.1),
  "IP3D_signed_d0_significance" : np.arange(-30, 30, 1),
  "IP3D_signed_z0_significance" : np.arange(-50, 50, 1),
  "z0RelativeToBeamspot": np.arange(-50, 50, 1),
  "z0RelativeToBeamspotUncertainty" : np.arange(-5, 5, 0.1),
}

variables = {
    "hits": [
        "numberOfInnermostPixelLayerHits",
        "numberOfNextToInnermostPixelLayerHits",
        "numberOfInnermostPixelLayerSharedHits",
        "numberOfInnermostPixelLayerSplitHits",
        "numberOfPixelHits",
        "numberOfPixelHoles",
        "numberOfPixelSharedHits",
        "numberOfPixelSplitHits",
        "numberOfSCTHits",
        "numberOfSCTHoles",
        "numberOfSCTSharedHits",
        "expectNextToInnermostPixelLayerHit",
        "expectInnermostPixelLayerHit",
        "radiusOfFirstHit",
    ],
    "quality": [
        "chiSquared",
        "numberDoF",
        "ptfrac",
    ],
    "kine": [
        "pt",
        "eta",
        "deta",
        "dphi",
        "theta",
        "dr",
        "qOverP",
        "qOverPUncertainty",
        "phiUncertainty",
        "thetaUncertainty",
    ], 
    "ips": [
        "IP3D_signed_d0",
        "IP2D_signed_d0",
        "IP3D_signed_z0",
        "d0",
        "z0SinTheta",
        "d0Uncertainty",
        "z0SinThetaUncertainty",
        "IP3D_signed_d0_significance",
        "IP3D_signed_z0_significance",
        "z0RelativeToBeamspot",
        "z0RelativeToBeamspotUncertainty"
    ], 
}

b_tracks_std = 0
b_tracks_lrt = 0

with File(input_file_std, 'r') as h5files:
    tracks = h5files['tracks_from_jet']
    #tracks = h5files['tracks']
    jets = h5files['jets']
    bjets = (jets["HadronConeExclTruthLabelID"] == 5).nonzero()[0]
    b_tracks_std = tracks[bjets,:]
    rownum,colnum=b_tracks_std.shape
    print("The dimensions of the array for std container is, after cuts: " +str(rownum)+" by "+str(colnum))

with File(input_file_lrt, 'r') as h5filel:
    tracks = h5filel['tracks_from_jet']
    #tracks = h5filel['tracks']
    jets = h5filel['jets']
    bjets = (jets["HadronConeExclTruthLabelID"] == 5).nonzero()[0]
    b_tracks_lrt = tracks[bjets,:]
    rownum,colnum=b_tracks_lrt.shape
    print("The dimensions of the array for std+LRT container is, after cuts: " +str(rownum)+" by "+str(colnum))

os.makedirs('bplots_new',exist_ok = True)
os.chdir('bplots_new')

for vartype in variables:
    print("The vartype is: "+ vartype+ "\n")
    for var in variables[vartype]:
        print("The var is: "+ var +"\n")
        stndrd = b_tracks_std[b_tracks_std["valid"] == 1][var]
        lrt = b_tracks_lrt[b_tracks_lrt["valid"] == 1][var]
            
        plt.clf()
        fig,ax=plt.subplots(2,1,sharex=True)
            
        val_of_bins_x1, edges_of_bins_x1, patches_x1=ax[0].hist(stndrd, color = ['r'], bins = Bins[var], histtype='stepfilled', alpha=0.5, density=True, label="ttbar STD corr to b-jets")
        val_of_bins_x2, edges_of_bins_x2, patches_x2=ax[0].hist(lrt, color = ['g'], bins = Bins[var], histtype='stepfilled', alpha=0.5, density=True, label="ttbar STD+LRT corr to b-jets")
            
        pltratio = np.true_divide(val_of_bins_x2,val_of_bins_x1,where=(val_of_bins_x1 != 0))
        plterror = np.true_divide(val_of_bins_x1 * np.sqrt(val_of_bins_x2) + val_of_bins_x2 * np.sqrt(val_of_bins_x1),np.power(val_of_bins_x2, 2),where=(val_of_bins_x1 != 0))
            
        bincenter = 0.5 * (edges_of_bins_x1[1:] + edges_of_bins_x1[:-1])
            
        ax[0].legend(loc='upper right',fontsize=10,framealpha=0.2)
        #ax[0].set_xlabel(var, size=10)
        ax[0].set_ylabel("Normalized distribution \n (Method=density)", size=10)
        
        ax[1].errorbar(bincenter, pltratio, yerr=None, fmt='k.')
        ax[1].grid(True)
        ax[1].set_xlabel(var, size=10)
        ax[1].set_ylabel("Ratio", size=10)
         
        plname=str(var)+'_bottom.png'
        fig.tight_layout()
        fig.savefig(plname,bbox_inches="tight")
        print("Savefig block done for "+var+".\n")
