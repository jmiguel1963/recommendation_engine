#Functions used to perform processing and mapping of feature values
import re
import numpy as np
import math
from sklearn.base import TransformerMixin
import pandas as pd
import configuration as config

# test if string value is a NaN value
def isNaN(string):
    return string != string

# test if string value is not a NaN value
def isnotNaN(string):
    return string==string

# find a string between 2 characters
def find_string_between(s,start,end):
    if start in s and end in s:
        s=s=re.sub(r"\xa0",'',s)
        return (s.split(start))[1].split(end)[0]
    else:
        return s

# find a string after a character
def find_string_after(s,start):
        return s.split(start)[1]

# processing wavelength values for coated and uncoated products
def cleaning_coating_wavelength(s):
    s=re.sub(r"um",'µm',s)
    s=re.sub(r"[\s+]",'',s)
    s=re.sub(r"nm-",'-',s)
    
    if '&' in s:
        s=re.sub(r"&"," & ",s)
    
    if 'µm' in s:
        
        if '(' in s:
            s=s.split('(')[0]
        s=re.sub(r"µm",'',s)
        
        if '-' in s:
            s1=s.split('-')[0]
            s2=s.split('-')[1]
            s1=float(s1)*1000
            s2=float(s2)*1000
            s=str(int(s1))+' - '+str(int(s2))
            return s
        
        else:
            s=float(s)*1000
            s=str(int(s))
            return s
    
    elif 'nm' in s:
        
        if '(' in s:
            s=s.split('(')[0]
        s=re.sub(r"nm",'',s)
        s=re.sub(r"-",' - ',s)
        return s
    
    else:
        s=re.sub(r",",'',s)
        s=re.sub(r"-",' - ',s)
        return s

# assignment of some special coated products wavelength
def wavelength_assignment(s):
    if s=='VIS-NIR':
        return '400 - 1000'
    elif s=='UV-VIS':
        return '250 - 700'
    elif s=='VIS':
        return '425 - 675'  

# processing of all circular products (diameter feature values)
def diameter_processing(s):
    
    if '&nbsp ' in s:
        s=s.split('&nbsp ')[1]
    s=s.replace('±','+')
    s=s.replace(',','.')
    s=s.replace('1/2','0.5')
    s=re.sub(r"\s+",'',s)
    for c in ['mm','Ø','φ','ø']:
        s=s.replace(c,'')
   
    if '+' in s and '"' not in s:
        s=s.split('+')[0]
        s=float(s)
        s=str(round(s, 2))
        return s
        
    elif '"' in s:
        s=s.split('"')[0]
        s=float(s)*25.4
        s=str(round(s, 2))
        return s
    
    else:
        s=float(s)
        s=str(round(s, 2))
        return s    

# processing of all square/rectangular products (dimensions and similar features values)
def square_rectangle_processing(s,polygon):
    
    if '&nbsp ' in s:
        s=(s.split('&nbsp ')[1]).split('UVFS')[0]
        s=s.replace(' mm','')
    
    if 'BK7' in s or 'Silica' in s:
        s=s.replace('Silica','BK7')
        if 'BK7' in s:
            s=(s.split('BK7 ')[1]).split('mm')[0]
    s=s.replace('±','+')
    s=s.replace('□','')
    s=s.replace('×','x')
    s=re.sub(r"\s+",'',s)
    s=s.replace('mm','')
    s=s.replace(',','.')
    
    if '+' in s:
        s=s.split('+')[0]
        s=s.strip()
    
    if 'x' in s:
        a=s.split('x')[0]   
        b=s.split('x')[1]
        a=float(a)
        b=float(b)
        if polygon=='square':
            if a==b:
                return str(round(a,2))
            else:
                return np.nan
        else:
            if a!=b:
                s=str(round(a,2))+' x '+str(round(b,2))
                return s
            else:
                return np.nan
    else:
        s=float(s)
        s=str(round(s,2))
        return s 

# processing of all 'elliptical' products
def minor_major_axis_processing(s):
    s=s.replace(',','.')
    s=s.replace('mm','')
    s=re.sub(r"\s+",'',s)
    if '+' in s:
        s=s.split('+')[0]
    s=float(s)
    s=str(round(s,2))
    
    return s

#processing of thickness feature values
def thickness_processing(s):
   
    if ' t ' in s:
        s=s.split('t = ')[1]
    if 'Thick' in s:
        s=(s.split('nm, ')[1]).split(' Thick')[0]
    s=re.sub(r"\s+",'',s)
    s=re.sub(r"T",'',s)
    s=s.replace('+','±')
    if '±' in s:
        s=s.split('±')[0]
    if '(' in s:
        s=s.split('(')[0]
    s=s.replace('-','')
    s=s.replace('mm','')
    s=s.replace(',','.')
    s=float(s)
    s=str(round(s,2))
    return s

#processing of curvature-radius feature values
def curvature_radius_processing(s):
    s=str(round(float(re.sub(r"[\s+,mm,+,-]",'',s)),2))
    return s

#processing of wedge angle feature values
def wedge_angle_processing(s):
    
    s=re.sub(r"\s+",'',s)
    if 'arcmin' in s:
        if '±' in s:
            s=s.split('±')[0]
        s=s.replace('arcmin','')
        s=round(float(s)/60.,2)
        s=str(s)
        return s
    
    if '±' in s and '°' in s:
        s=s.split('±')[0]
        s=s.replace('°','')
        return s
    
    degree=s.split('°')[0]
    degree=float(degree)
    minute=(s.split('°')[1]).strip().split("'")[0]
    
    if '"' in s:
        
        second=((s.split('°')[1]).strip().split("'")[1]).split('"')[0]
        total=60*float(minute)+float(second)
        remainding=total/3600.
        s=str(round(degree+remainding,2))
        return s
    
    else:
        
        remainding=float(minute)/60.
        s=str(round(degree+remainding,2))
        return s 

#processing of diffused angle feature values
def diffused_angle_processing(s):
    s=re.sub(r"[\s,(,),F,W,H,M]",'',s)
    return s

#processing of parallelism feature values
def parallelism_processing(s,angle_meas):
    s=re.sub(r"[\s,≤,<]",'',s)
    
    if '±' in s:
        s=s.split('±')[0]
    
    if 'arcmin' in s or 'arcsec' in s or 'min' in s or angle_meas=='arcmin' or angle_meas=='arcsec':
        if 'arcmin' in s or 'min' in s or angle_meas=='arcmin':
            s=re.sub(r"[arcmin,min]",'',s)
            s=round(float(s),2)
            s=str(s)
            return s
        elif 'arcsec' in s or angle_meas=='arcsec':
            s=re.sub(r"[arcsec]",'',s)
            s=round(float(s)/60.,2)
            s=str(s)
            return s
        
    if "′" not in s:
        s=re.sub(r"[″,'']",'',s)
        s=round(float(s)/60.,2)
        s=str(s)
        return s
    else:
        if '″' not in s and "''" not in s:
            s=s.replace("′",'')
            s=round(float(s),2)
            s=str(s)
            return s
        else:
            s1=s.split("′")[0]
            s2=(s.split("′")[1]).split('″')[0]
            s1=float(s1)
            s2=float(s2)/60.
            s=str(round(s1+s2,2))
            return s

#processing of surface flatness feature values
def flatness_processing(s):
    
    s=re.sub(r"\s+",'',s)
    s=s.replace('Entire','')
    s=s.replace('Full','')

    if 'over' in s:
        s=s.replace('over','Over')
    if 'mm' in s and 'Clear' in s:
        s=s.split('mm')[1]
    if '-' in s and len(s)<3:
        s=s.replace('-','λ/10')
    if 'Over' in s:
        s=s.split('Over')[0]
    if 'at' in s:
        s=s.split('at')[0]
    if '@' in s:
        s=s.split('@')[0]
    for c in ['<','≤',' over 25mm Aperture','(typical)','※','perinch']:
        s=s.replace(c,'')
    return s

#processing of surface quality feature values
def quality_processing(s):
    s=s.replace('Scratch','scratch')
    if 'scratch' in s:
        s=s.split(' scratch')[0]
    s=s.replace(' ','')
    return s

#processing of wavefront error feature values
def wavefront_error_processing(s):
    
    s=s.replace('over','Over')
    for c in ['Entire','Full','Over','(70% of Dia.)','per 25mm @ 633nm']:
        s=s.replace(c,'')
    s=re.sub(r"\s+|≤|≤±|±|<",'',s)
    
    if 'mm' in s and 'Clear' in s:
        s=(s.split('mm')[1]).split('Clear')[0]
    elif 'Clear' in s and 'mm' not in s:
        s=s.split('Clear')[0]
    if 'at' in s:
        s=s.split('at')[0]
    if '@' in s:
        s=s.split('@')[0]
    
    return s

#processing of reflectance of coated products
def reflectance_processing(s):
    
    s=re.sub(r"<|≥|>",'≤',s)
    s=s.replace(' Average','')
    
    if '@' in s:
        s_list=re.split('@',s)
        max_list=[]
        for i in range(len(s_list)-1):
            s_list[i]=((s_list[i].split('%')[0]).split('≤')[1]).strip()
            max_list.append(round(float(s_list[i]),2))
        s=max(max_list)
        return str(s)
    elif '≤' in s and len(s)<5:
        s=s.replace('≤','')
        s=s.strip()
        if '%' in s:
            s=s.replace('%','')
            s=100.-float(s)
        else:
            s=float(s)
        return str(round(s,2))
    elif 'Milky' in s:
        return np.nan
    elif '@' not in s:
        s_list=re.split('%',s)
        max_list=[]
        for i in range(len(s_list)-1):
            s_list[i]=s_list[i].split('≤')[1].strip()
            
            max_list.append(round(float(s_list[i]),2))
        s=max(max_list)
        return str(s)
    else:
        return np.nan

#processing of damagethreshold or similar features values
def damagethreshold_processing(s,c):
    if isnotNaN(c):
        if '-' not in c:
            s=re.sub(r'\s+','',s)
            if 'J' in s:
                s=s.split('J')[0]
                s=s.replace('>','')
                s=round(float(s),2)
                return str(s)
        else:
            return np.nan
    else:
        return np.nan

# mapping for reactangular products
# for comparing 2 different rectangles, we will calculate rectangle diagonal value.
def rectangle_value_mapping(s):
    s=re.sub(r"\s+",'',s)
    s1=s.split('x')[0]
    s1=float(s1)
    s2=s.split('x')[1]
    s2=float(s2)
    value=math.sqrt(s1**2+s2**2)
    return round(value,2)

# mapping for elliptical products
# for comparing 2 elliptical products, we will calculate diagonal of rectangle in which the ellipse is circunscrite
def elliptical_value_mapping(s1,s2):
    s1=re.sub(r"\s+",'',s1)
    s2=re.sub(r"\s+",'',s2)
    s1=float(s1)
    s2=float(s2)
    value=math.sqrt(s1**2+s2**2)
    return round(value,2)

#mapping of diffused angle
def circular_elliptical_angle_mapping(s):
    
    if 'x' not in s:
        s=float(s)/50
        return s
    else:
        if '0.2x40' in s:
            return float(4)
        
        elif '1x60' in s:
            return float(6)
        
        elif '5x30' in s:
            return float(8)
        
        elif '10x60' in s:
            return float(10)
        
#mapping of some opto mecanical products which have no substrate        
def special_component_mapping(s):
    
    if 'Fiber' in s or 'SMA' in s:
        return float(200)
    elif 'Brewster' in s:
        return float(400)
    else:
        return float(600)
    return

#mapping of aberration feature 
def aberration_mapping(s):
    s=re.sub("λ",'',s)
    s=(float(s)+1.0)
    return s

