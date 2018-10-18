Test for Static folders
***********************


This option requires that each .rst that contains some static files (images for example) 
has to be inside their own folders, with a subfolder _static. The name of the folder has 
to be included in the conf.py as follows

# Include in folders the name of each one of the lecture folders
folders =  ["images", "simple_notebook", "test_static"]

The builder wil take this folder structure and it will be replicated in 
_build/jupyter, where each notebook will have their own folder with the 
respective static files.


Image 
-----

.. image:: _static/hood.jpg