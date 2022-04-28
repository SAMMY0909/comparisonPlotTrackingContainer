import h5py
import matplotlib.pyplot as plt
import numpy as np
import glob
import tables as tb
from h5py import File
import os

input_file_std = "/home/sammy/eos/user/s/sgoswami/public/NN_SRC_DATA/ttbar/std/refined_std_tightuser.sgoswami.28416367._000243.output.h5"

stndrd_l = 0
stndrd_c = 0
stndrd_b = 0

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

l_tracks_std = 0
c_tracks_std = 0
b_tracks_std = 0


with File(input_file_std, 'r') as h5file:
  tracks = h5file['tracks_from_jet']
  #tracks = h5file['tracks']
  jets = h5file['jets']

  ljets = (jets["HadronConeExclTruthLabelID"] == 0).nonzero()[0]
  cjets = (jets["HadronConeExclTruthLabelID"] == 4).nonzero()[0]
  bjets = (jets["HadronConeExclTruthLabelID"] == 5).nonzero()[0]

  l_tracks_std = tracks[ljets,:]
  c_tracks_std = tracks[cjets,:]
  b_tracks_std = tracks[bjets,:]

  rownum_l,colnum_l=l_tracks_std.shape
  rownum_c,colnum_c=c_tracks_std.shape
  rownum_b,colnum_b=b_tracks_std.shape
  
  print("The dimensions of the l array for std container is, after cuts:" +str(rownum_l)+"by"+str(colnum_l))
  print("The dimensions of the c array for std container is, after cuts:" +str(rownum_c)+"by"+str(colnum_c))
  print("The dimensions of the b array for std container is, after cuts:" +str(rownum_b)+"by"+str(colnum_b))
o

os.makedirs("combSTD_new",exist_ok=True)
os.chdir('combSTD_new')

for vartype in variables:
  print("The vartype is: "+ vartype+ "\n")
  for var in variables[vartype]:
    print("The var is: "+ var +"\n")
    stndrd_l = l_tracks_std[l_tracks_std["valid"] == 1][var]
    stndrd_c = c_tracks_std[c_tracks_std["valid"] == 1][var]
    stndrd_b = b_tracks_std[b_tracks_std["valid"] == 1][var]
    
    plt.clf()
    
    plt.hist(stndrd_l, color = ['r'], bins = Bins[var], histtype='step', alpha=0.5, density=True, label="ttbar STD corr to l-jets")
    plt.hist(stndrd_c, color = ['b'], bins = Bins[var], histtype='step', alpha=0.5, density=True, label="ttbar STD corr to c-jets")
    plt.hist(stndrd_b, color = ['g'], bins = Bins[var], histtype='step', alpha=0.5, density=True, label="ttbar STD corr to b-jets")
    
    plt.legend(loc='upper right',fontsize=10,framealpha=0.2)
    plt.xlabel(var, size=14)
    plt.ylabel("Normalized distribution (Method=density)", size=14)
    plt.savefig(var + '_combined_std.png')
    print("Savefig block done for "+var+".\n")
