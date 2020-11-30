#lists and dictionnary used to create new 'FeatureApplicationProcessed' feature are shown below
#'FeatureApplicationProcessed' feature values are applications_dictionnary values
flat_windows_list=['UV and IR Windows','Visible Windows','Laser Line Windows','Specialty Windows>Infrared (IR) Material Windows',
               'Uncoated Laser Window Substrates','Ultrafast Lenses and Windows','Coated Windows>AR','Coated Windows>Optical',
                'Flat Rectangular Windows','Precision Rectangular Windows','Precision Round Windows','Precision Thin Round Windows',
                'Flat Round Windows','Flat Windows','Flat Substrates>Optical Parallels (Synthetic fused silica, Circle) φ10 - 20',
                  'Flat Substrates>Optical Parallels (BK7, Circle) φ10 - 20','Flat Substrates>Optical Parallels (Synthetic fused silica, Square) □10 - □20',
                  'Flat Substrates>Optical Parallels (BK7, Square) □10 - □20','Flat Substrates>Optical Flats (Circle)',
                  'Flat Substrates>Optical Flats (Square)','Flat Substrates>Optical Flats (Rectangle)',
                  'Flat Substrates>Reasonable Optical Flat (Circle)','Flat Substrates>Low Scattering Substrate',
                  'Flat Substrates>Float Glass']

wedged_windows_list=['Specialty Prisms','Specialty Windows>Wedged Windows','UV Fused Silica Wedged Windows','N-BK7 Wedged Windows','Wedged Substrates',
                     'Barium Fluoride Wedged Windows','Magnesium Fluoride Wedged Windows','Germanium Wedged Windows','Wedged Laser Windows',
                     'Silicon Wedged Windows','Zinc Selenide (ZnSe) Wedged Windows','Sapphire Wedged Windows','Calcium Fluoride Wedged Windows']

brewster_windows_list=['Plate Polarizers>Brewster Windows','UV Fused Silica Brewster Windows','Linear Polarizers>Brewster Windows']

diffusers_list=['Optical Diffusers']

mirror_list=['Concave Substrates','Curved Windows (Plano-Concave)','Curved Windows (Plano-Convex)','Elliptical Windows']

interferometers_testers_list=['Interferometry Windows','Laser Windows>Optical Flats','Flat Substrates>High Precision Optical Flats']

beam_samplers_list=['Laser Line Beamsplitters','Beam Samplers']

spherical_aberration_compensation_plates_list=['Spherical Aberration Compensation Plate']

beam_splitter_compensation_plates_list=['Light path correctors','AOI Beamsplitter']

optomechanical_components_list=['Optotune Laser Speckle Reducers','Window Mounts','High-Vacuum CF Components']

special_components_list=['Glass Domes','3M Light Control Film','Fused Silica Wafers']

applications_list=[flat_windows_list,wedged_windows_list,brewster_windows_list,diffusers_list,mirror_list,interferometers_testers_list,
                  beam_samplers_list,spherical_aberration_compensation_plates_list,beam_splitter_compensation_plates_list,
                  optomechanical_components_list,special_components_list]

applications_dictionnary = {
        1: 'Flat_windows',
        2: 'Wedged_windows',
        3: 'Brewster_windows',
        4: 'Diffusers',
        5: 'Mirrors',
        6: 'Interferometry_windows',
        7: 'Beam_samplers',
        8: 'Spherical_aberration_compensation_plates',
        9: 'Beam_splitter_compensation_plates',
        10: 'Optomechanical_components',
        11: 'Special_components'
    }

#lists and dictionnary used to create new 'SusbstrateProcessed' feature are shown below
#'SusbstrateProcessed' feature values are substrate_material_dictionnary values
BK7_list=['BK7','N-BK7'];silica_list=['Silica','UVFS','UV FS','silica'];kbr_list=['KBr'];caf2_list=['CaF2','CaF_2','CAF_2','Calcium','calcium','CaF<sub>2</sub>'];germanium_list=['Germanium','germanium']
sapphire_list=['Sapphire','sapphire'];silicon_list=['Silicon','silicon'];znse_list=['ZnSe','Zinc Selenide'];mgf2_list=['MgF2','Magnesium','MgF<sub>2</sub>','MgF_2'];baf2_list=['BaF2','BAF_2','Barium'];as87eco_list=['AS87ECO']
infrasil_list=['Infrasil','infrasil'];floatglass_list=['Float Glass','Float glass','float glass'];hardglass_list=['Hard Glass','Hard glass']
lowexpansionglass_list=['Low Expansion Glass','Low expansion glass'];coloredglass_list=['Colored Glass','Colored glass'];thermosetADC=['Thermoset ADC']
whitediffusingglass_list=['White Diffusing Glass'];b270_list=['B270'];borofloat_list=['Borofloat','BOROFLOAT'];gorillaglass_list=['Gorilla® Glass']
pollycristalline_list=['Polycrystalline'];polymerfilm_list=['Polymer Film'];pet_list=['PET'];opalglass_list=['Opal Glass'];zerodur_list=['ZERODUR','Zerodur']
polycarbonate_list=['Polycarbonate'];nacl_list=['NaCl'];optotune_list=['Optotune polymer'];zns_list=['Zinc Sulfide']

