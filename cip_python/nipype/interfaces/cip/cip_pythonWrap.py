import sys
sys.path.append("/Users/rolaharmouche/ChestImagingPlatform/")
sys.path.append("/Users/rolaharmouche/ChestImagingPlatform/cip_python/")

import os
import nrrd
import nibabel as nb
import numpy as np
from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec
from nipype.utils.filemanip import split_filename
from cip_python.phenotypes.parenchyma_phenotypes import ParenchymaPhenotypes
from cip_python.phenotypes.body_composition_phenotypes import BodyCompositionPhenotypes




# example http://nipy.sourceforge.net/nipype/devel/python_interface_devel.html

class parenchyma_phenotypesInputSpec(BaseInterfaceInputSpec):
    in_ct = File(exists=True, desc='Input CT file', mandatory=True)
    in_lm = File(exists=True, desc='Input label map containing structures of interest', mandatory=True)
    out_csv = File( desc='Output csv file in which to store the computed \
                   dataframe', mandatory=True)
    cid = traits.Str(desc='The database case ID',
                     mandatory=True)
    chest_regions = traits.Str(desc='Chest regions',
                mandatory=False)
        #chest_types = traits.Str(desc='Chest types',
    #                     mandatory=False)
        #pairs = traits.Str(desc='Chest region/type pairs',
    #                    mandatory=False)
    pheno_names = traits.Str(desc='Phenotype names',
                           mandatory=False)
    out_csv = File( desc='Output csv file in which to store the computed \
                   dataframe', mandatory=False)
class parenchyma_phenotypesOutputSpec(TraitedSpec):
    out_csv = File( desc='Output csv file in which to store the computed \
                   dataframe', mandatory=False)

class parenchyma_phenotypes(BaseInterface):
    input_spec = parenchyma_phenotypesInputSpec
    output_spec = parenchyma_phenotypesOutputSpec
    
    def _run_interface(self, runtime):
        
        lm, lm_header = nrrd.read(self.inputs.in_lm)
        ct, ct_header = nrrd.read(self.inputs.in_ct)
    
        spacing = np.zeros(3)
        spacing[0] = ct_header['space directions'][0][0]
        spacing[1] = ct_header['space directions'][1][1]
        spacing[2] = ct_header['space directions'][2][2]
    
        #regions = None
        #print(self.inputs.chest_regions)
            #if self.inputs.chest_regions is not None:
        #regions = self.inputs.chest_regions.split(',')
        #types = None
            #if self.inputs.chest_types is not None:
        #types = self.inputs.chest_types.split(',')
        #pairs = None
            #if self.inputs.options.pairs is not None:
            #tmp = pairs.split(',')
            #assert len(tmp)%2 == 0, 'Specified pairs not understood'
            #pairs = []
                #for i in xrange(0, len(tmp)/2):
                #pairs.append([tmp[2*i], tmp[2*i+1]])
        pheno_names = None
        if self.inputs.pheno_names is not None:
            pheno_names = self.inputs.pheno_names.split(',')
    
        paren_pheno = ParenchymaPhenotypes(chest_regions=self.inputs.chest_regions,
                                       chest_types=None, pairs=None, pheno_names=pheno_names)
    
        df = paren_pheno.execute(ct, lm, self.inputs.cid, spacing)
    
        if self.inputs.out_csv is not None:
            df.to_csv(self.inputs.out_csv, index=False)
        
        
        
#fname = self.inputs.volume
#       img = nb.load(fname)
#        data = np.array(img.get_data())
        
#        active_map = data > self.inputs.threshold
        
#        thresholded_map = np.zeros(data.shape)
#        thresholded_map[active_map] = data[active_map]
        
#        new_img = nb.Nifti1Image(thresholded_map, img.get_affine(), img.get_header())
#        _, base, _ = split_filename(fname)
#        nb.save(new_img, base + '_thresholded.nii')
        
        return runtime
    
    def _list_outputs(self):
        outputs = self._outputs().get()
        fname = self.inputs.out_csv
        _, base, _ = split_filename(fname)
        outputs["out_csv"] = os.path.abspath(fname)
        return outputs




"""
Body composition phenotyopes
"""

class body_composition_phenotypesInputSpec(BaseInterfaceInputSpec):
    in_ct = File(exists=True, desc='Input CT file', mandatory=True)
    in_lm = File(exists=True, desc='Input label map containing structures of interest', mandatory=True)
    out_csv = File( desc='Output csv file in which to store the computed \
                   dataframe', mandatory=True)
    cid = traits.Str(desc='The database case ID',
                     mandatory=True)
    chest_regions = traits.Str(desc='Chest regions',
                               mandatory=False)
    chest_types = traits.Str(desc='Chest types',
                         mandatory=False)
    pairs = traits.Str(desc='Chest region/type pairs',
                        mandatory=False)
    pheno_names = traits.Str(desc='Phenotype names',
                             mandatory=False)

class body_composition_phenotypesOutputSpec(TraitedSpec):
    out_csv = File( desc='Output csv file in which to store the computed \
                   dataframe', mandatory=False)

class body_composition_phenotypes(BaseInterface):
    input_spec = parenchyma_phenotypesInputSpec
    output_spec = parenchyma_phenotypesOutputSpec
    
    def _run_interface(self, runtime):
        
        lm, lm_header = nrrd.read(self.inputs.in_lm)
        ct, ct_header = nrrd.read(self.inputs.in_ct)
        
        spacing = np.zeros(3)
        spacing[0] = ct_header['space directions'][0][0]
        spacing[1] = ct_header['space directions'][1][1]
        spacing[2] = ct_header['space directions'][2][2]
        
        #regions = None
        #print(self.inputs.chest_regions)
        #if self.inputs.chest_regions is not None:
        #regions = self.inputs.chest_regions.split(',')
        #types = None
        #if self.inputs.chest_types is not None:
        #types = self.inputs.chest_types.split(',')
        #pairs = None
        #if self.inputs.options.pairs is not None:
        #tmp = pairs.split(',')
        #assert len(tmp)%2 == 0, 'Specified pairs not understood'
        #pairs = []
        #for i in xrange(0, len(tmp)/2):
        #pairs.append([tmp[2*i], tmp[2*i+1]])
        pheno_names = None
        if self.inputs.pheno_names is not None:
            pheno_names = self.inputs.pheno_names.split(',')
        
        body_pheno = BodyCompositionPhenotypes(chest_regions=self.inputs.chest_regions,
                                           chest_types=None, pairs=None, pheno_names=pheno_names)
        
        df = body_pheno.execute(ct, lm, self.inputs.cid, spacing)
        
        if self.inputs.out_csv is not None:
            df.to_csv(self.inputs.out_csv, index=False)
        
        
        
        #fname = self.inputs.volume
        #       img = nb.load(fname)
        #        data = np.array(img.get_data())
        
        #        active_map = data > self.inputs.threshold
        
        #        thresholded_map = np.zeros(data.shape)
        #        thresholded_map[active_map] = data[active_map]
        
        #        new_img = nb.Nifti1Image(thresholded_map, img.get_affine(), img.get_header())
        #        _, base, _ = split_filename(fname)
        #        nb.save(new_img, base + '_thresholded.nii')
        
        return runtime
    
    def _list_outputs(self):
        outputs = self._outputs().get()
        fname = self.inputs.out_csv
        _, base, _ = split_filename(fname)
        outputs["out_csv"] = os.path.abspath(fname)
        return outputs
