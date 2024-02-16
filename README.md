Source code for https://leukemia-outlier.cmm.cit.tum.de

## Docker
A docker image can be created using the recipe in docker. A built image on 02.16.2024 is also available [here].
If you download the built image, run: `sudo docker load --input mll_website.tar` to load the image.  
Run the image: `sudo docker run -it -p 8080:8080 mll_website`.
This will start a gunicorn server which serves the website on port 8080. Then you should configure nginx to proxy the website.