substrate_material_list=[BK7_list,silica_list,kbr_list,caf2_list,germanium_list,sapphire_list,silicon_list,znse_list,mgf2_list,
                        baf2_list,as87eco_list,infrasil_list,floatglass_list,hardglass_list,lowexpansionglass_list,coloredglass_list,
                        thermosetADC,whitediffusingglass_list,b270_list,borofloat_list,gorillaglass_list,pollycristalline_list,
                        polymerfilm_list,pet_list,opalglass_list,zerodur_list,polycarbonate_list,nacl_list,optotune_list,zns_list]    

substrate_material_dictionnary = {
        1: 'BK7',
        2: 'UVFS',
        3: 'KBr',
        4: 'CaF2',
        5: 'Germanium',
        6: 'Sapphire',
        7: 'Silicon',
        8: 'ZnSe',
        9: 'MgF2',
        10: 'BaF2',
        11: 'AS87ECO',
        12: 'Infrasil',
        13: 'Float Glass',
        14: 'Hard Glass',
        15: 'Low Expansion Glass',
        16: 'Colored Glass',
        17: 'Thermoset ADC',
        18: 'White Diffusing Glass',
        19: 'B270',
        20: 'Borofloat',
        21: 'Gorilla Glass',
        22: 'Polycrystalline CVD',
        23: 'Polymer Film',
        24: 'Pet',
        25: 'Opal Glass',
        26: 'Zerodur',
        27: 'Polycarbonate',
        28: 'NaCl',
        29: 'Optotune polymer',
        30: 'ZnS'
    }

#List of original features using during processing and mapping
original_features_list=['breadcrumbs','description_supplier','supplier','Substrate','Material','Substrate Material',
                        'Parallelism','Wedge angle','Parallelism ･ Wedge angle','Coating',
                       'Coated Surface Flatness','Wavelength Range (nm)','Wavelength range','Wavelength','AR Coating',
                        'AR Coating Range','Wavelength Range of AR Coating','Diameter (mm)','Diameter φD','Diameter',
                       'D','Diameter D','Window Diameter (Unmounted)','Dimensions (mm)','Outer dimension A','Outer dimension A×B',
                       'L, Length','W, Width','Dimensions','Minor Axis (mm)','Major Axis (mm)','Minor axis','Major axis',
                        'Minor axis D','Minor Diameter','Thickness (mm)','Thickness t','Thickness, mm','T, Thickness','Thickness T',
                       'Thickness', 'Window Thickness (Unmounted)','Edge Thickness te','Center Thickness tc','ET', 'CT',
                       'Radius of curvature r','ROC','Wedge Angle','Diffusing Angle (°)','Parallelism (arcmin)','Parallelism (arcsec)',
                       'Parallelism','Surface Flatness','Surface Flatness PV','Rear surfacesurface flatness','Surface Flatness PVr',
                       'Surface flatness of substrate','Surface flatness','Flatness','S1/S2 Surface Flatness','Surface flatness S1, S2',
                       '1st surface flatness:','Surface Flatness (@633 nm)','Surface Quality','Surface Quality(Scratch-Dig)',
                       'Surface quality (scratch-dig)','Surface quality','Surface quality S1, S2','S1/S2 Surface Quality',
                       'Transmitted Wavefront, P-V','Transmitted Wavefront Tolerance','Wavefront distortion','Transmitted Wavefront Error (@633 nm)',
                        'Transmitted Wavefront Error (@ 633 nm)','Transmitted Wavefront Error','Coating Specification','Reflection (%)',
                       'Transmittance (λ=10.6μm)','Reflectance over AR Coating Range','AR Coating Performance','AR Coating Reflectance',
                       'Reflectance Over AR Coating Range','list_title','Damage Threshold, Pulsed','Laser Damage Threshold','Damage Threshold: BK7 UVFS',
                        'Damage Threshold','Damage Threshold | Pulse','Optic Damage Threshold | Pulse','Wedge Angle of Back Surface',
                       'Aberration','Compatible Brewster Window | Minor Diameter','Compatible Brewster Window | Thickness']

