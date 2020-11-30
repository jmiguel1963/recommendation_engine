#import python librairies needed for the task
import pandas as pd
from sklearn.pipeline import Pipeline
import configuration as config
import functions_classes as fc

#json file path
path=r'C:\Users\Jose Miguel\Downloads\windows.json'

#Dataframe generation from json file
df=pd.read_json(path)

#pipeline of all processing steps
processing_pipe=Pipeline([('DataframeModification',fc.DataFrameModification()),('FeatureApplicationCreation',fc.FeatureApplicationCreation(config.processed_features_list,config.applications_list,config.applications_dictionnary,config.original_features_list)),
                   ('FeatureApplicationModification',fc.FeatureApplicationModification(config.original_features_list,config.processed_features_list,config.features_application_list)),
                   ('SubstrateProcessedCreation',fc.SubstrateProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list,config.breadcrumbs_list,config.substrate_material_list,config.substrate_material_dictionnary)),
                   ('CoatingProcessedCreation',fc.CoatingProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list,config.thorlabs_coating_description_list)),
                   ('CoatingWavelengthProcessedCreation',fc.CoatingWavelengthProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('UncoatedWavelengthProcessedCreation',fc.UncoatedWavelengthProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list,config.substrate_material_list,config.wavelength_dictionnary)),
                   ('DiameterProcessedCreation',fc.DiameterProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('SquareRectangleProcessedCreation',fc.SquareRectangleProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list,config.optosigma_dimensions_breadcrumbs_list)),
                   ('MinorMajorAxisProcessedCreation',fc.MinorMajorAxisProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('ThicknessProcessedCreation',fc.ThicknessProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('CurvatureRadiusProcessedCreation',fc.CurvatureRadiusProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('WedgeAngleProcessedCreation',fc.WedgeAngleProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('DiffusedAngleProcessedCreation',fc.DiffusedAngleProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('ParallelismProcessedCreation',fc.ParallelismProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('SurfaceFlatnessProcessedCreation',fc.SurfaceFlatnessProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list,config.surfaceflatlambda2_breadcrumbs_list,config.surfaceflatlambda4_breadcrumbs_list,config.surfaceflatlambda8_breadcrumbs_list,config.surfaceflatlambda10_breadcrumbs_list)),
                   ('SurfaceQualityProcessedCreation',fc.SurfaceQualityProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list,config.surfacequality105_breadcrumbs_list,config.surfacequality2010_breadcrumbs_list,config.surfacequality4020_breadcrumbs_list)),
                   ('WavefrontDistortionProcessedCreation',fc.WavefrontDistortionProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list)),
                   ('ReflectanceProcessedCreation',fc.ReflectanceProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list,config.reflectance_breadcumbs_list)),
                   ('DamageThresholdProcessedCreation',fc.DamageThresholdProcessedCreation(config.processed_features_list,config.original_features_list,config.suppliers_list))])                  
#pipeline of all mapping steps
mapping_pipe=Pipeline([('ApplicationAndCoatingMapping',fc.ApplicationAndCoatingMapping(config.processed_features_list,config.mapped_features_list)),
                      ('WavelengthMapping',fc.WavelengthMapping(config.processed_features_list,config.mapped_features_list)),
                      ('DimensionsMapping',fc.DimensionsMapping(config.processed_features_list,config.original_features_list,config.mapped_features_list)),
                      ('ThicknessMapping',fc.ThicknessMapping(config.processed_features_list,config.original_features_list,config.mapped_features_list)),
                      ('MirrorsShapeMapping',fc.MirrorsShapeMapping(config.processed_features_list,config.original_features_list,config.mapped_features_list)),
                      ('WedgeAngleParallelismMapping',fc.WedgeAngleParallelismMapping(config.processed_features_list,config.mapped_features_list)),
                      ('DiffusingangleAberrationMapping',fc.DiffusingangleAberrationMapping(config.processed_features_list,config.original_features_list,config.mapped_features_list)),
                      ('SurfacefeaturesMapping',fc.SurfacefeaturesMapping(config.processed_features_list,config.mapped_features_list)),
                      ('SpecialfeaturesMapping',fc.SpecialfeaturesMapping(config.processed_features_list,config.original_features_list,config.mapped_features_list)),
                      ('MappedFeaturesSum',fc.MappedFeaturesSum(config.result_feature_list,config.counting_mapped_features_list))])  

#execution of both pipelines
df=processing_pipe.fit_transform(df)
df=mapping_pipe.fit_transform(df) 
 
#dataframe modified saved in csv format
df.to_csv(r'recommendation.csv',index=False)
