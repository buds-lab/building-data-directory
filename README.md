# building-data-directory  
This is the program file of the Building Data Genome Directory, a comprehensive building dataset collection, where you can find the links for the datasets related with building energy research.  

**· For users:**

Welcome to Building Data Genome Directory!

The Building Data Genome Directory is an open data-sharing platform (buildingdatadirectory.org/) providing essential data for building energy research. It offers valuable datasets at various spatial and temporal scales, covering meter, building-level, and community-level data. The 60 datasets were sourced from governments, research institutes, and online energy dashboards. Users can also contribute by suggesting datasets through the crowdsourcing mechanism. This directory supports research and applications for building energy efficiency, crucial for addressing global energy and environmental challenges.

The _META DIRECTORY_ page shows the data categories included in our directory.

![Figure 1  Types of Datasets included in Building Data Genome Directory](https://github.com/buds-lab/building-data-directory/assets/79083820/49778a5c-edeb-4263-8fdd-f51f01bfc194)

You can choose the desired category from the left-hand sidebar.

![image](https://github.com/buds-lab/building-data-directory/assets/79083820/911a5696-bb4f-4c5c-aed7-6aa1164b03f0)

Or upload the dataset you want to share from the left-hand sidebar.

![image](https://github.com/buds-lab/building-data-directory/assets/79083820/039e7991-bf38-4212-b404-805414f3519c)

The sub-page of _Building Energy and Water Data_ has filtering functions on the left-hand sidebar and visualization functions below the table.

![image](https://github.com/buds-lab/building-data-directory/assets/79083820/1aebd4d4-3578-457c-954b-776e1ee9c3f3)
![image](https://github.com/buds-lab/building-data-directory/assets/79083820/636e0d54-64ba-41b5-8a67-26901cc637c0)

The preprint of the paper _The Building Data Genome Directory – An open, comprehensive data sharing platform for building performance research_ has been added to arxiv https://arxiv.org/abs/2307.00793

To cite the Building Data Genome Directory:

arXiv:2307.00793 [stat.AP](or arXiv:2307.00793v1 [stat.AP] for this version)

https://doi.org/10.48550/arXiv.2307.00793

**· For developers:**
The files with the suffix of ".py" are built for the streamlit webpage, the "META_DIRECTORY.py" is the main page (i.e., the meta directory). Other files in the folder "pages" are for the sub-pages of the streamlit api.  
The “Procfile” file is the instruction for running the main page. If there is any change on the main page program file name, remember to make revision on that.  
If any new library is imported, please note to add "lirary_name == version" (e.g., "plotly == 5.10.0") in the "requirements.txt" file.  
The media files required on the API website ("meta directory.png", "browsing.gif"), history codes and tables ("history codes", "previous lists") are also stored in this repository.