#List of generated processed features
processed_features_list=['FeatureApplicationProcessed','SubstrateProcessed','CoatingProcessed','CoatingWavelengthProcessed (nm)',
                         'UncoatedWavelengthProcessed (nm)','DiameterProcessed (mm)','SquareSideProcessed (mm)','RectangleSidesProcessed (mm)',
                        'MinorAxisProcessed (mm)','MajorAxisProcessed (mm)','ThicknessProcessed (mm)','EdgeThicknessProcessed (mm)',
                        'CenterThicknessProcessed (mm)','CurvatureRadiusProcessed (mm)','WedgeAngleProcessed (°)','DiffusedAngleProcessed (°)',
                        'ParallelismProcessed (arcmin)','SurfaceFlatnessProcessed','SurfaceQualityProcessed (Scratch-Dig)','WavefrontErrorProcessed',
                        'ReflectanceProcessed (%)','LaserDamageThresholdProcessed (J/cm2)']

#List of generated mapped features
mapped_features_list=['FeatureApplicationMapped','CoatingMapped','CoatingWavelengthMapped','UncoatedWavelengthMapped','ShapeMapped','ShapeValueMapped',
                     'MirrorShapeMapped','ThicknessMapped','EdgeThicknessMapped','CenterThicknessMapped','CurvatureRadiusMapped',
                     'WedgeAngleMapped','DiffusedAngleMapped','ParallelismMapped','SurfaceFlatnessMapped','SurfaceQualityMapped','WavefrontErrorMapped',
                     'ReflectanceMapped','LaserDamageThresholdMapped','AberrationMapped','SpecialComponentsMapped','FiberComponentMapped','FlangeHardwareMapped']

#List contains mapped specific features which will be used for recommendation engine
counting_mapped_features_list=['FeatureApplicationMapped','CoatingMapped','CoatingWavelengthMapped','UncoatedWavelengthMapped','ShapeMapped','ShapeValueMapped',
                     'MirrorShapeMapped','ThicknessMapped','EdgeThicknessMapped','CenterThicknessMapped','CurvatureRadiusMapped',
                     'WedgeAngleMapped','DiffusedAngleMapped','AberrationMapped','SpecialComponentsMapped','FiberComponentMapped','FlangeHardwareMapped']

#List contains global feature (sum of specific mapped features) used in recommendation engine
result_feature_list=['FeatureMappedAmount']

#List contains values of 'FeatureApplicationProcessed' feature
features_application_list=['Flat_windows','Mirrors','Wedged_windows','Diffusers','Optomechanical_components','Beam_samplers','Brewster_windows',
                  'Spherical_aberration_compensation_plates','Beam_splitter_compensation_plates','Special_components']

#List contains values of 'suppliers' list
suppliers_list=['Edmund Optics','OptoSigma','EKSMA Optics','Thorlabs']

#Lists values below (all the lists till the end of this code cell) are mainly breadcrumbs and description_supplier values 
#which are needed for generating Processed and Mapped features
breadcrumbs_list=['Products>Laser Optics>Laser Windows>Optotune Laser Speckle Reducers','Home>Optics>Windows Substrates>Concave Substrates>Concave Mirror Substrates φ10',
           'Home>Optics>Windows Substrates>Concave Substrates>Concave Mirror Substrate for Laser','Home>Optics>Windows Substrates>Flat Substrates>Optical Flats (Circle)',
           'Home>Optics>Windows Substrates>Flat Substrates>Optical Flats (Square)','Home>Optics>Windows Substrates>Flat Substrates>Optical Flats (Rectangle)',
            'Home>Optics>Windows Substrates>Coated Windows>AR Coated Windows for High Power Laser','Home>Optics>Windows Substrates>Flat Substrates>Reasonable Optical Flat (Circle)']

optosigma_dimensions_breadcrumbs_list=['Home>Optics>Windows Substrates>Coated Windows>Light path correctors']