#mapping of surface quality processed feature
def surfacequality_mapping(s):
    if '10-5' in s:
        return float(20)
    elif '20-10' in s:
        return float(15)
    elif '40-20' in s:
        return float(10)
    elif '60-40' in s:
        return float(5)   
    else:
        return float(0)

#mapping of surface flatness processed feature    
def surfaceflatness_mapping(s):
    s=re.sub("λ",'',s)
    if '/' in s:
        s=re.sub("/",'',s)
        s=float(s)
        return s
    else:
        if '4-6' in s:
            return float(0.2)
        elif s=='':
            return float(1)
        else:
            return (1.0/float(s))

#mapping of wavefronterror processed feature
def wavefronterror_mapping(s):
    s=re.sub("λ",'',s)
    if '/' in s:
        s=re.sub("/",'',s)
        s=float(s)
        return s
    else:
        if s=='':
            return float(1)
        else:
            return (1.0/float(s)) 

#mapping of fiber products
def fibercomponent_mapping(s):
    s=re.sub('Ø2.75"','',s)
    if 'Ø' in s:
        s1=(s.split('Ø')[1]).split(' µm')[0]
        s1=float(s1)
        s2=(s.split('Core, ')[1]).split(' nm')[0]
        s3=float(s2.split(' - ')[0])
        s4=float(s2.split(' - ')[1])
        deltas=s4-s3
        
        if deltas==1000. or deltas==600.:
            return (float(5)+s1/20.)
        elif deltas==2000. or deltas==1800.:
            return (float(10)+s1/20.)   
    else:
        return float(100)

#mapping of flange products
def flangehardware_mapping(s):
    s=re.sub('Ø2.75"','',s)
    if 'Optics' in s:
        s=(s.split('Ø')[1]).split('"')[0]
        s=float(s)*10.
        return s
    else:
        return float(50)

#the following 3 funcions are combined to use a dictionnary to assign new values to initial values
#they are used as sentence swith case does not exist in python
def list_number_assignment(path,essential_list,count):
    result=False
    for test_str in essential_list:
        result=result or (test_str in path)
    return count*result 
        
def switch_assignment(number,switch):
    
    return switch.get(number,"Not_Available")

def feature_transformation(mystr,transformation_list,switch):
    
    total=0
    
    for i,inner_list in enumerate(transformation_list):
            
        total += list_number_assignment(mystr,inner_list,i+1)
    
    category=switch_assignment(total,switch)
    
    return category

#modification of description_supplier using 'breadcrumbs' feature as there is no information of Substrate
def description_supplier_modification(description,category_path):
    
    if 'Reasonable' in category_path:
        description=re.sub(r"Reasonable",'Reasonable BK7',description)
    elif 'Concave Mirror' in category_path:
        description=re.sub(r"Mirror",'Mirror BK7',description)
    elif 'Optical Flats' in category_path:
        if ('BK7' not in description) and ('silica' not in description):
            description=re.sub(r"Flat",'Flat Hard glass',description)
    elif 'Speckle' in category_path:
        description=re.sub(r"Speckle",'Speckle Optotune polymer',description)
    else:
        description=re.sub(r"Window",'Synthetic fused silica Window',description)
    return description

#creation of several classes based on TransformerMixin class (sklearn.base library)
#these classes will allow us to pipeline all dataframe processing

#these classes have 3 main functions:
# __init__ (initialize features lists)
#fit (define individual features from input lists)
#transform (transform individual features values to generate new features values)

#once classes are instantiated with parameters lists in pipeline function, function fit_transform generates 
# whole pipeline transformation

#Generation of correct dataframe shape
class DataFrameModification(TransformerMixin):
    
    def fit(self,df):
        
        return self
    
    def transform(self,df):
        #json file data extraction into a dataframe (features as indexes and products as columns)
        #dataframe transposition (products as indexes and features as columns)
        #product indexes transformation into integer indexes (Product is an additional feature)
        columns=list(df.columns.values)
        index=list(df.index.values)
        df_array_transpose=np.transpose(df.to_numpy())
        df=pd.DataFrame(data=df_array_transpose,index=columns,columns=index)
        df=df.reset_index()
        df.columns = ['Product' if x=='index' else x for x in df.columns]
        
        return df

#Generation of 'FeatureApplicationProcessed' feature
class FeatureApplicationCreation(TransformerMixin):
    
    def __init__(self,ProcessedFeaturesList,ApplicationList,ApplicationDict,OriginalFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.list=ApplicationList
        self.dict=ApplicationDict
        self.original_features_list=OriginalFeaturesList
    
    def fit(self,df):
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.application_processed_feature=self.processed_features_list[0]
        return self
    
    def transform(self,df):
        #Generation of 'FeatureApplicationProcessed' feature assigning applications_dictionnary values to all products which are grouped by specific 'breadcrumbs' feature values
        df[self.application_processed_feature]=df[self.breadcrumbs_feature].apply(lambda row: feature_transformation(row,self.list,self.dict))
        
        return df

#Modification of 'FeatureApplicationProcessed' feature
class FeatureApplicationModification(TransformerMixin):
    
    def __init__(self,OriginalFeaturesList,ProcessedFeaturesList,FeaturesApplicationList):
    
        self.original_features_list=OriginalFeaturesList
        self.processed_features_list=ProcessedFeaturesList
        self.features_application_list=FeaturesApplicationList
        
    def fit(self,df):
        
        self.para_feature=self.original_features_list[6]
        self.wedge_feature=self.original_features_list[7]
        self.parawedge_feature=self.original_features_list[8]
        
        self.application_processed_feature=self.processed_features_list[0]
        
        self.flat_windows_feature=self.features_application_list[0]
        self.wedge_windows_feature=self.features_application_list[2]
        
        return self
    
    def transform(self,df):
        #Modification of products which have 'Parallelism · Wedge angle' feature to separate products with 'Parallelism' and 'Wedge angle' features
        #Modification of 'FeatureApllicationProcessed' by reassigning some products which have been previously considered as 'Flat_windows' to 'wedge_windows'
        df[self.para_feature]=df.apply(lambda row: row[self.parawedge_feature] if row[self.parawedge_feature]=='<5″' else row[self.para_feature],axis=1)
        df[self.wedge_feature]=df.apply(lambda row: row[self.parawedge_feature] if row[self.parawedge_feature]=="1°±5′" else row[self.wedge_feature],axis=1)
        df[self.application_processed_feature]=df.apply(lambda row: self.wedge_windows_feature if ((row[self.application_processed_feature]==self.flat_windows_feature) and (isnotNaN(row[self.wedge_feature]))) else row[self.application_processed_feature] ,axis=1)
        
        return df
    
#Generation of 'SubstrateProcessed' feature 
#products with no optical substrate have been mapped as Not_Available
class SubstrateProcessedCreation(TransformerMixin):
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList,BreadcrumbsList,ApplicationList,ApplicationDict):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
        self.breadcrumbs_list=BreadcrumbsList
        self.list=ApplicationList
        self.dict=ApplicationDict
    
    def fit(self,df):
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.description_feature=self.original_features_list[1]
        self.supplier_feature=self.original_features_list[2]
        self.substrate_feature=self.original_features_list[3]
        self.material_feature=self.original_features_list[4]
        self.substrate_material_feature=self.original_features_list[5]
        self.supplier_name=self.suppliers_list[3]
        self.substrate_processed_feature=self.processed_features_list[1]
        
        return self
    
    def transform(self,df):
        #Generation of 'SubstrateProcessed' feature unifying 2 Thorlabs features 'Substrate' and 'Substrate material'
        df[self.substrate_feature]=df.apply(lambda row: '' if (row[self.supplier_feature]==self.supplier_name and isNaN(row[self.substrate_feature]) and isnotNaN(row[self.substrate_material_feature])) else row[self.substrate_feature],axis=1)
        df[self.substrate_material_feature]=df.apply(lambda row: '' if (row[self.supplier_feature]==self.supplier_name and isNaN(row[self.substrate_material_feature]) and isnotNaN(row[self.substrate_feature])) else row[self.substrate_material_feature],axis=1)
        df[self.substrate_feature]=df.apply(lambda row: row[self.substrate_feature]+row[self.substrate_material_feature] if (row[self.supplier_feature]==self.supplier_name and isnotNaN(row[self.substrate_feature]) and isnotNaN(row[self.substrate_material_feature])) else row[self.substrate_feature],axis=1)
        #Generation of 'description_supplier' feature for products which have NaN values after checking manufacturers description
        df[self.description_feature]=df.apply(lambda row: description_supplier_modification(row[self.description_feature],row[self.breadcrumbs_feature]) if (row[self.breadcrumbs_feature] in self.breadcrumbs_list) else row[self.description_feature],axis=1)
        #Generation of 'SubstrateProcessed' feature after substrate_material_dictionnary values mapping using features as 'description_supplier'
        df[self.substrate_processed_feature] = df.apply(lambda row: feature_transformation(row[self.description_feature],self.list,self.dict) if (isNaN(row[self.material_feature]) and isNaN(row[self.substrate_feature])) else '' ,axis=1)
        #Generation of 'SubstrateProcessed' feature adding values for 'Substrate' and 'Material' features
        df[self.substrate_feature].fillna('',inplace=True)
        df[self.material_feature].fillna('',inplace=True)
        df[self.substrate_processed_feature]=df[self.substrate_processed_feature]+df[self.material_feature]+df[self.substrate_feature]
        #Modification of 'SubstrateProcessed' feature,as names for the same substrate can slighly vary in different products and suppliers, we unify the names of the substrates
        df[self.substrate_processed_feature]=df[self.substrate_processed_feature].apply(lambda row: feature_transformation(row,self.list,self.dict))
        
        return df

#Generation of 'CoatingProcessed' feature
class CoatingProcessedCreation(TransformerMixin):
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList,SpecialList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
        self.special_list=SpecialList
    
    def fit(self,df):
        
        self.substrate_processed_feature=self.processed_features_list[1]
        self.coating_processed_feature=self.processed_features_list[2]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.description_feature=self.original_features_list[1]
        self.supplier_feature=self.original_features_list[2]
        self.coating_feature=self.original_features_list[9]
        self.coating_surface_flatness_feature=self.original_features_list[10]
        
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        
        df[self.coating_processed_feature]=df[self.coating_feature]
         
        #Generation of 'CoatingProcessed' feature for Edmund Optics products using features as 'breadcrumbs'
        df[self.coating_processed_feature]=df.apply(lambda row: 'Uncoated' if ((row[self.supplier_feature]==self.supplier_edmund) and ('Coated' not in row[self.breadcrumbs_feature]) and (isNaN(row[self.coating_processed_feature]))) else row[self.coating_processed_feature],axis=1)
        df[self.coating_processed_feature]=df.apply(lambda row: 'Coated' if ((row[self.supplier_feature]==self.supplier_edmund) and ('Coated' in row[self.breadcrumbs_feature]) and (isNaN(row[self.coating_processed_feature]))) else row[self.coating_processed_feature],axis=1)
        
        #Generation of CoatingProcessed' feature for OptoSigma products using features as'description_supplier'
        df[self.coating_processed_feature]=df.apply(lambda row: 'Uncoated' if ((row[self.supplier_feature]==self.supplier_optosigma) and ('Coated' not in row[self.description_feature]) and (isNaN(row[self.coating_processed_feature]))) else row[self.coating_processed_feature],axis=1)
        df[self.coating_processed_feature]=df.apply(lambda row: 'Coated' if ((row[self.supplier_feature]==self.supplier_optosigma) and ('Coated' in row[self.description_feature]) and (isNaN(row[self.coating_processed_feature]))) else row[self.coating_processed_feature],axis=1)
        
        #Generation of 'CoatingProcessed' feature for EKSMA Optics products using features as 'Coated Surface Flatness' 
        df[self.coating_processed_feature]=df.apply(lambda row: 'Coated' if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.coating_surface_flatness_feature]))) else row[self.coating_processed_feature],axis=1)
        df[self.coating_processed_feature]=df.apply(lambda row: 'Uncoated' if ((row[self.supplier_feature]==self.supplier_eksma) and (isNaN(row[self.coating_processed_feature]))) else row[self.coating_processed_feature],axis=1)
        
        #Generation of 'CoatingProcessed' feature for Thorlabs products using features as 'description_supplier' 
        #There are 2 exceptions: 
        #Not_Available values for Substrate feature
        #Products where value is only indicated in supplier documentation
        df[self.coating_processed_feature]=df.apply(lambda row: 'Uncoated' if ((row[self.supplier_feature]==self.supplier_thorlabs) and (('Uncoated' in row[self.description_feature]) or ('Uncoated' in row[self.breadcrumbs_feature]))) else row[self.coating_processed_feature] ,axis=1)
        df[self.coating_processed_feature]=df.apply(lambda row: 'Not_Available' if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.substrate_processed_feature]=='Not_Available')) else row[self.coating_processed_feature] ,axis=1)
        df[self.coating_processed_feature]=df.apply(lambda row: 'Coated' if ((row[self.supplier_feature]==self.supplier_thorlabs) and (('Coating' in row[self.description_feature]) or ('Coated' in row[self.description_feature]) or ('ARC' in row[self.description_feature]))) else row[self.coating_processed_feature],axis=1)
        df[self.coating_processed_feature]=df.apply(lambda row: 'Uncoated' if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.description_feature] in self.special_list)) else row[self.coating_processed_feature],axis=1)
        
        return df

