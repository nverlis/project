## lab1


ссылка на датасет https://drive.google.com/drive/folders/1uQXClyqUj3JKq66xT7y42HuikdYCU6xi?usp=sharing 


## lab 2
<img width="1433" height="595" alt="image" src="https://github.com/user-attachments/assets/13ff6647-6709-4bfd-9306-30ab5285a4a0" />
<img width="1445" height="762" alt="image" src="https://github.com/user-attachments/assets/d606233b-08b0-408f-88e4-371fedb04f92" />
<img width="1365" height="54" alt="image" src="https://github.com/user-attachments/assets/426d8680-7fa4-4099-b685-ede80b99d9c8" />

Типы данных до изменения:

id                         object

title                      object

common_name                object

description                object

cas                        object

pubchem_id                 object

chemical_formula           object

weight                     object

appearance                 object

melting_point              object

boiling_point              object

solubility                 object

route_of_exposure          object

mechanism_of_toxicity      object

metabolism                 object

toxicity                   object

lethaldose                 object

carcinogenicity            object
use_source                 object
min_risk_level             object
health_effects             object
symptoms                   object
treatment                  object
created_at                 object
updated_at                 object
wikipedia                  object
uniprot_id                 object
kegg_compound_id           object
omim_id                    object
chebi_id                   object
biocyc_id                  object
ctd_id                     object
stitch_id                  object
drugbank_id                object
pdb_id                     object
actor_id                   object
export                     object
moldb_smiles               object
moldb_formula              object
moldb_inchi                object
moldb_inchikey             object
moldb_average_mass         object
moldb_mono_mass            object
origin                     object
state                      object
logp                       object
hmdb_id                    object
chembl_id                  object
chemspider_id              object
biodb_id                   object
synthesis_reference        object
structure_image_caption    object
synonyms_list              object
types                      object
cellular_locations         object
tissues                    object
pathways                   object
dtype: object
Типы данных после изменения: 
id                                      object
title                                   object
common_name                             object
description                             object
cas                                     object
pubchem_id                              object
chemical_formula                        object
weight                                 float64
appearance                              object
melting_point                           object
boiling_point                           object
solubility                              object
route_of_exposure                       object
mechanism_of_toxicity                   object
metabolism                              object
toxicity                                object
lethaldose                              object
carcinogenicity                       category
use_source                              object
min_risk_level                          object
health_effects                          object
symptoms                                object
treatment                               object
created_at                 datetime64[ns, UTC]
updated_at                 datetime64[ns, UTC]
wikipedia                               object
uniprot_id                              object
kegg_compound_id                        object
omim_id                                 object
chebi_id                                object
biocyc_id                               object
ctd_id                                  object
stitch_id                               object
drugbank_id                             object
pdb_id                                  object
actor_id                                object
export                                category
moldb_smiles                            object
moldb_formula                           object
moldb_inchi                             object
moldb_inchikey                          object
moldb_average_mass                     float64
moldb_mono_mass                        float64
origin                                category
state                                 category
logp                                   float64
hmdb_id                                 object
chembl_id                               object
chemspider_id                           object
biodb_id                                object
synthesis_reference                     object
structure_image_caption                 object
synonyms_list                           object
types                                   object
cellular_locations                      object
tissues                                 object
pathways                                object
dtype: object