thorlabs_coating_description_list=['Customer Inspired!&nbsp Ø2.75" CF Flange, 150 nm - 4.5 µm Sapphire Window','Customer Inspired!&nbsp Ø2.75" CF Flange, 180 nm - 8 µm CaF_2 Window']

reflectance_breadcumbs_list=['Home>Optics>Windows Substrates>Coated Windows>Optical Windows with Anti-Reflection Coating',
                             'Home>Optics>Windows Substrates>Coated Windows>AR Coated Windows for High Power Laser',
                             'Products Home>Optical Elements>Optical Windows>Wedged Windows>Silicon Wedged Windows>Silicon Wedged Windows, AR Coating: 2 - 5 µm','Products Home>Optomechanical Components>Vacuum Components>High-Vacuum CF Components>High-Vacuum CF Flange Viewports for Ø1.5" Wedged Windows>High-Vacuum CF Flange Viewports for Ø1.5" Wedged Windows',
                             'Products Home>Optomechanical Components>Vacuum Components>High-Vacuum CF Components>High-Vacuum CF Flange Viewports for Ø1.5" Windows>High-Vacuum CF Flange Viewports for Ø1.5" Windows',
                             'Products Home>Optomechanical Components>Vacuum Components>High-Vacuum CF Components>High-Vacuum CF Flange Viewports for Ø1.5" Windows>Ø1.5" UV Fused Silica Flat Vacuum Windows']

surfacequality4020_breadcrumbs_list=['Home>Optics>Windows Substrates>Coated Windows>Optical Windows with Anti-Reflection Coating',
                                    'Home>Optics>Windows Substrates>UV and IR Windows>Sapphire Windows for Infrared Laser',
                                    'Home>Optics>Windows Substrates>UV and IR Windows>ZnSe Windows for Infrared Laser',
                                    'Home>Optics>Windows Substrates>UV and IR Windows>Germanium Windows for Infrared Laser',
                                    'Home>Optics>Windows Substrates>UV and IR Windows>Silicon Windows for Infrared Laser',
                                    'Products Home>Optical Elements>Optical Windows>Wedged Windows>Silicon Wedged Windows>Silicon Wedged Windows, AR Coating: 2 - 5 µm']

surfacequality2010_breadcrumbs_list=['Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 1050 - 1700 nm)',
                                    'Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 650 - 1050 nm)',
                                    'Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 350 - 700 nm)',
                                    'Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 245 - 400 nm)',
                                    'Home>Optics>Windows Substrates>UV and IR Windows>Water Free Synthetic Fused Silica Windows for Infrared Laser',
                                    'Home>Optics>Windows Substrates>Flat Substrates>High Precision Optical Flats',
                                    'Home>Optics>Windows Substrates>Concave Substrates>Concave Mirror Substrates φ10']

surfacequality105_breadcrumbs_list=['Home>Optics>Windows Substrates>Coated Windows>AR Coated Windows for High Power Laser']

surfaceflatlambda2_breadcrumbs_list=['Products Home>Optical Elements>Optical Windows>Wedged Windows>Silicon Wedged Windows>Silicon Wedged Windows, AR Coating: 2 - 5 µm',
                                    'Home>Optics>Windows Substrates>Concave Substrates>Concave Mirror Substrates φ10']
surfaceflatlambda4_breadcrumbs_list=['Home>Optics>Windows Substrates>Concave Substrates>Concave Mirror Substrate for Laser',
                                    'Products>Optics>Windows and Diffusers>Visible Windows>λ/4 N-BK7 Precision Windows']
surfaceflatlambda8_breadcrumbs_list=['Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 1050 - 1700 nm)',
                                    'Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 350 - 700 nm)',
                                    'Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 245 - 400 nm)',
                                    'Products Home>Optical Elements>Optical Beamsplitters>Plate Beamsplitters>Beam Samplers>UV Fused Silica Beam Samplers (AR Coating: 650 - 1050 nm)']
surfaceflatlambda10_breadcrumbs_list=['Home>Optics>Windows Substrates>Coated Windows>Optical Windows with Anti-Reflection Coating',
                                     'Home>Optics>Windows Substrates>Coated Windows>AR Coated Windows for High Power Laser',
                                     'Home>Optics>Windows Substrates>Flat Substrates>Reasonable Optical Flat (Circle)',
                                     'Products>Laser Optics>Laser Windows>Uncoated Laser Window Substrates',
                                     'Products>Optics>Windows and Diffusers>UV and IR Windows>Zinc Selenide (ZnSe) Windows']