#Generation of 'CoatingWavelengthProcessed (nm)' feature
class CoatingWavelengthProcessedCreation(TransformerMixin):
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.coating_processed_feature=self.processed_features_list[2]
        self.coating_wavelength_processed_feature=self.processed_features_list[3]
        
        self.description_feature=self.original_features_list[1]
        self.supplier_feature=self.original_features_list[2]
        self.coating_feature=self.original_features_list[9]
        self.wavelengthrangenm_feature=self.original_features_list[11]
        self.wavelengthrange_feature=self.original_features_list[12]
        self.wavelength_feature=self.original_features_list[13]
        self.arcoating_feature=self.original_features_list[14]
        self.arcoatingrange_feature=self.original_features_list[15]
        self.arcoatingwavelengthrange_feature=self.original_features_list[16]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Modification of 'CoatingProcessed' for some specific products to be able to process them futherly with the remaining products
        df[self.coating_processed_feature]=df.apply(lambda row: (row[self.coating_processed_feature]+ ' (400-700nm)') if row[self.coating_processed_feature]=='Opal' else row[self.coating_processed_feature],axis=1)
        df[self.coating_processed_feature]=df.apply(lambda row: (row[self.coating_processed_feature]+ ' (250-700nm)') if row[self.coating_processed_feature]=='UV-VIS' else row[self.coating_processed_feature],axis=1)
        #Generation of 'CoatingWavelengthProcessed (nm)' feature for Edmund Optics products using features as 'CoatingProcessed' and 'Wavelength Range(nm)
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: find_string_between(row[self.coating_processed_feature],"(",")") if ((row[self.supplier_feature]==self.supplier_edmund) and (row[self.coating_processed_feature]!='Uncoated')) else np.nan,axis=1)
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: find_string_between(row[self.coating_wavelength_processed_feature],"@ "," S2") if ((row[self.supplier_feature]==self.supplier_edmund) and (row[self.coating_processed_feature]!='Uncoated')) else row[self.coating_wavelength_processed_feature],axis=1)
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: row[self.wavelengthrangenm_feature] if ((row[self.supplier_feature]==self.supplier_edmund) and (row[self.coating_processed_feature]=='Coated')) else row[self.coating_wavelength_processed_feature],axis=1) 
        #Generation of 'CoatingWavelengthProcessed (nm)' feature for OptoSigma products using features as 'description_supplier' ,'Wavelength range' and 'Coating'
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: row[self.wavelengthrange_feature] if ((row[self.supplier_feature]==self.supplier_optosigma) and (row[self.coating_processed_feature]!='Uncoated') and (isnotNaN(row[self.wavelengthrange_feature]))) else row[self.coating_wavelength_processed_feature],axis=1)
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: find_string_after(row[self.description_feature],'Coated ') if ((row[self.supplier_feature]==self.supplier_optosigma) and (row[self.coating_processed_feature]=='Antireflection Coating')) else row[self.coating_wavelength_processed_feature],axis=1)  
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: find_string_after(row[self.description_feature],'50x50mm ') if ((row[self.supplier_feature]==self.supplier_optosigma) and (row[self.coating_feature]=='Both surfaces: Antireflection coating')) else row[self.coating_wavelength_processed_feature],axis=1)
        #Generation of 'CoatingWavelengthProcessed (nm)' feature for EKSMA products using features as 'CoatingProcessed' and 'Wavelength'
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: row[self.wavelength_feature] if ((row[self.supplier_feature]==self.supplier_eksma) and (row[self.coating_processed_feature]!='Uncoated') and (isnotNaN(row[self.wavelength_feature]))) else row[self.coating_wavelength_processed_feature],axis=1)
        #Generation of 'CoatingWavelengthProcessed (nm)' feature for Thorlabs products using features as 'AR Coating', 'AR Coating Range', 'Wavelength Range of AR Coating', 'CoatingProcessed'
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: row[self.arcoating_feature] if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_Available') and (isnotNaN(row[self.arcoating_feature]))) else row[self.coating_wavelength_processed_feature],axis=1)
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: row[self.arcoatingrange_feature] if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_Available') and (isnotNaN(row[self.arcoatingrange_feature]))) else row[self.coating_wavelength_processed_feature],axis=1)
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: row[self.arcoatingwavelengthrange_feature] if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_Available') and (isnotNaN(row[self.arcoatingwavelengthrange_feature]))) else row[self.coating_wavelength_processed_feature],axis=1)
        #Generation of 'CoatingWavelengthProcessed (nm)' feature for Thorlabs using features as 'description_supplier', 'CoatingProcessed'
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: find_string_between(row[self.description_feature],'ARC: ',',') if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_Available') and ('UVFS' in row[self.description_feature]) and (isNaN(row[self.coating_wavelength_processed_feature]))) else row[self.coating_wavelength_processed_feature],axis=1)
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: find_string_after(row[self.description_feature],'Coating: ') if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_Available') and ('Wedged'in row[self.description_feature]) and (isNaN(row[self.coating_wavelength_processed_feature]))) else row[self.coating_wavelength_processed_feature],axis=1)
        #Cleaning of all 'CoatingWavelengthProcessed (nm)' feature values
        df[self.coating_wavelength_processed_feature]=df.apply(lambda row: cleaning_coating_wavelength(row[self.coating_wavelength_processed_feature]) if (isnotNaN(row[self.coating_wavelength_processed_feature])) else row[self.coating_wavelength_processed_feature],axis=1)
        
        return df

#Generation of 'UncoatedWavelengthProcessed (nm)' feature
class UncoatedWavelengthProcessedCreation(TransformerMixin):
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList,SubstrateList,WavelengthDict):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
        self.list=SubstrateList
        self.dict=WavelengthDict
    
    def fit(self,df):
        
        self.substrate_processed_feature=self.processed_features_list[1]
        self.coating_processed_feature=self.processed_features_list[2]
        self.uncoated_wavelength_processed_feature=self.processed_features_list[4]
        
        self.supplier_feature=self.original_features_list[2]
        self.wavelengthrangenm_feature=self.original_features_list[11]
        self.wavelength_feature=self.original_features_list[13]
        
        self.supplier_edmund=self.suppliers_list[0]
        
        return self
    
    def transform(self,df):
        #Preprocessing 'Wavelength Range (nm)' feature for Edmund Optics products using features as 'Wavelength' 
        df[self.wavelengthrangenm_feature]=df.apply(lambda row: wavelength_assignment(row[self.wavelength_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.wavelength_feature]))) else row[self.wavelengthrangenm_feature],axis=1)
        #Generation of 'UncoatedWavelengthProcessed (nm)' feature for some Edmund Optics products using features as 'Wavelength Range (nm)' and 'CoatingProcessed'
        df[self.uncoated_wavelength_processed_feature]=df.apply(lambda row: row[self.wavelengthrangenm_feature] if ((row[self.supplier_feature]==self.supplier_edmund) and (row[self.coating_processed_feature]=='Uncoated') and (isnotNaN(row[self.wavelengthrangenm_feature]))) else np.nan,axis=1)
        #Generation of 'UncoatedWavelengthProcessed (nm)' feature using wavelength_dictionnary
        df[self.uncoated_wavelength_processed_feature]=df.apply(lambda row: feature_transformation(row[self.substrate_processed_feature],self.list,self.dict) if ((row[self.coating_processed_feature]=='Uncoated') and (isNaN(row[self.wavelengthrangenm_feature]))) else row[self.uncoated_wavelength_processed_feature],axis=1)
        #Cleaning of all 'UncoatedWavelengthProcessed (nm)' feature values
        df[self.uncoated_wavelength_processed_feature]=df.apply(lambda row: cleaning_coating_wavelength(row[self.uncoated_wavelength_processed_feature]) if isnotNaN(row[self.uncoated_wavelength_processed_feature]) else row[self.uncoated_wavelength_processed_feature],axis=1)
        
        return df

#Generation of 'DiameterProcessed (mm)' feature (for circular optical products)
class DiameterProcessedCreation(TransformerMixin):
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.diameter_processed_feature=self.processed_features_list[5]
        
        self.supplier_feature=self.original_features_list[2]
        self.diametermm_feature=self.original_features_list[17]
        self.diameterφD_feature=self.original_features_list[18]
        self.diameter_feature=self.original_features_list[19]
        self.d_feature=self.original_features_list[20]
        self.diameterD_feature=self.original_features_list[21]
        self.windowdiameter_feature=self.original_features_list[22]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'DiameterProcessed (mm)' feature for Edmund Optics products using features as 'Diameter (mm)'
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.diametermm_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.diametermm_feature]))) else np.nan,axis=1)
        #Generation of 'DiameterProcessed (mm)' feature for OptoSigma products using features as 'Diameter φD'
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.diameterφD_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.diameterφD_feature]))) else row[self.diameter_processed_feature],axis=1)
        #Generation of 'DiameterProcessed (mm)' feature for EKSMA products using features as 'Diameter', 'D' and 'Diameter D'
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.diameter_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.diameter_feature]))) else row[self.diameter_processed_feature],axis=1)
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.d_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.d_feature]))) else row[self.diameter_processed_feature],axis=1)
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.diameterD_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.diameterD_feature]))) else row[self.diameter_processed_feature],axis=1)
        #Generation of 'DiameterProcessed (mm)' feature for Thorlabs products using features as 'Diameter' and 'Window Diameter (Unmounted)'
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.diameter_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.diameter_feature]))) else row[self.diameter_processed_feature],axis=1)
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.windowdiameter_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.windowdiameter_feature]))) else row[self.diameter_processed_feature],axis=1)
        
        return df

