Test for Static folders
***********************


This option requires that each .rst that contains some static files (images for example) 
has to be inside their own folders, with a subfolder _static. 

The builder wil recognise this folder structure and it will be replicated in 
_build/jupyter, where each notebook will have their own folder with the 
respective static files, but also preserving a global _static 


Image 
-----

.. image:: _static/hood.jpg