#Dictionnary used to map substrates with their wavelength range in nm
wavelength_dictionnary={
        1: '350 - 2200',
        2: '200 - 2200',
        4: '200 - 7000',
        5: '2000 - 14000',
        6: '200 - 5500',
        7: '1200 - 7000',
        8: '600 - 18000',
        9: '120 - 7000',
        10: '200 - 12000',
        12: '300 - 3000',
        13: '350 - 2000',
        14: '380 - 2300',
        15: '400 - 2500',
        18: '400 - 700',
        19: '350 - 2500',
        22: '200 -12000',
        26: '400 - 2300',
        27: '400 - 1600'
}

#'FeatureApplicationMapped' feature values for recommendation engine
featureapplication_mapping={
    'Flat_windows':10000000,
    'Mirrors':9000000,
    'Wedged_windows': 8000000,
    'Diffusers':7000000,
    'Interferometry_windows': 6000000,
    'Optomechanical_components': 5000000,
    'Beam_samplers': 4000000,
    'Spherical_aberration_compensation_plates': 3000000,
    'Beam_splitter_compensation_plates': 2000000,
    'Special_components': 1000000
}

#'CoatingMapped' feature values for recommendation engine
coating_mapping={'Uncoated':500000,
              'Coated':0,
              'Not_Available':0
}

#'UncoatedWavelengthMapped' feature values for recommnendation engine
uncoated_wavelength_mapping={ 
                    '350 - 2200': 20000,
                    '350 - 2000': 20000,
                    '380 - 2300': 20000,
                    '350 - 2500': 20000,
                    '400 - 2300': 20000,
                    '400 - 2500': 20000,
                    '300 - 3000': 20000,
                    '200 - 2200': 40000,
                    '200 - 1500': 40000,
                    '200 - 3500': 40000,
                    '280 - 2100': 40000,
                    '200 - 3200': 40000,
                    '400 - 1500': 60000,
                    '400 - 1600': 60000,
                    '400 - 700': 60000,
                    '250 - 700': 80000,
                    '425 - 675': 80000,
                    '400 - 1000': 80000,
                    '700 - 1100': 80000,
                    '120 - 7000': 100000,
                    '200 - 7000': 100000,
                    '200 - 5500': 100000,
                    '200 - 12000': 120000,
                    '250 - 16000': 120000,
                    '250 - 26000': 120000,
                    '400 - 12000': 140000,
                    '3000 - 12000': 140000,
                    '600 - 18000': 140000,
                    '1200 - 7000': 160000,
                    '2000 - 14000':160000,
                    '8000 - 14000':160000                        
}

#'CoatedWavelengthMapped' feature values for recommnendation engine
coating_wavelength_mapping={
                '250 - 425': 20000,
                '245 - 400': 20000,
                '250 - 450': 20000,
                '250 - 700': 40000,
                '350 - 450': 60000,
                '425 - 675': 60000,
                '450 - 650': 60000,
                '350 - 700': 60000,
                '400 - 700': 60000,
                '425 - 700': 60000,
                '350 - 1100': 80000,
                '400 - 1000': 80000,
                '650 - 1050': 80000,
                '600 - 1050': 80000,
                '700 - 1150': 100000,
                '700 - 1100': 100000,
                '900 - 1080': 100000,
                '750 - 1550': 120000,
                '600 - 1700': 120000,
                '1050 - 1700':120000,
                '1200 - 1600':120000,
                '1900 - 2100':120000,
                '1650 - 3000':140000,
                '2000 - 5000':140000,
                '1900 - 6000':140000,
                '3000 - 5000':140000,
                '4500 - 7500':140000,
                '2000 - 13000':160000,
                '3000 - 12000':160000,
                '7000 - 12000':160000,
                '8000 - 12000':160000,
                '261 - 266': 200000,
                '266': 210000,
                '343': 220000,
                '355': 230000,
                '405': 240000,
                '515': 250000,
                '523 - 532': 260000,
                '523 - 532 & 1047 - 1064': 270000,
                '532': 280000,
                '633': 290000,
                '785': 300000,
                '980': 310000,
                '1030': 320000,
                '1047 - 1064': 330000,
                '1064': 340000,
                '1080': 350000,
                '1550': 360000,
                '610 - 860': 370000,
                '633 - 1064': 380000,
                '10600': 400000,
                '700 - 10000': 420000  
}