#Generation of 'SquareRectangleProcessed (mm)' feature (for rectangle and square products)
class SquareRectangleProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList,OptoSigmaDimensionsBreadcrumbsList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
        self.list=OptoSigmaDimensionsBreadcrumbsList
    
    def fit(self,df):
        
        self.coating_processed_feature=self.processed_features_list[2]
        self.diameter_processed_feature=self.processed_features_list[5]
        self.square_processed_feature=self.processed_features_list[6]
        self.rectangle_processed_feature=self.processed_features_list[7]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.description_feature=self.original_features_list[1]
        self.supplier_feature=self.original_features_list[2]
        self.dimensionsmm_feature=self.original_features_list[23]
        self.outerdimensiona_feature=self.original_features_list[24]
        self.outerdimensionaxb_feature=self.original_features_list[25]
        self.length_feature=self.original_features_list[26]
        self.width_feature=self.original_features_list[27]
        self.dimensions_feature=self.original_features_list[28]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'SquareSideProcessed (mm)' feature for Edmund Optics products using features as 'Dimensions (mm)'
        df[self.square_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.dimensionsmm_feature],'square') if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.dimensionsmm_feature]))) else np.nan,axis=1)
        #Generation of 'RectangleSidesProcessed (mm)' feature for Edmund Optics products using features as 'Dimensions (mm)'
        df[self.rectangle_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.dimensionsmm_feature],'rectangle') if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.dimensionsmm_feature]))) else np.nan,axis=1)
        #Generation of 'SquareSideProcessed (mm)' feature for OptoSigma products using features as 'Outer dimension A' and 'Outer dimension A×B' 
        df[self.square_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.outerdimensiona_feature],'square') if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.outerdimensiona_feature]))) else row[self.square_processed_feature],axis=1)
        df[self.square_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.outerdimensionaxb_feature],'square') if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.outerdimensionaxb_feature]))) else row[self.square_processed_feature],axis=1)
        #Generation of 'RectangleSidesProcessed (mm)' feature for OptoSigma products using features as 'Outer dimension A×B'
        df[self.rectangle_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.outerdimensionaxb_feature],'rectangle') if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.outerdimensionaxb_feature]))) else row[self.rectangle_processed_feature],axis=1)
        #Generation of an intermediate feature 'LxW' using features as 'L, Length' and 'W, Width' for EKSMA products
        df['LxW']=df[self.length_feature]+' x '+df[self.width_feature]
        #Generation of 'SquareSideProcessed (mm)' feature for EKSMA products using 'LxW' feature
        df[self.square_processed_feature]=df.apply(lambda row: square_rectangle_processing(row['LxW'],'square') if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row['LxW']))) else row[self.square_processed_feature],axis=1)
        #Generation of 'RectangleSidesProcessed (mm)' feature for EKSMA products using 'LxW' feature
        df[self.rectangle_processed_feature]=df.apply(lambda row: square_rectangle_processing(row['LxW'],'rectangle') if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row['LxW']))) else row[self.rectangle_processed_feature],axis=1)
        #Generation of 'RectangleSidesProcessed (mm)' feature for Thorlabs products using features as 'Dimensions'
        df[self.rectangle_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.dimensions_feature],'rectangle') if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.dimensions_feature]))) else row[self.rectangle_processed_feature],axis=1)
        #Generation of 'SquareSideProcessed (mm)' feature for Thorlabs products using features as 'description_supplier' and 'breadcrumbs'
        df[self.square_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.description_feature],'square') if ((row[self.supplier_feature]==self.supplier_optosigma) and (row[self.breadcrumbs_feature] in self.list)) else row[self.square_processed_feature],axis=1)
        #Generation of 'DiameterProcessed (mm)' feature for some specific Thorlabs products which were not assigned previously
        df[self.diameter_processed_feature]=df.apply(lambda row: diameter_processing(row[self.description_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) & (row[self.coating_processed_feature]!='Not_Available') & (isNaN(row[self.diameter_processed_feature])) & (isNaN(row[self.rectangle_processed_feature])) & (isNaN(row[self.square_processed_feature])) & ('Brewster' not in row[self.description_feature]) & ('x' not in row[self.description_feature])) else row[self.diameter_processed_feature] ,axis=1)
        #Generation of 'RectangleSidesProcessed (mm)' feature for Thorlabs products using features 'description_supplier' and 'CoatingProcessed' for special 
        df[self.rectangle_processed_feature]=df.apply(lambda row: square_rectangle_processing(row[self.description_feature],'rectangle') if ((row[self.supplier_feature]==self.supplier_thorlabs) & (row[self.coating_processed_feature]!='Not_Available') & (isNaN(row[self.diameter_processed_feature])) & (isNaN(row[self.rectangle_processed_feature])) & (isNaN(row[self.square_processed_feature])) & ('Brewster' not in row[self.description_feature]) & ('Ø' not in row[self.description_feature])) else row[self.rectangle_processed_feature] ,axis=1)
        
        return df

#Generation of 'MinorMajorAxisProcessed (mm)' feature (for elliptical products: Elliptical mirrors and brewster windows)
class MinorMajorAxisProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.coating_processed_feature=self.processed_features_list[2]
        self.minoraxis_processed_feature=self.processed_features_list[8]
        self.majoraxis_processed_feature=self.processed_features_list[9]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.supplier_feature=self.original_features_list[2]
        self.minoraxismm_feature=self.original_features_list[29]
        self.majoraxismm_feature=self.original_features_list[30]
        self.minoraxis_feature=self.original_features_list[31]
        self.majoraxis_feature=self.original_features_list[32]
        self.minoraxisd_feature=self.original_features_list[33]
        self.minordiameter_feature=self.original_features_list[34]
        self.compatibleminordiameter_feature=self.original_features_list[92]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of  'MinorAxisProcessed (mm)' feature for Edmund Optics products using features as 'Minor Axis (mm)'
        df[self.minoraxis_processed_feature]=df.apply(lambda row: minor_major_axis_processing(row[self.minoraxismm_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) & (isnotNaN(row[self.minoraxismm_feature]))) else np.nan,axis=1)
        #Generation of 'MajorAxisProcessed (mm)' feature for Edmund Optics products using features as 'Major Axis (mm)'
        df[self.majoraxis_processed_feature]=df.apply(lambda row: row[self.majoraxismm_feature] if ((row[self.supplier_feature]==self.supplier_edmund) & (isnotNaN(row[self.majoraxismm_feature]))) else np.nan,axis=1)
        #Generation of 'MinorAxisProcessed (mm)' feature for EKSMA products using features as 'Minor Axis (mm)' and 'Minor axis D'
        df[self.minoraxis_processed_feature]=df.apply(lambda row: minor_major_axis_processing(row[self.minoraxis_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.minoraxis_feature]))) else row[self.minoraxis_processed_feature],axis=1)
        df[self.minoraxis_processed_feature]=df.apply(lambda row: minor_major_axis_processing(row[self.minoraxisd_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.minoraxisd_feature]))) else row[self.minoraxis_processed_feature],axis=1)
        #Generation of 'MajorAxisProcessed (mm)' feature for EKSMA Optics products using features as 'Major axis'
        df[self.majoraxis_processed_feature]=df.apply(lambda row: minor_major_axis_processing(row[self.majoraxis_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.majoraxis_feature]))) else row[self.majoraxis_processed_feature],axis=1)
        #Generation of 'MinorAxisProcessed (mm)' feature for Thorlabs products using features as 'Minor Diameter' and 'Compatible Brewster Window | Minor Diameter'
        df[self.minoraxis_processed_feature]=df.apply(lambda row: minor_major_axis_processing(row[self.minordiameter_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) & (isnotNaN(row[self.minordiameter_feature]))) else row[self.minoraxis_processed_feature],axis=1)
        df[self.minoraxis_processed_feature]=df.apply(lambda row: minor_major_axis_processing(row[self.compatibleminordiameter_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]=='Not_Available') and ('Brewster' in row[self.breadcrumbs_feature])) else row[self.minoraxis_processed_feature],axis=1)
        
        return df

#Generation of 'ThicknessProcessed (mm)', 'EdgeThickness (mm)' and 'CenterThickness (mm)' features (we generate thickness, edge thickness and center thickness)
class ThicknessProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.coating_processed_feature=self.processed_features_list[2]
        self.thickness_processed_feature=self.processed_features_list[10]
        self.edgethickness_processed_feature=self.processed_features_list[11]
        self.centerthickness_processed_feature=self.processed_features_list[12]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.description_feature=self.original_features_list[1]
        self.supplier_feature=self.original_features_list[2]
        self.thicknessbracketmm_feature=self.original_features_list[35]
        self.thicknesst_feature=self.original_features_list[36]
        self.thicknessmm_feature=self.original_features_list[37]
        self.tcapthickness_feature=self.original_features_list[38]
        self.thicknesstcap_feature=self.original_features_list[39]
        self.thickness_feature=self.original_features_list[40]
        self.windowsthickness_feature=self.original_features_list[41]
        self.edgethickness_feature=self.original_features_list[42]
        self.centerthickness_feature=self.original_features_list[43]
        self.etthickness_feature=self.original_features_list[44]
        self.ctthickness_feature=self.original_features_list[45]
        self.compatiblethickness_feature=self.original_features_list[93]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'ThicknessProcessed (mm)' feature for Edmund Optics products using features as 'Thickness (mm)' 
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.thicknessbracketmm_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.thicknessbracketmm_feature]))) else np.nan,axis=1)
        #Generation of 'ThicknessProcessed (mm)' feature for Edmund Optics products for some missing values using manufacturer documentation
        df[self.thickness_processed_feature]=df.apply(lambda row: '4.7' if ((row[self.supplier_feature]==self.supplier_edmund) and (isNaN(row[self.thicknessbracketmm_feature]))) else row[self.thickness_processed_feature],axis=1)
        #Generation of 'ThicknessProcessed (mm)' feature for OptoSigma products using features as 'Thickness t'
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.thicknesst_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) & (isnotNaN(row[self.thicknesst_feature]))) else row[self.thickness_processed_feature],axis=1)
        #Generation of 'ThicknessProcessed (mm)' feature for EKSMA Optics products using features as 'Thickness, mm', 'T, Thickness' and 'Thickness T'
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.thicknessmm_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.thicknessmm_feature]))) else row[self.thickness_processed_feature],axis=1)
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.tcapthickness_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.tcapthickness_feature]))) else row[self.thickness_processed_feature],axis=1)
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.thicknesstcap_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.thicknesstcap_feature]))) else row[self.thickness_processed_feature],axis=1)
        #Generation of 'ThicknessProcessed (mm)' feature for Thorlabs Optics products using features as 'Thickness' and 'Window Thickness (Unmounted)'
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.thickness_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) & (isnotNaN(row[self.thickness_feature]))) else row[self.thickness_processed_feature],axis=1)
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.windowsthickness_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) & (isnotNaN(row[self.windowsthickness_feature]))) else row[self.thickness_processed_feature],axis=1)
        #Generation of 'ThicknessProcessed (mm)' feature for Thorlabs Optics products using features as 'description_supplier' and 'Compatible Brewster Window | Thickness'
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.description_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isNaN(row[self.thickness_processed_feature])) & (' t ' in row[self.description_feature]) & (row[self.coating_processed_feature]!='Not_Available')) else row[self.thickness_processed_feature],axis=1)
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.description_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isNaN(row[self.thickness_processed_feature])) & (' Thick' in row[self.description_feature]) & (row[self.coating_processed_feature]!='Not_Available')) else row[self.thickness_processed_feature],axis=1)
        df[self.thickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.compatiblethickness_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]=='Not_Available') and ('Brewster' in row[self.breadcrumbs_feature])) else row[self.thickness_processed_feature],axis=1)
        #Generation of 'ThicknessProcessed (mm)' feature for Thorlabs Optics products for missing values using manufacturer documentation 
        df[self.thickness_processed_feature]=df.apply(lambda row: '3.0' if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.description_feature]=='Customer Inspired!&nbsp Ø1/2" Wedged Silicon Window, AR Coating: 2 - 5 µm')) else row[self.thickness_processed_feature],axis=1)
        df[self.thickness_processed_feature]=df.apply(lambda row: '5.0' if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.description_feature]=='Customer Inspired!&nbsp Ø1" Wedged Silicon Window, AR Coating: 2 - 5 µm')) else row[self.thickness_processed_feature],axis=1)
        #Generation of 'EdgeThicknessProcessed (mm)' feature for OptoSigma products using features as 'Edge Thickness te'
        df[self.edgethickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.edgethickness_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isNaN(row[self.thickness_processed_feature])) and (isnotNaN(row[self.edgethickness_feature]))) else np.nan,axis=1)
        #Generation of 'CenterThicknessProcessed (mm)' feature for OptoSigma products using features as 'Center Thickness tc'
        df[self.centerthickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.centerthickness_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isNaN(row[self.thickness_processed_feature])) and (isnotNaN(row[self.centerthickness_feature]))) else np.nan,axis=1)
        #Generation of 'EdgeThicknessProcessed (mm)' feature for EKSMA Optics products using features as 'ET'
        df[self.edgethickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.etthickness_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isNaN(row[self.thickness_processed_feature])) and (isnotNaN(row[self.etthickness_feature]))) else row[self.edgethickness_processed_feature],axis=1)
        #Generation of 'CenterThicknessProcessed (mm)' feature for EKSMA Optics products using features as 'CT'
        df[self.centerthickness_processed_feature]=df.apply(lambda row: thickness_processing(row[self.ctthickness_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isNaN(row[self.thickness_processed_feature])) and (isnotNaN(row[self.ctthickness_feature]))) else row[self.centerthickness_processed_feature],axis=1)
        
        return df

