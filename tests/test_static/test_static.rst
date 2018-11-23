Test for Static folders
***********************


This option requires that each .rst that contains some static files (images for example) 
has to be inside their own folders, with a subfolder _static. The name of the folder has 
to be included in the conf.py as follows

Include in *folders* the name of each one of the lecture folders

.. code:: python

    folders =  ["Lecture_1", "Lecture_2", "Lecture_3"]

The builder wil take this folder structure and it will be replicated in 
_build/jupyter, where each notebook will have their own folder with the 
respective static files, but also preserving a global _static for the 
files that were not included in *folders*


Image 
-----
.. jupyter-dependency:: _static/hood.jpg

.. image:: _static/hood.jpg