#Generation of 'CurvatureRadiusProcessed (mm)' feature 
class CurvatureRadiusProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.coating_processed_feature=self.processed_features_list[2]
        self.curvatureradius_processed_feature=self.processed_features_list[13]
        
        self.supplier_feature=self.original_features_list[2]
        self.radiuscurvature_feature=self.original_features_list[46]
        self.roc_feature=self.original_features_list[47]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'CurvatureRadiusProcessed (mm)' feature for OptoSigma products using features as 'Radius of curvature r'  
        df[self.curvatureradius_processed_feature]=df.apply(lambda row: curvature_radius_processing(row[self.radiuscurvature_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and isnotNaN(row[self.radiuscurvature_feature])) else np.nan,axis=1)
        #Generation of 'CurvatureRadiusProcessed (mm)' feature for EKSMA Optics products using features as 'ROC'
        df[self.curvatureradius_processed_feature]=df.apply(lambda row: curvature_radius_processing(row[self.roc_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and isnotNaN(row[self.roc_feature])) else row[self.curvatureradius_processed_feature],axis=1)
        
        return df

#Generation of 'WedgeAngleProcessed (°)' feature
class WedgeAngleProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.wedgeangle_processed_feature=self.processed_features_list[14]
        
        self.supplier_feature=self.original_features_list[2]
        self.wedgeangle_feature=self.original_features_list[7]
        self.wedgeanglecap_feature=self.original_features_list[48]
        self.wedgeanglebacksurface_feature=self.original_features_list[90]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation 'WedgeAngleProcessed (°)' feature for Edmund Optics products using features as 'Wedge Angle'
        df[self.wedgeangle_processed_feature]=df.apply(lambda row: wedge_angle_processing(row[self.wedgeanglecap_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.wedgeanglecap_feature]))) else np.nan,axis=1)
        #Generation 'WedgeAngleProcessed (°)' feature for OptoSigma products using features as 'Wedge angle'
        df[self.wedgeangle_processed_feature]=df.apply(lambda row: wedge_angle_processing(row[self.wedgeangle_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.wedgeangle_feature]))) else row[self.wedgeangle_processed_feature],axis=1)
        #Generation of 'WedgeAngleProcessed (°)' feature for Thorlabs products using features as 'Wedge Angle'
        df[self.wedgeangle_processed_feature]=df.apply(lambda row: wedge_angle_processing(row[self.wedgeanglecap_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.wedgeanglecap_feature]))) else row[self.wedgeangle_processed_feature],axis=1)
        #Generation of 'WedgeAngleProcessed (°)' feature for Thorlabs products using features as 'Wedge Angle of Back Surface'
        df[self.wedgeangle_processed_feature]=df.apply(lambda row: wedge_angle_processing(row[self.wedgeanglebacksurface_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.wedgeanglebacksurface_feature]))) else row[self.wedgeangle_processed_feature],axis=1)
        
        return df

#Generation of 'DiffusedAngleProcessed (°)' feature
class DiffusedAngleProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.diffusedangle_processed_feature=self.processed_features_list[15]
        
        self.supplier_feature=self.original_features_list[2]
        self.diffusedangle_feature=self.original_features_list[49]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'DiffusedAngleProcessed (°)' feature for Edmund Optics products using features as 'Diffusing Angle (°)'
        df[self.diffusedangle_processed_feature]=df.apply(lambda row: diffused_angle_processing(row[self.diffusedangle_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.diffusedangle_feature]))) else np.nan,axis=1)
        
        return df

#Generation of 'ParallelismProcessed' feature
class ParallelismProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.application_processed_feature=self.processed_features_list[0]
        self.parallelism_processed_feature=self.processed_features_list[16]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.supplier_feature=self.original_features_list[2]
        self.parallelismarcmin_feature=self.original_features_list[50]
        self.parallelismarcsec_feature=self.original_features_list[51]
        self.parallelism_feature=self.original_features_list[52]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'ParallelismProcessed' feature for Edmund Optics products using features as 'Parallelism (arcmin)' and 'Parallelism (arcsec)'
        df[self.parallelism_processed_feature]=df.apply(lambda row: parallelism_processing(row[self.parallelismarcmin_feature],'arcmin') if ((row[self.supplier_feature]==self.supplier_edmund) & (isnotNaN(row[self.parallelismarcmin_feature]))) else np.nan,axis=1)
        df[self.parallelism_processed_feature]=df.apply(lambda row: parallelism_processing(row[self.parallelismarcsec_feature],'arcsec') if ((row[self.supplier_feature]==self.supplier_edmund) & (isnotNaN(row[self.parallelismarcsec_feature]))) else row[self.parallelism_processed_feature],axis=1)
        #Generation of 'ParallelismProcessed' feature for OptoSigma products using features as 'Parallelism' 
        df[self.parallelism_processed_feature]=df.apply(lambda row: parallelism_processing(row[self.parallelism_feature],'none') if ((row[self.supplier_feature]==self.supplier_optosigma) & (isnotNaN(row[self.parallelism_feature]))) else row[self.parallelism_processed_feature],axis=1)
        #Generation of 'ParallelismProcessed' feature for EKSMA Optics products using features as 'Parallelism'
        df[self.parallelism_processed_feature]=df.apply(lambda row: parallelism_processing(row[self.parallelism_feature],'none') if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.parallelism_feature]))) else row[self.parallelism_processed_feature],axis=1)
        #Generation of 'ParallelismProcessed' feature for Thorlabs products using features as 'Parallelism'
        df[self.parallelism_processed_feature]=df.apply(lambda row: parallelism_processing(row[self.parallelism_feature],'none') if ((row[self.supplier_feature]==self.supplier_thorlabs) & (isnotNaN(row[self.parallelism_feature]))) else row[self.parallelism_processed_feature],axis=1)
        #Generation of 'ParallelismProcessed' feature for some missing products of OptosSigma from manufacturer documentation 
        df[self.parallelism_processed_feature]=df.apply(lambda row: '3.0' if ((row[self.supplier_feature]==self.supplier_optosigma) and (row[self.application_processed_feature]!='Wedged_windows') and (row[self.application_processed_feature]!='Mirrors') and (isNaN(row[self.parallelism_processed_feature])) and (row[self.breadcrumbs_feature]!='Home>Optics>Windows Substrates>Flat Substrates>Float Glass')) else row[self.parallelism_processed_feature],axis=1)
        
        return df

#Generation of 'SurfaceFlatnessProcessed' feature
class SurfaceFlatnessProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList,SurfaceFlatLambda2List,SurfaceFlatLambda4List,SurfaceFlatLambda8List,SurfaceFlatLambda10List):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
        self.surfaceflatlambda2_list=SurfaceFlatLambda2List
        self.surfaceflatlambda4_list=SurfaceFlatLambda4List
        self.surfaceflatlambda8_list=SurfaceFlatLambda8List
        self.surfaceflatlambda10_list=SurfaceFlatLambda10List
        
    def fit(self,df):
        
        self.surfaceflatness_processed_feature=self.processed_features_list[17]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.supplier_feature=self.original_features_list[2]
        self.surfaceflatnesscap_feature=self.original_features_list[53]
        self.surfaceflatnesspv_feature=self.original_features_list[54]
        self.rearsurfaceflatness_feature=self.original_features_list[55]
        self.surfaceflatnesspvr_feature=self.original_features_list[56]
        self.surfaceflatnessofsubstrate_feature=self.original_features_list[57]
        self.surfaceflatness_feature=self.original_features_list[58]
        self.flatness_feature=self.original_features_list[59]
        self.s1s2surfaceflatness_feature=self.original_features_list[60]
        self.surfaceflatnesss1s2_feature=self.original_features_list[61]
        self.firstsurfaceflatness_feature=self.original_features_list[62]
        self.surfaceflatness633_feature=self.original_features_list[63]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'SurfaceFlatnessProcessed' feature for Edmund Optics products using features as 'Surface Flatness' 
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatnesscap_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.surfaceflatnesscap_feature]))) else np.nan,axis=1)
        #Generation of 'SurfaceFlatnessProcessed' feature for OptoSigma products using features as 'Surface Flatness','Surface Flatness PV', 'Rear surfacesurface flatness', 'Surface Flatness PVr' and 'Surface flatness of substrate'
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatnesscap_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.surfaceflatnesscap_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatnesspv_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.surfaceflatnesspv_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.rearsurfaceflatness_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.rearsurfaceflatness_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatnesspvr_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.surfaceflatnesspvr_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatnessofsubstrate_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.surfaceflatnessofsubstrate_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        #Generation of 'SurfaceFlatnessProcessed' feature for EKSMA Optics products using features as 'Surface flatness','Flatness', 'S1/S2 Surface Flatness', 'Surface flatness S1, S2' and '1st surface flatness:'
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatness_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.surfaceflatness_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.flatness_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.flatness_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.s1s2surfaceflatness_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.s1s2surfaceflatness_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatnesss1s2_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.surfaceflatnesss1s2_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.firstsurfaceflatness_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.firstsurfaceflatness_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        #Generation of 'SurfaceFlatnessProcessed' feature for Thorlabs products using features as 'Surface Flatness' and 'Surface Flatness (@633 nm)'
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatnesscap_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.surfaceflatnesscap_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: flatness_processing(row[self.surfaceflatness633_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.surfaceflatness633_feature]))) else row[self.surfaceflatness_processed_feature],axis=1)
        #Generation of missing values from manufacturers documentation using features as 'breadcrumbs'
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: 'λ/2' if (row[self.breadcrumbs_feature] in self.surfaceflatlambda2_list) else row[self.surfaceflatness_processed_feature],axis=1)        
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: 'λ/4' if (row[self.breadcrumbs_feature] in self.surfaceflatlambda4_list) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: 'λ/8' if (row[self.breadcrumbs_feature] in self.surfaceflatlambda8_list) else row[self.surfaceflatness_processed_feature],axis=1)
        df[self.surfaceflatness_processed_feature]=df.apply(lambda row: 'λ/10' if (row[self.breadcrumbs_feature] in self.surfaceflatlambda10_list) else row[self.surfaceflatness_processed_feature],axis=1)
        
        return df

#Generation of 'SurfaceQualityProcessed (Scratch-Dig)' feature
class SurfaceQualityProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList,SurfaceQuality105List,SurfaceQuality2010List,SurfaceQuality4020List):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
        self.surfacequal105_list=SurfaceQuality105List
        self.surfacequal2010_list=SurfaceQuality2010List
        self.surfacequal4020_list=SurfaceQuality4020List
    
    def fit(self,df):
        
        self.surfacequality_processed_feature=self.processed_features_list[18]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.supplier_feature=self.original_features_list[2]
        self.surfacequalitycap_feature=self.original_features_list[64]
        self.surfacequalityscratchdigcap_feature=self.original_features_list[65]
        self.surfacequalityscratchdig_feature=self.original_features_list[66]
        self.surfacequality_feature=self.original_features_list[67]
        self.surfacequalitys1s2_feature=self.original_features_list[68]
        self.s1s2surfacequality_feature=self.original_features_list[69]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'SurfaceQualityProcessed (Scratch-Dig)' feature for Edmund Optics products using features as 'Surface Quality'
        df[self.surfacequality_processed_feature]=df.apply(lambda row: row[self.surfacequalitycap_feature] if ((row[self.supplier_feature]==self.supplier_edmund) & (isnotNaN(row[self.surfacequalitycap_feature]))) else np.nan,axis=1)
        #Generation of 'SurfaceQualityProcessed (Scratch-Dig)' feature for OptoSigma products using features as 'Surface Quality(Scratch-Dig)' and 'Surface quality (scratch-dig)'
        df[self.surfacequality_processed_feature]=df.apply(lambda row: row[self.surfacequalityscratchdigcap_feature] if ((row[self.supplier_feature]==self.supplier_optosigma) & (isnotNaN(row[self.surfacequalityscratchdigcap_feature]))) else row[self.surfacequality_processed_feature],axis=1)
        df[self.surfacequality_processed_feature]=df.apply(lambda row: row[self.surfacequalityscratchdig_feature] if ((row[self.supplier_feature]==self.supplier_optosigma) & (isnotNaN(row[self.surfacequalityscratchdig_feature]))) else row[self.surfacequality_processed_feature],axis=1)
        #Generation 'SurfaceQualityProcessed (Scratch-Dig)' feature for EKSMA Optics products using features as 'Surface quality', 'Surface quality S1, S2' and 'S1/S2 Surface Quality'
        df[self.surfacequality_processed_feature]=df.apply(lambda row: quality_processing(row[self.surfacequality_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.surfacequality_feature]))) else row[self.surfacequality_processed_feature],axis=1)
        df[self.surfacequality_processed_feature]=df.apply(lambda row: quality_processing(row[self.surfacequalitys1s2_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.surfacequalitys1s2_feature]))) else row[self.surfacequality_processed_feature],axis=1)
        df[self.surfacequality_processed_feature]=df.apply(lambda row: quality_processing(row[self.s1s2surfacequality_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) & (isnotNaN(row[self.s1s2surfacequality_feature]))) else row[self.surfacequality_processed_feature],axis=1)
        #Generation of 'SurfaceQualityProcessed (Scratch-Dig)' feature for Thorlabs products using features as 'Surface Quality'
        df[self.surfacequality_processed_feature]=df.apply(lambda row: quality_processing(row[self.surfacequalitycap_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) & (isnotNaN(row[self.surfacequalitycap_feature]))) else row[self.surfacequality_processed_feature],axis=1)
        #Generation of 'SurfaceQualityProcessed (Scratch-Dig)' feature for missing values with manufacturers documentation using features as 'breadcrumbs'
        df[self.surfacequality_processed_feature]=df.apply(lambda row: '10-5' if (row[self.breadcrumbs_feature] in self.surfacequal105_list) else row[self.surfacequality_processed_feature],axis=1)
        df[self.surfacequality_processed_feature]=df.apply(lambda row: '20-10' if (row[self.breadcrumbs_feature] in self.surfacequal2010_list) else row[self.surfacequality_processed_feature],axis=1)
        df[self.surfacequality_processed_feature]=df.apply(lambda row: '40-20' if (row[self.breadcrumbs_feature] in self.surfacequal4020_list) else row[self.surfacequality_processed_feature],axis=1)
       
        return df

#Generation of 'WavefrontDistortionProcessed' feature
class WavefrontDistortionProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.surfaceflatness_processed_feature=self.processed_features_list[17]
        self.wavefronterror_processed_feature=self.processed_features_list[19]
        
        self.supplier_feature=self.original_features_list[2]
        self.transmittedwavefrontpv_feature=self.original_features_list[70]
        self.transmittedwavefronttol_feature=self.original_features_list[71]
        self.wavefrontdistortion_feature=self.original_features_list[72]
        self.transmittedwavefronterr633_feature=self.original_features_list[73]
        self.transmittedwavefronterr_633_feature=self.original_features_list[74]
        self.transmittedwavefronterr_feature=self.original_features_list[75]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'WavefrontErrorProcessed' feature for Edmund Optics products using features as 'Transmitted Wavefront, P-V', 'Transmitted Wavefront Tolerance' 
        df[self.wavefronterror_processed_feature]=df.apply(lambda row: wavefront_error_processing(row[self.transmittedwavefrontpv_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.transmittedwavefrontpv_feature]))) else np.nan,axis=1)
        df[self.wavefronterror_processed_feature]=df.apply(lambda row: wavefront_error_processing(row[self.transmittedwavefronttol_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.transmittedwavefronttol_feature]))) else row[self.wavefronterror_processed_feature],axis=1)
        #Generation of 'WavefrontErrorProcessed' feature values for Edmund Optics products for products in order to have exclusively 'SurfaceFlatnessProcessed' or 'WavefrontErrorProcessed'
        df[self.wavefronterror_processed_feature]=df.apply(lambda row: np.nan if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.surfaceflatness_processed_feature])) and (isnotNaN(row[self.wavefronterror_processed_feature]))) else row[self.wavefronterror_processed_feature],axis=1)
        #Generation of 'WavefrontErrorProcessed' feature for EKSMA Optics products using features as 'Wavefront distortion'
        df[self.wavefronterror_processed_feature]=df.apply(lambda row: wavefront_error_processing(row[self.wavefrontdistortion_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.wavefrontdistortion_feature]))) else row[self.wavefronterror_processed_feature],axis=1)
        #Generation of 'WavefrontErrorProcessed' feature for Thorlabs products using features as 'Transmitted Wavefront Error (@633 nm)', 'Transmitted Wavefront Error (@ 633 nm)' and 'Transmitted Wavefront Error'
        df[self.wavefronterror_processed_feature]=df.apply(lambda row: wavefront_error_processing(row[self.transmittedwavefronterr633_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.transmittedwavefronterr633_feature]))) else row[self.wavefronterror_processed_feature],axis=1)
        df[self.wavefronterror_processed_feature]=df.apply(lambda row: wavefront_error_processing(row[self.transmittedwavefronterr_633_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.transmittedwavefronterr_633_feature]))) else row[self.wavefronterror_processed_feature],axis=1)
        df[self.wavefronterror_processed_feature]=df.apply(lambda row: wavefront_error_processing(row[self.transmittedwavefronterr_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.transmittedwavefronterr_feature]!='<λ/4 Over Central Ø5 mm ≤λ/2 Over Full Clear Aperture') and (row[self.transmittedwavefronterr_feature]!='λ/4') and (row[self.transmittedwavefronterr_feature]!='-') and (isnotNaN(row[self.transmittedwavefronterr_feature]))) else row[self.wavefronterror_processed_feature],axis=1)
        
        return df

#Generation of 'ReflectanceProcessed' feature
class ReflectanceProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList,ReflectanceList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
        self.reflectance_list=ReflectanceList
    
    def fit(self,df):
        
        self.coating_processed_feature=self.processed_features_list[2]
        self.reflectance_processed_feature=self.processed_features_list[20]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.supplier_feature=self.original_features_list[2]
        self.coatingspec_feature=self.original_features_list[76]
        self.reflectionpercent_feature=self.original_features_list[77]
        self.transmittance106um_feature=self.original_features_list[78]
        self.reflectanceoverar_feature=self.original_features_list[79]
        self.arcoatingperf_feature=self.original_features_list[80]
        self.arcoatingreflec_feature=self.original_features_list[81]
        self.reflectanceovercapar_feature=self.original_features_list[82]
        self.title_feature=self.original_features_list[83]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'ReflectanceProcessed' feature for Edmund Optics products using features as 'Coating Specification' and 'Reflection (%)'
        df[self.reflectance_processed_feature]=df.apply(lambda row: reflectance_processing(row[self.coatingspec_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (row[self.coating_processed_feature]!='Uncoated') and (isnotNaN(row[self.coatingspec_feature]))) else np.nan,axis=1)
        df[self.reflectance_processed_feature]=df.apply(lambda row: reflectance_processing(row[self.reflectionpercent_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (row[self.coating_processed_feature]!='Uncoated') and (isnotNaN(row[self.reflectionpercent_feature]))) else row[self.reflectance_processed_feature],axis=1)
        #Generation of 'ReflectanceProcessed' feature for OptoSigma products using features as 'Transmittance (λ=10.6μm)'
        df[self.reflectance_processed_feature]=df.apply(lambda row: reflectance_processing(row[self.transmittance106um_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (row[self.coating_processed_feature]!='Uncoated') and (isnotNaN(row[self.transmittance106um_feature]))) else row[self.reflectance_processed_feature],axis=1)
        #Generation of 'ReflectanceProcessed' feature for some missing values using manufacturers documentation for some specific values of 'breadcrumbs' and 'title' features
        df[self.reflectance_processed_feature]=df.apply(lambda row: '0.6' if (self.reflectance_list[0] in row[self.breadcrumbs_feature]) else row[self.reflectance_processed_feature],axis=1)
        df[self.reflectance_processed_feature]=df.apply(lambda row: '1.0' if (self.reflectance_list[1] in row[self.breadcrumbs_feature]) else row[self.reflectance_processed_feature],axis=1)        
        df[self.reflectance_processed_feature]=df.apply(lambda row: '0.25' if (row[self.title_feature]=='Laser Line Anti-Reflection Coated Precision Windows') else row[self.reflectance_processed_feature],axis=1)
        #Generation of 'ReflectanceProcessed' feature for Thorlabs products using features as 'Reflectance over AR Coating Range', 'AR Coating Performance', 'AR Coating Reflectance' and 'Reflectance Over AR Coating Range'
        df[self.reflectance_processed_feature]=df.apply(lambda row: reflectance_processing(row[self.reflectanceoverar_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_available') & (isnotNaN(row[self.reflectanceoverar_feature]))) else row[self.reflectance_processed_feature],axis=1)
        df[self.reflectance_processed_feature]=df.apply(lambda row: reflectance_processing(row[self.arcoatingperf_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_available') & (isnotNaN(row[self.arcoatingperf_feature]))) else row[self.reflectance_processed_feature],axis=1)
        df[self.reflectance_processed_feature]=df.apply(lambda row: reflectance_processing(row[self.arcoatingreflec_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_available') & (isnotNaN(row[self.arcoatingreflec_feature]))) else row[self.reflectance_processed_feature],axis=1)
        df[self.reflectance_processed_feature]=df.apply(lambda row: reflectance_processing(row[self.reflectanceovercapar_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Not_available') & (isnotNaN(row[self.reflectanceovercapar_feature]))) else row[self.reflectance_processed_feature],axis=1)
        #Generation of 'ReflectanceProcessed' feature for some missing values using manufacturers documentation
        df[self.reflectance_processed_feature]=df.apply(lambda row: '1.25' if (self.reflectance_list[2] in row[self.breadcrumbs_feature]) else row[self.reflectance_processed_feature],axis=1)        
        df[self.reflectance_processed_feature]=df.apply(lambda row: '0.5' if (self.reflectance_list[3] in row[self.breadcrumbs_feature]) else row[self.reflectance_processed_feature],axis=1)
        df[self.reflectance_processed_feature]=df.apply(lambda row: '0.5' if (self.reflectance_list[4] in row[self.breadcrumbs_feature]) else row[self.reflectance_processed_feature],axis=1)                        
        df[self.reflectance_processed_feature]=df.apply(lambda row: '0.5' if (self.reflectance_list[5] in row[self.breadcrumbs_feature]) else row[self.reflectance_processed_feature],axis=1)                                                                    
        
        return df

#Generation of 'DamageThresholdProcessed' feature
class DamageThresholdProcessedCreation(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,SuppliersList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.suppliers_list=SuppliersList
    
    def fit(self,df):
        
        self.coatingwavelengthnm_processed_feature=self.processed_features_list[3]
        self.damagethreshold_processed_feature=self.processed_features_list[21]
        
        self.supplier_feature=self.original_features_list[2]
        self.damagethresholdpulsed_feature=self.original_features_list[84]
        self.laserdamagethreshold_feature=self.original_features_list[85]
        self.damagethresholdbk7uvfs_feature=self.original_features_list[86]
        self.damagethreshold_feature=self.original_features_list[87]
        self.damagethresholdpulse_feature=self.original_features_list[88]
        self.opticdamagethresholdpulse_feature=self.original_features_list[89]
        
        self.supplier_edmund=self.suppliers_list[0]
        self.supplier_optosigma=self.suppliers_list[1]
        self.supplier_eksma=self.suppliers_list[2]
        self.supplier_thorlabs=self.suppliers_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'DamageThresholdProcessed' feature for Edmund Optics products using features as 'Damage Threshold, Pulsed' and 'CoatingWavelengthProcessed (nm)'
        df[ self.damagethreshold_processed_feature]=df.apply(lambda row: damagethreshold_processing(row[self.damagethresholdpulsed_feature],row[self.coatingwavelengthnm_processed_feature]) if ((row[self.supplier_feature]==self.supplier_edmund) and (isnotNaN(row[self.damagethresholdpulsed_feature]))) else np.nan,axis=1)
        #Generation of 'DamageThresholdProcessed' feature for OptoSigma products using features as 'Laser Damage Threshold' and 'CoatingWavelengthProcessed (nm)'
        df[ self.damagethreshold_processed_feature]=df.apply(lambda row: damagethreshold_processing(row[self.laserdamagethreshold_feature],row[self.coatingwavelengthnm_processed_feature]) if ((row[self.supplier_feature]==self.supplier_optosigma) and (isnotNaN(row[self.laserdamagethreshold_feature]))) else row[self.damagethreshold_processed_feature],axis=1)
        #Generation of 'DamageThresholdProcessed' feature for EKSMA Optics products using features as 'Damage Threshold: BK7 UVFS' and 'CoatingWavelengthProcessed (nm)'
        df[ self.damagethreshold_processed_feature]=df.apply(lambda row: damagethreshold_processing(row[self.damagethresholdbk7uvfs_feature],row[self.coatingwavelengthnm_processed_feature]) if ((row[self.supplier_feature]==self.supplier_eksma) and (isnotNaN(row[self.damagethresholdbk7uvfs_feature]))) else row[self.damagethreshold_processed_feature],axis=1)
        #Generation of 'DamageThresholdProcessed' feature for Thorlabs products using features as 'Damage Threshold', 'Damage Threshold | Pulse' and 'Optic Damage Threshold | Pulse'
        df[ self.damagethreshold_processed_feature]=df.apply(lambda row: damagethreshold_processing(row[self.damagethreshold_feature],row[self.coatingwavelengthnm_processed_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.damagethreshold_feature]))) else row[self.damagethreshold_processed_feature],axis=1)
        df[ self.damagethreshold_processed_feature]=df.apply(lambda row: damagethreshold_processing(row[self.damagethresholdpulse_feature],row[self.coatingwavelengthnm_processed_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.damagethresholdpulse_feature]))) else row[self.damagethreshold_processed_feature],axis=1)
        df[ self.damagethreshold_processed_feature]=df.apply(lambda row: damagethreshold_processing(row[self.opticdamagethresholdpulse_feature],row[self.coatingwavelengthnm_processed_feature]) if ((row[self.supplier_feature]==self.supplier_thorlabs) and (isnotNaN(row[self.opticdamagethresholdpulse_feature]))) else row[self.damagethreshold_processed_feature],axis=1)
        
        return df
    
#creation of several classes based on TransformerMixin class (sklearn.base library)
#these classes will allow us to pipeline all dataframe mapping

#these classes have 3 main functions:
# __init__ (initialize features lists)
#fit (define individual features from input lists)
#transform (transform individual features values to generate new features values)

#once classes are instantiated with parameters lists in pipeline function, function fit_transform generates 
# whole pipeline transformation

#Generation of 'FeatureApplicationMapped' and 'CoatingMApped' features
class ApplicationAndCoatingMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.application_processed_feature=self.processed_features_list[0]
        self.coating_processed_feature=self.processed_features_list[2]
        
        self.application_mapped_feature=self.mapped_features_list[0]
        self.coating_mapped_feature=self.mapped_features_list[1]
        
        return self
    
    def transform(self,df):
        #Postprocessing 'CoatingProcessed' feature before its mapping
        df[self.coating_processed_feature]=df.apply(lambda row: 'Coated' if ((row[self.coating_processed_feature]!='Uncoated') and (row[self.coating_processed_feature]!='Coated') and (row[self.coating_processed_feature]!='Not_Available')) else row[self.coating_processed_feature],axis=1)
        #Generation of 'FeatureApplicationMapped' feature using featureapplication_mapping dictonnary 
        df[self.application_mapped_feature]=df[self.application_processed_feature].map(config.featureapplication_mapping)
        #Generation of 'CoatingMapped' feature using coating_mapping dictonnary
        df[self.coating_mapped_feature]=df[self.coating_processed_feature].map(config.coating_mapping)
        
        return df
    
#Generation of 'CoatingWavelengthMapped' and 'UncoatedWavelengthMapped' features    
class WavelengthMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.coatingwavelength_processed_feature=self.processed_features_list[3]
        self.uncoatedwavelength_processed_feature=self.processed_features_list[4]
        
        self.coatingdwavelength_mapped_feature=self.mapped_features_list[2]
        self.uncoatedwavelength_mapped_feature=self.mapped_features_list[3]
        
        return self
    
    def transform(self,df):
        #Generation of 'UncoatedWavelengthMapped' feature using uncoated_wavelength_mapping dictionnary
        #NaN values are replaced by 0
        df[self.uncoatedwavelength_mapped_feature]=df[self.uncoatedwavelength_processed_feature].map(config.uncoated_wavelength_mapping)
        df[self.uncoatedwavelength_mapped_feature]=df[self.uncoatedwavelength_mapped_feature].fillna(0)
        #Generation of 'CoatingWavelengthMapped' feature using coating_wavelength_mapping dictionnary
        #'CoatingWavelengthMapped' NaN values are replaced by 0
        df[self.coatingdwavelength_mapped_feature]=df[self.coatingwavelength_processed_feature].map(config.coating_wavelength_mapping)
        df[self.coatingdwavelength_mapped_feature]=df[self.coatingdwavelength_mapped_feature].fillna(0)
        
        return df
#Generation of 'ShapeMapped' and 'ShapeValueMapped' features
class DimensionsMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.diameter_processed_feature=self.processed_features_list[5]
        self.squareside_processed_feature=self.processed_features_list[6]
        self.rectanglesides_processed_feature=self.processed_features_list[7]
        self.minoraxis_processed_feature=self.processed_features_list[8]
        self.majoraxis_processed_feature=self.processed_features_list[9]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        
        self.shape_mapped_feature=self.mapped_features_list[4]
        self.shapevalue_mapped_feature=self.mapped_features_list[5]
        
        
        return self
    
    def transform(self,df):
        #Generation of 'ShapeMapped' feature for circular optical products
        df[self.shape_mapped_feature]=df.apply(lambda row: 3000 if isnotNaN(row[self.diameter_processed_feature]) else np.nan,axis=1)
        #Generation of 'ShapeMapped' feature for square optical products
        df[self.shape_mapped_feature]=df.apply(lambda row: 8000 if isnotNaN(row[self.squareside_processed_feature]) else row[self.shape_mapped_feature],axis=1)
        #Generation of 'ShapeMapped' feature for rectangle optical products
        df[self.shape_mapped_feature]=df.apply(lambda row: 10000 if isnotNaN(row[self.rectanglesides_processed_feature]) else row[self.shape_mapped_feature],axis=1)
        #'ShapeMapped' NaN values are replaced by 0
        df[self.shape_mapped_feature]=df[self.shape_mapped_feature].fillna(0)
        #Generation of 'ShapeValueMapped' feature for circular optical products
        df[self.shapevalue_mapped_feature]=df.apply(lambda row: float(row[self.diameter_processed_feature]) if isnotNaN(row[self.diameter_processed_feature]) else np.nan,axis=1)
        #Generation of 'ShapeValueMapped' feature for square optical products
        df[self.shapevalue_mapped_feature]=df.apply(lambda row: float(row[self.squareside_processed_feature]) if isnotNaN(row[self.squareside_processed_feature]) else row[self.shapevalue_mapped_feature],axis=1)
        #Generation of 'ShapeValueMapped' feature for rectangle optical products
        df[self.shapevalue_mapped_feature]=df.apply(lambda row: rectangle_value_mapping(row[self.rectanglesides_processed_feature]) if isnotNaN(row[self.rectanglesides_processed_feature]) else row[self.shapevalue_mapped_feature],axis=1)
        #Generation of 'ShapeValueMapped' feature for elliptical optical products (brewster windows)
        df[self.shapevalue_mapped_feature]=df.apply(lambda row: float(row[self.minoraxis_processed_feature]) if ((isnotNaN(row[self.minoraxis_processed_feature])) and ('Elliptical' not in row[self.breadcrumbs_feature])) else row[self.shapevalue_mapped_feature],axis=1)
        #Generation of 'ShapeValueMapped' feature for elliptical optical products (elliptical mirrors)
        df[self.shapevalue_mapped_feature]=df.apply(lambda row: elliptical_value_mapping(row[self.minoraxis_processed_feature],row[self.majoraxis_processed_feature]) if ((isnotNaN(row[self.minoraxis_processed_feature])) and (isnotNaN(row[self.majoraxis_processed_feature])) and ('Elliptical' in row[self.breadcrumbs_feature])) else row[self.shapevalue_mapped_feature],axis=1)
        #'ShapeValueMapped' NaN values are replaced by 0
        df[self.shapevalue_mapped_feature]=df[self.shapevalue_mapped_feature].fillna(0) 
        
        return df

#Generation of 'ThicknessMapped','EdgeThicknessMapped' and 'CenterThicknessMapped' features
class ThicknessMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.thickness_processed_feature=self.processed_features_list[10]
        self.edgethickness_processed_feature=self.processed_features_list[11]
        self.centerthickness_processed_feature=self.processed_features_list[12]
        
        self.centerthickness_feature=self.original_features_list[43]
        
        self.thickness_mapped_feature=self.mapped_features_list[7]
        self.edgethickness_mapped_feature=self.mapped_features_list[8]
        self.centerthickness_mapped_feature=self.mapped_features_list[9]
        
        return self
    
    def transform(self,df):
        #Generation of 'ThicknessMapped'feature using features as 'ThicknessProcessed (mm)'
        #'ThicknessMapped' NaN are replaced by 0
        df[self.thickness_mapped_feature]=df.apply(lambda row: float(row[self.thickness_processed_feature]) if isnotNaN(row[self.thickness_processed_feature]) else np.nan,axis=1)
        df[self.thickness_mapped_feature]=df[self.thickness_mapped_feature].fillna(0)
        #Generation of 'EdgeThicknessMapped'feature using features as 'EdgeThicknessProcessed (mm)'
        #'EdgeThicknessMapped' NaN are replaced by 0
        df[self.edgethickness_mapped_feature]=df.apply(lambda row: float(row[self.edgethickness_processed_feature]) if isnotNaN(row[self.edgethickness_processed_feature]) else np.nan,axis=1)
        df[self.edgethickness_mapped_feature]=df[self.edgethickness_mapped_feature].fillna(0)
        #Generation of 'CenterThicknessMapped' feature using features as 'CenterThicknessProcessed (mm)'
        #'CenterThicknessMapped' NaN are replaced by 0
        df[self.centerthickness_mapped_feature]=df.apply(lambda row: float(row[self.centerthickness_processed_feature]) if ((isnotNaN(row[self.centerthickness_processed_feature])) and (isNaN(row[self.centerthickness_feature]))) else np.nan,axis=1)
        df[self.centerthickness_mapped_feature]=df[self.centerthickness_mapped_feature].fillna(0)
        
        return df

#generation of 'MirrorShapeMapped' and 'CurvatureRadiusMapped' features  
class MirrorsShapeMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.application_processed_feature=self.processed_features_list[0]
        self.minoraxis_processed_feature=self.processed_features_list[8]
        self.curvatureradius_processed_feature=self.processed_features_list[13]
        
        self.ctthickness_feature=self.original_features_list[45]
        
        self.mirrorshape_mapped_feature=self.mapped_features_list[6]
        self.curvatureradius_mapped_feature=self.mapped_features_list[10]
        
        return self
    
    def transform(self,df):
        #Generation of 'MirrorShapeMapped' feature using features as 'CT', 'FeatureApplicationProcessed' and 'MinorAxisProcessed (mm)'
        #'MirrorShapeMapped' NaN values are replaced by 0
        df[self.mirrorshape_mapped_feature]=df.apply(lambda row: 20000 if isnotNaN(row[self.ctthickness_feature]) else np.nan,axis=1)
        df[self.mirrorshape_mapped_feature]=df.apply(lambda row: 10000 if ((row[self.application_processed_feature]=='Mirrors') and (isnotNaN(row[self.minoraxis_processed_feature]))) else row[self.mirrorshape_mapped_feature],axis=1)
        df[self.mirrorshape_mapped_feature]=df.apply(lambda row: 30000 if ((row[self.application_processed_feature]=='Mirrors') and (isNaN(row[self.mirrorshape_mapped_feature]))) else row[self.mirrorshape_mapped_feature],axis=1)
        df[self.mirrorshape_mapped_feature]=df[self.mirrorshape_mapped_feature].fillna(0)
        #Generation of 'CurvatureRadiusMapped' feature using features as 'CurvatureRadiusProcessed'
        #'CurvatureRadiusMapped' NaN values are replaced by 0
        df[self.curvatureradius_mapped_feature]=df.apply(lambda row: float(row[self.curvatureradius_processed_feature])/50. if isnotNaN(row[self.curvatureradius_processed_feature]) else np.nan,axis=1)
        df[self.curvatureradius_mapped_feature]=df[self.curvatureradius_mapped_feature].fillna(0)
        
        return df

#Generation of 'WedgeAngleMapped' and 'ParallelismMapped' features
class WedgeAngleParallelismMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.wedgeangle_processed_feature=self.processed_features_list[14]
        self.parallelism_processed_feature=self.processed_features_list[16]
        
        self.wedgeangle_mapped_feature=self.mapped_features_list[11]
        self.parallelism_mapped_feature=self.mapped_features_list[13]
        
        return self
    
    def transform(self,df):
        #Generation of 'WedgeAngleMapped' feature using features as 'WedgeAngleProcessed'
        #'WedgeAngleMapped' NaN values are replaced by 0
        df[self.wedgeangle_mapped_feature]=df.apply(lambda row: float(row[self.wedgeangle_processed_feature]) if isnotNaN(row[self.wedgeangle_processed_feature]) else np.nan,axis=1)
        df[self.wedgeangle_mapped_feature]=df[self.wedgeangle_mapped_feature].fillna(0)
        #Generation of 'ParallelismMapped' feature using features as 'ParallelismProcessed'
        #'ParallelismMapped' NaN values are replaced by 0
        df[self.parallelism_mapped_feature]=df.apply(lambda row: float(row[self.parallelism_processed_feature]) if isnotNaN(row[self.parallelism_processed_feature]) else np.nan,axis=1)
        df[self.parallelism_mapped_feature]=df[self.parallelism_mapped_feature].fillna(0)
        
        return df

#Generation of 'DiffusedAngleMapped' and 'AberrationMapped' features
class DiffusingangleAberrationMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.diffusedangle_processed_feature=self.processed_features_list[15]
        
        self.aberration_feature=self.original_features_list[91]
        
        self.diffusedangle_mapped_feature=self.mapped_features_list[12]
        self.aberration_mapped_feature=self.mapped_features_list[19]
        
        return self
    
    def transform(self,df):
        #Generation of 'DiffusedAngleMapped' feature using features as 'DiffusedAngleProcessed'
        #'DiffusedAngleMapped' NaN values are replaced by 0
        df[self.diffusedangle_mapped_feature]=df.apply(lambda row: circular_elliptical_angle_mapping(row[self.diffusedangle_processed_feature]) if isnotNaN(row[self.diffusedangle_processed_feature]) else np.nan,axis=1)
        df[self.diffusedangle_mapped_feature]=df[self.diffusedangle_mapped_feature].fillna(0)
        #Generation of 'AberrationMapped' feature using features as 'AberrationProcessed'
        #'AberrationMapped' NaN values are replaced by 0
        df[self.aberration_mapped_feature]=df.apply(lambda row: aberration_mapping(row[self.aberration_feature]) if isnotNaN(row[self.aberration_feature]) else np.nan,axis=1)
        df[self.aberration_mapped_feature]=df[self.aberration_mapped_feature].fillna(0)
        
        return df

#Generation of 'SurfaceFlatnessMapped','SurfaceQualityMapped' and 'WavefrontErrorMapped' features
class SurfacefeaturesMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.mapped_features_list=MappedFeaturesList
    
    def fit(self,df):
        
        self.surfaceflatness_processed_feature=self.processed_features_list[17]
        self.surfacequality_processed_feature=self.processed_features_list[18]
        self.wavefronterror_processed_feature=self.processed_features_list[19]
        
        self.surfaceflatness_mapped_feature=self.mapped_features_list[14]
        self.surfacequality_mapped_feature=self.mapped_features_list[15]
        self.wavefronterror_mapped_feature=self.mapped_features_list[16]
        
        return self
    
    def transform(self,df):
        #Generation of 'SurfaceFlatnessMapped' feature using features as 'SurfaceFlatnessProcessed'
        #'SurfaceFlatnessMapped' NaN values are replaced by 0
        df[self.surfaceflatness_mapped_feature]=df.apply(lambda row: surfaceflatness_mapping(row[self.surfaceflatness_processed_feature]) if isnotNaN(row[self.surfaceflatness_processed_feature]) else np.nan,axis=1)
        df[self.surfaceflatness_mapped_feature]=df[self.surfaceflatness_mapped_feature].fillna(0)
        #Generation of 'SurfaceQualityMapped' feature using features as 'SurfaceQualityProcessed'
        #'SurfaceQualityMapped' NaN values are replaced by 0
        df[self.surfacequality_mapped_feature]=df.apply(lambda row: surfacequality_mapping(row[self.surfacequality_processed_feature]) if isnotNaN(row[self.surfacequality_processed_feature]) else np.nan,axis=1)
        df[self.surfacequality_mapped_feature]=df[self.surfacequality_mapped_feature].fillna(0)
        #Generation of 'WavefrontErrorMapped' feature using features as 'WavefrontErrorProcessed'
        #'WavefrontErrorMapped' NaN values are replaced by 0
        df[self.wavefronterror_mapped_feature]=df.apply(lambda row: wavefronterror_mapping(row[self.wavefronterror_processed_feature]) if  isnotNaN(row[self.wavefronterror_processed_feature]) else np.nan,axis=1)
        df[self.wavefronterror_mapped_feature]=df[self.wavefronterror_mapped_feature].fillna(0)
        
        return df

#Generation of 'SpecialComponentsMapped','FiberComponentMapped' and 'FlangeHardwareMapped' features
class SpecialfeaturesMapping(TransformerMixin):     
    
    def __init__(self,ProcessedFeaturesList,OriginalFeaturesList,MappedFeaturesList):
    
        self.processed_features_list=ProcessedFeaturesList
        self.original_features_list=OriginalFeaturesList
        self.mapped_features_list=MappedFeaturesList
        
    def fit(self,df):
        
        self.coating_processed_feature=self.processed_features_list[2]
        
        self.breadcrumbs_feature=self.original_features_list[0]
        self.descriptionsupplier_feature=self.original_features_list[1]
        
        self.specialcomponents_mapped_feature=self.mapped_features_list[20]
        self.fibercomponent_mapped_feature=self.mapped_features_list[21]
        self.flangehardware_mapped_feature=self.mapped_features_list[22]
        
        return self
    
    def transform(self,df):
        #Generation of 'SpecialComponentsMapped' feature using features as 'breadcrumbs'
        #'SpecialComponentsMapped' NaN values are replaced by 0
        df[self.specialcomponents_mapped_feature]=df.apply(lambda row: special_component_mapping(row[self.breadcrumbs_feature]) if row[self.coating_processed_feature]=='Not_Available' else np.nan ,axis=1)
        df[self.specialcomponents_mapped_feature]=df[self.specialcomponents_mapped_feature].fillna(0)
        #Generation of 'FiberComponentMapped' feature using features as 'description_supplier'
        #'FiberComponentMapped' NaN values are replaced by 0
        df[self.fibercomponent_mapped_feature]=df.apply(lambda row: fibercomponent_mapping(row[self.descriptionsupplier_feature]) if ((row[self.coating_processed_feature]=='Not_Available') and ('SMA' in row[self.descriptionsupplier_feature])) else np.nan ,axis=1)
        df[self.fibercomponent_mapped_feature]=df[self.fibercomponent_mapped_feature].fillna(0)
        #Generation of 'FlangeHardwareMapped' feature using features as 'description_supplier'
        #'FlangeHardwareMapped' NaN values are replaced by 0
        df[self.flangehardware_mapped_feature]=df.apply(lambda row: flangehardware_mapping(row[self.descriptionsupplier_feature]) if ((row[self.coating_processed_feature]=='Not_Available') and (('Optics' in row[self.descriptionsupplier_feature]) or ('Gaskets' in row[self.descriptionsupplier_feature]) or ('Viton' in row[self.descriptionsupplier_feature]) or ('Hardware' in row[self.descriptionsupplier_feature]))) else np.nan ,axis=1)
        df[self.flangehardware_mapped_feature]=df[self.flangehardware_mapped_feature].fillna(0)
        
        return df

#Generation of 'FeatureMappedAmount' feature for recommendation engine
class MappedFeaturesSum(TransformerMixin):     
    
    def __init__(self,ResultFeatureList,CountingMappedFeaturesList):
    
        self.result_feature_list=ResultFeatureList
        self.counting_mapped_features_list=CountingMappedFeaturesList
    
    def fit(self,df):
        
        self.feature_mapped_amount=self.result_feature_list[0]
        
        return self
    
    def transform(self,df):
        #generation of 'FeatureMappedAmount' feature by adding speficic individual mapped features
        df[self.feature_mapped_amount]=df[self.counting_mapped_features_list].sum(axis=1)
        
        return df